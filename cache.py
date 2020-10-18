'''from flask import Flask,render_template,url_for,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from forms import  Registerform,Loginform,Usergreeting
from flask_moment import Moment
from flask_migrate import Migrate,MigrateCommand
from datetime import datetime
# from models import User
from flask_bootstrap import Bootstrap
import os
basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config.from_pyfile('config.py')
db=SQLAlchemy(app)
bootstrap=Bootstrap(app)
moment=Moment(app)


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,index=True)
    email=db.Column(db.String(100),unique=True)
    
    def __repr__(self):
        return'<User %r %r>'%(self.username,self.email)
    
@app.route('/')
def home():
    return render_template('home.htm',current_date=datetime.utcnow())

@app.route('/blogs')
def blogs():
    return render_template('blogs.htm',current_date=datetime.utcnow())
@app.route('/about')
def about():
    return render_template('about.htm')

@app.route('/register',methods=['GET','POST'])
def register():
    form=Registerform()
    # if form.validate_on_submit():
        
    return render_template('register.htm',title='register',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form=Loginform()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).all()
        print(user)
        if not user :
            flash('wrong email')
            #return redirect(url_for('home'))

            
        else:
            flash('you exist in database')
            #return redirect(url_for('home',name=user))
    return render_template('login.htm',title='Login',form=form)
    
    
@app.route('/user',methods=['GET','POST'])
def user():
    form=Usergreeting()
    if form.validate_on_submit():
        session['name']=form.name.data
        name=form.name.data
        if name==session['name']:
            flash('welcome back alex')
        else:
            flash('welcome to the family %s'%name)
        form.name.data=''
        return redirect(url_for('home'))
    return render_template('greeting.htm',form=form,name=session.get('name'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page.htm'),404
@app.errorhandler(500)
def internal_server_error(e):
    return '<h1>INTERNAL SERVER ERROR OCCURED</h1>'



if __name__=='__main__':
    app.run(port=3000)'''
