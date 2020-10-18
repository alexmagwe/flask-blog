from flask_wtf import FlaskForm
from ..models import  *
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,FileField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError

        
class AccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    img=FileField('Update profile picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    submit= SubmitField('Update')
    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('That username is already taken')
        
    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('That email is already in use')


class Registerform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    img=FileField('Add profile picture',validators=[FileAllowed(['jpg','png','jpeg'])])
    confirm_password=PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('register')
    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is already taken')
    
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('That email is already in use')
        
class Loginform(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember me') 
    submit=SubmitField('Login')
class ResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField('Reset')
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Account not found,are u registered?')
class PasswordResetForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm password',validators=[DataRequired(),EqualTo('password')])
    submit= SubmitField('Reset')
    
            