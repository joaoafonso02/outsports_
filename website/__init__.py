from flask import Flask
from flask_mongoengine import MongoEngine
from os import path
from flask_login import LoginManager

db = MongoEngine()
DB_NAME = "OutSports"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['MONGODB_SETTINGS'] = {
        'db': DB_NAME,
        'host': 'mongodb://localhost:27017/' + DB_NAME
    }
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        try:
            # Try to load the user by ID
            return User.objects.get(id=id)
        except User.DoesNotExist:
            # Handle the case where the user doesn't exist
            return None

    return app
