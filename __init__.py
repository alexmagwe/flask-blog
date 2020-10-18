from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate,MigrateCommand
from flask_moment import Moment
from sqlalchemy import MetaData
from flask_mail import Mail 
from .config import configs
from flask_login import LoginManager
from flask_admin import Admin

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })
login=LoginManager()
mail=Mail()
admin=Admin()
login.login_view='auth.login'
db=SQLAlchemy(metadata=meta)
bootstrap=Bootstrap()
migrate=Migrate()
moment=Moment()

from .email import *

def create_app():
    app=Flask(__name__)
    bootstrap.init_app(app)
    app.config.from_object(configs['production'])
    db.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    with app.app_context():
        if db.engine.url.drivername=='sqlite':
            migrate.init_app(app,db,render_as_batch=True)
        else:
            migrate.init_app(app,db)
    
    admin.init_app(app)
    from .main import counter_app as blueprint1
    app.register_blueprint(blueprint1)
    
    from .handlers.errors import errors
    app.register_blueprint(errors)
    
    from .authentication import auth
    app.register_blueprint(auth,url_prefix='/auth') 
    
    from .blog import blog
    app.register_blueprint(blog,url_prefix='/blog')
    
    return app
from blogssite.models import User,Posts
