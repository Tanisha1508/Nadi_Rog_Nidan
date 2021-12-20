from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_webapp.config import Config

#extensions:
db=SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'#-->fn name of our route
login_manager.login_message_category = 'info' # blue alert
mail = Mail()

# to avoid circular imports we add the import here:
# from flask_webapp import routes-->older

#create func of our app
def create_app(config_class=Config):
    #move creation of our app inside this fn
    app=Flask(__name__)
    app.config.from_object(Config)

    #initialize the extensions here but declare them outside: so that the extension object doesn't 
    # initially get bound to the application using this design pattern no app specific state is on the extension
    # object so one extension object can be used for multiple apps
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #register the blueprints
    from flask_webapp.users.routes import users
    from flask_webapp.main.routes import main
    from flask_webapp.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    return app

#now we will use current_app instead of app in other files