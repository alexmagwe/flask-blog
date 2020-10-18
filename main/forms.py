from flask_wtf import FlaskForm
from ..models import  *
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,FileField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError

        

    
class Usergreeting(FlaskForm):
    name=StringField('enter  user name',validators=[DataRequired()])
    submit=SubmitField('submit')

