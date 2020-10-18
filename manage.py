import os
from . import create_app,db,migrate
from .models import User,Posts,Preview
# from . import email
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager



app=create_app()
manager=Manager(app)
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Posts':Posts,'Preview':Preview}

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
if __name__ == "__main__":
    manager.run()