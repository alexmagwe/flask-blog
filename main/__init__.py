from flask import Blueprint
counter_app=Blueprint('counter_app',__name__)
from . import views