from . import db
from datetime import datetime
from . import admin
from . import login
import os
import secrets
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from passlib.hash import sha256_crypt
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,index=True,nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    profile_pic=db.Column(db.String(20),default='default.png')
    posts=db.relationship('Posts',backref='author',lazy='dynamic')
    
    
    def __repr__(self):
        return'<User %r %r>'%(self.username,self.email)
    
    def get_reset_tk(self,expires_sec=1800):
        s=Serializer(os.environ['SECRET_KEY'],expires_sec)
        
        return s.dumps({'user_id':self.id}).decode('utf-8')    
    def verify_reset_tk(token):
        s=Serializer(os.environ['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None  
        return User.query.get(user_id)
    
    def set_password(self,pswd):
        self.password=sha256_crypt.encrypt(pswd)    
        return pswd
    def check_password(self,pswd):
        return sha256_crypt.verify(pswd,self.password)
class Preview(db.Model):
    __tablename__='preview'
    id=db.Column(db.Integer,primary_key=True)
    caption=db.Column(db.String(100))
    img=db.Column(db.Text,nullable=False,default='default.jpg')
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    preview_of=db.Column(db.String(16),db.ForeignKey('posts.stamp'),nullable=False)

    
    def __repr__(self):
       return'<Date posted %r caption%r>'%(self.date_posted,self.caption) 
class Posts(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text)
    preview=db.relationship('Preview',backref='article',lazy='joined')
    title=db.Column(db.String(100))
    stamp=db.Column(db.String(16),unique=True)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    users_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    
    
    def __init__(self,*args,**kwargs):
        # creating unique id to relate with preview
        super(Posts,self).__init__(*args,**kwargs)
        self.stamp=secrets.token_hex(8)
        
        
    def __repr__(self):
       return'<Date posted %r Author%r>'%(self.date_posted,self.author)
    @property
    def has_preview(self):
        return len(self.preview)>0
    

admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Posts,db.session))
admin.add_view(ModelView(Preview,db.session))


