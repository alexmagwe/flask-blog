
from flask import redirect, render_template,url_for,Blueprint

errors=Blueprint('errors',__name__)
@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/error_404.htm'),404
@errors.app_errorhandler(500)
def internal_server_error(e):
    return  render_template('errors/error_500.htm'),500
@errors.app_errorhandler(403)
def internal_server_error(e):
    return  render_template('errors/error_403.htm'),403
