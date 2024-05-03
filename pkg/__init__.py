import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message





migrate = Migrate()
csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()





def create_app():
    from pkg.models import db
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config['UPLOAD_FOLDER'] = 'static/book/'
    app.config['TEMP_DIR'] = os.path.join(app.instance_path, 'temp')
    os.makedirs(app.config['TEMP_DIR'], exist_ok=True)
    app.config['SECRET_KEY'] = 'sk_test_ead50eacadfcfa37f1e5f65f95551db34e36513b'
    app.config['PERMANENT_SESSION_LIFETIME'] = 600
    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    migrate.init_app(app,db)
    return app

app = create_app()


from pkg import admin_routes, user_routes