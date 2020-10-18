import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    # POSTGRES={'user':os.environ.get('POSTGRES_USER'),'password':os.environ.get('POSTGRES_PASSWORD'),'db':os.environ.get('POSTGRES_DB_NAME'),'host':os.environ.get('POSTGRES_HOST'),'port':os.environ.get('POSTGRES_PORT')}
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    POSTS_PER_PAGE=9
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True 
class Dev_config(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'dev-db.sqlite')
    MAIL_USE_TLS:True
    MAIL_PORT=587
    # DB_PASSWORD=os.environ['DB_PASSWORD']
    # DB_NAME=os.environ['DB_NAME']
    DB_SERVER='localhost'
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER='smtp.gmail.com'
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    DEBUG=True

class Testing_config(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'dev-db.sqlite')

class Production_config(Config):
    # SQLALCHEMY_DATABASE_URI='postgres://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s'%Config.POSTGRES
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
configs={
    'development':Dev_config,
    'testing':Testing_config,
    'production':Production_config,
    'default':Config,
    }
