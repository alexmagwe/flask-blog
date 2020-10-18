from flask import Blueprint,render_template,abort,flash,url_for,redirect,session,request,current_app
import bleach
from .forms import Postform
from datetime import datetime
from .. import db
import os
from markdown import markdown
import secrets
from werkzeug.urls import url_parse
from flask_script import Shell
from . import blog
from flask_login import current_user,login_user,logout_user,login_required
from ..models import User,Posts,Preview
from passlib.hash import sha256_crypt

static_folder=blog.root_path.split('/')
static_folder="/".join(static_folder[:-1])+'/static'
imgfolder='blog-images'
#returns generated filename and saved path
def save_pic(file,folder=imgfolder,static_folder=static_folder):
    pic_hex=secrets.token_hex(8)
    _,pic_ext=os.path.splitext(file.filename)
    pic_name=pic_hex+pic_ext
    pic_path=os.path.join(static_folder,folder,pic_name)
    try:
        file.save(pic_path)
        url=url_for("static",filename=os.path.join(folder,pic_name))
    except Exception as e:
        return None
    return (pic_name,url)
#deletes files
def delete_pic(current_img,folder=imgfolder,static_folder=static_folder):
    pic_path=os.path.join(static_folder,folder,current_img)
    if os.path.exists(pic_path):
        try:
            os.remove(pic_path)
        except:
            print('failed to delete')
    else:
        print('picture not found ')
    

# all articles
@blog.route('/blogs',methods=['POST','GET'])
def blogs():
    page=request.args.get('page',1,type=int)
    
    pagination=Posts.query.order_by(Posts.date_posted.desc()).paginate(page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    posts=pagination.items
    
    return render_template('blog/blog.htm',current_date=datetime.utcnow(),posts=posts,pagination=pagination)


@blog.route('/blogs/<int:post_id>')
def post(post_id):
    post=Posts.query.get_or_404(post_id)
    return render_template('blog/post.htm',post=post)


@blog.route ('/blogs/update/<int:post_id>',methods=['GET'])
@login_required
def update_post(post_id):
    return render_template('blog/post_editor.html',action='update')
    # return {"content":post.content}
    

@blog.route ('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    post=Posts.query.get_or_404(id)
    if request.method=='POST':
        data=request.json
        post.content=cleaner(data.get('content'))
        post.title=data.get('title')
        image=data.get('img')
        cleaned_image=cleaner(image)
        post.preview[0].caption=post.title
        post.preview[0].img=cleaned_image
        try:
            db.session.commit()
            return{"success":'updated successfuly'}
        except Exception as e:
            db.session.rollback()
            return {"error":e},500
    if post:
        return {'content':post.content}
    else:
         return {"error":"article not found"} ,404  
    
#for local storage
# @blog.route('/blogs/<int:post_id>/delete/',methods=['GET','POST'])
# def delete_post(post_id):
#     folder='blog-images'
#     post=Posts.query.get_or_404(post_id)
#     image=url_for('static',filename=folder+"/"+post.img)
#     if post.author!=current_user:
#         abort(403)
#     db.session.delete(post)
#     delete_pic(static_folder,post.img,folder)
#     return redirect(url_for('blog.blogs'))

# for tiny drive hosted images
@blog.route('/blogs/<int:post_id>/delete/',methods=['GET','POST'])
def delete_post(post_id):
    post=Posts.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    return redirect(url_for('blog.blogs'))

#creating a new article with tinyMCE editor
@blog.route('/create',methods=['GET','POST'])
@login_required
def create():
    return render_template('blog/post_editor.html',action='create')
#publishing created article
def cleaner(content):
    allowed_tags=['a','div','span','aside','footer','p','br','hr','abbr','iframe','figure','figcaption','embed','video', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul','table','td','th','tr','img','h1','h1','h2','h3','h4','h5','h6']
    attrs = { '*': ['class','id','title','width','height','style'],'a': ['href', 'rel','target'],'img': ['src','alt'],'video':['src'],'iframe':['src'],'embed':['src','type']}
    styles=['width','height','text-align','margin','margin-top','margin-bottom','margin-left','margin-right','float','padding','padding-left','padding-bottom','padding-right','padding-top','border','border-top','border-left','border-right','border-bottom','background-color','background-image','background-position','background-repeat','background-origin','box-shadow','display','opacity','font-family','font-size','font-weight','color','position','border-radius','animation','transition']
    cleaned_content=bleach.linkify(bleach.clean(content,tags=allowed_tags,attributes=attrs,styles=styles,strip=True))
    return cleaned_content
@blog.route('/publish',methods=['POST'])
def publish():
    payload=request.json
    
    if (content:=payload.get('content')):
        articletitle=payload.get('title')
        if not articletitle:
            return 'add a title by adding a H1 header to the article',400
        cleaned_content=cleaner(content)
        post=Posts(content=cleaned_content,users_id=current_user._get_current_object().id,title=articletitle)
        image=payload.get('img')
        cleaned_image=cleaner(image)
        preview=Preview(caption=articletitle,img=cleaned_image,preview_of=post.stamp)
        db.session.add(post)
        db.session.add(preview)
        try:
            db.session.commit()
            return {'success':'published successfully'}
        except Exception as err:
            db.session.rollback()
            return {"error":err},400
    return 
#USED WITH TINYMCE FOR TESTING UPLOADING LOCAL FILES
def upload_image():
    img=request.files.get('file')
    location=save_pic(img)[1]
    return {"location":location}