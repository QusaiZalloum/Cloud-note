from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

# Initialize SQLAlchemy instance
from .models import db

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Initialize LoginManager for user session management
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Qusai') # Use environment variable for secret key
    
    # Configure SQLAlchemy using DATABASE_URL from environment variables
    # Default to local PostgreSQL if DATABASE_URL is not set
    database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:QusaiPOSTGRES204@localhost/MyDB')
    # Railway provides postgresql:// URLs, but SQLAlchemy needs postgresql://
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    from .views import views
    from .auth import auth
    
    # Register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # Setup login manager
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables if they don't exist
    # Note: Railway might handle migrations differently, but this ensures tables are created
    with app.app_context():
        db.create_all()
    
    return app
