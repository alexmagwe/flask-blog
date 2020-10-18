
from flask_wtf import FlaskForm
from ..models import  *
from flask_login import current_user
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,TextAreaField,FileField
from wtforms.validators import DataRequired,Email,EqualTo,Length,ValidationError



class Postform(FlaskForm):
    title=StringField("TITLE",validators=[DataRequired()])
    content=TextAreaField('Body',validators=[DataRequired(),Length(min=1,max=10000)])
    img=FileField('Image',validators=[FileAllowed(['jpg','png','jpeg','svg'])])
    submit=SubmitField('Post')
