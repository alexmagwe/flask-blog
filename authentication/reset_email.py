from flask import url_for,render_template
from ..email import send_email


def send_reset_email(user):
    token=user.get_reset_tk()
    send_email(subject='RESET PASSWORD',sender='noreply@gmail.com',recipients=[user.email], text=render_template('email/pswd_reset.txt',user=user,token=token),html=render_template('email/pswd_reset.htm',user=user,token=token))
    