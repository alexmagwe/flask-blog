
from flask import Blueprint,render_template,abort,flash,url_for,redirect,session,request
from blogssite.authentication.forms import Registerform,Loginform,AccountForm,ResetForm,PasswordResetForm
from flask_bootstrap import Bootstrap
import datetime
from .. import db
from PIL import Image
import os
from flask import current_app as app
from flask_mail import Message
import secrets
from blogssite.main import counter_app
from .reset_email import send_reset_email
from werkzeug.urls import url_parse
import jwt
from flask_script import Shell
from blogssite.authentication import auth
from flask_login import current_user,login_user,logout_user,login_required
from ..models import User,Posts
from passlib.hash import sha256_crypt



static_folder=auth.root_path.split('/')
static_folder="/".join(static_folder[:-1])+'/static'
def save_pic(static_folder,file,folder):
    print('file:',file)
    pic_hex=secrets.token_hex(8)
    _,pic_ext=os.path.splitext(file.filename)
    pic_name=pic_hex+pic_ext
    size=(400,400)
    img=Image.open(file)
    img.thumbnail(size)
    pic_path=os.path.join(static_folder,folder,pic_name)
    print(pic_path)
    img.save(pic_path)
    return pic_name
def delete_pic(static_folder,current_img,folder):
    pic_path=os.path.join(static_folder,folder,current_img)
    print('pic path:'+pic_path)
    if os.path.exists(pic_path):
        try:
            os.remove(pic_path)
        except:
            print('failed to delete')
    else:
        print('picture not found ')
    

@auth.route('/register',methods=['GET','POST'])
def register():
    form=Registerform()
    folder='profile_pics'
    if form.validate_on_submit():
            pswd=form.password.data
            if form.img.data:
                image=save_pic(static_folder,form.img.data,folder)
                user=User(username=form.username.data,email=form.email.data,profile_pic=image)
            else:
                user=User(username=form.username.data,email=form.email.data)
            user.set_password(pswd)
            db.session.add(user) 
            flash('account created succesfully','success') 
            return redirect(url_for('.login'))

                   
    return render_template('forms/register.htm',title='Register',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('counter_app.home'))
    form=Loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        pswd=form.password.data
        if user is None  or not user.check_password(pswd):
            flash('wrong email/password','danger')
            return redirect(url_for('auth.login'))
              
               
        login_user(user,remember=form.remember.data)
        next_page=request.args.get('next')
        if next_page:
            # print(next_page)
            next_page=next_page.split('/')[-2:]
            next_page=next_page[0]+"."+next_page[1]
            print(next_page)
        if not next_page or url_parse(next_page).netloc!='':
            next_page='counter_app.home'
        
        flash(f'Welcome back {user.username}','success')
        session['']=form.email.data
        return redirect(url_for(next_page))
    return render_template('forms/login.htm',title='Login',form=form)

    
@auth.route('/logout') 
def logout():
    logout_user()
    return redirect(url_for('counter_app.home'))


@auth.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('counter_app.home'))
    form=ResetForm()
    if form.validate_on_submit():
       
        user=User.query.filter_by(email=form.email.data).first()
        flash(f"an email has been sent to {user.email} with reset instructions",'info')
        send_reset_email(user)
        return redirect(url_for('auth.login'))

    return render_template('forms/email_reset.htm',title='RESET',form=form)

@auth.route('/new_password/<token>',methods=['GET','POST'])
def new_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('counter_app.home'))
    user=User.verify_reset_tk(token)
    if user is None:
        flash('token is invalid or expired,try again','danger')
        return redirect(url_for('auth.reset_request'))  
    form=PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        flash("password reset succesfully",'success')
        return redirect(url_for('auth.login'))
    return(render_template('forms/new_pswd.htm',form=form,user=user))


        
@auth.route('/user',methods=['GET','POST'])
@login_required
def user():
    folder='profile_pics'
    posts=current_user.posts.order_by(Posts.date_posted.desc()).all()
    form=AccountForm()
    if form.validate_on_submit():
        if form.img.data:
            delete_pic(static_folder,current_user.profile_pic,folder)
            file=form.img.data
            print(type(file))
            pic_file=save_pic(static_folder,file,folder)
            current_user.profile_pic=pic_file
        current_user.email=form.email.data
        current_user.username=form.username.data   
        db.session.commit()
        flash('account updated succesfully','success')
        return redirect(url_for('.user'))
    profile_pic=url_for('static',filename='/profile_pics/'+current_user.profile_pic)    
    print(profile_pic)
    form.email.data=current_user.email
    form.username.data=current_user.username
    # form.img.data=get_pic(current_user.profile_pic)
    return render_template('forms/user.htm',form=form,name=session.get('name'),posts=posts,profile_pic=profile_pic)

# tiny cloud authentication
@auth.route('/jwt',methods=["POST"])
def signjwt():
  
    if current_user.is_authenticated:
        with open(os.path.abspath('./authentication/tinydrivepkey'))as pkey:
            key=pkey.read()
        exp=datetime.datetime.utcnow()+datetime.timedelta(minutes=30)
        print(type(exp))
        payload={"sub":current_user.email,"name":current_user.email,"exp":exp}
        token=jwt.encode(payload,key,algorithm='RS256').decode('utf-8')
        return {"token":token}
    else:
        abort(403)