from flask import Blueprint,render_template,abort,flash,url_for,redirect,session,request
from .forms import Usergreeting
from flask_bootstrap import Bootstrap
from datetime import datetime
from .. import db

import os
import secrets
from werkzeug.urls import url_parse
from flask_script import Shell
from . import counter_app
from flask_login import current_user,login_user,logout_user,login_required
from ..models import User,Posts
from passlib.hash import sha256_crypt


@counter_app.route('/')
@counter_app.route('/home')
def home():
    posts=Posts.query.all()
    return render_template('home.htm',current_date=datetime.utcnow(),posts=posts)
@counter_app.route('/about')
def about():
    return render_template('about.htm')

