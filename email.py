from flask_mail import Message,Mail
from flask import url_for
from . import mail
from threading import Thread
from flask import current_app as app

#asynchronous email 
def async_email(app,msg):
    with app.app_context():
        print('sending email')
        mail.send(msg)
        print('email sent')
        
def send_email(subject, sender, recipients, text, html):
    print(app.config['MAIL_SERVER'])
   
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text
    msg.html = html
    thr=Thread(target=async_email,args=[app._get_current_object(),msg])
    thr.start()

    