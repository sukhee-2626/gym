"""
SmartGym Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'smartgym-secret-2024')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///smartgym.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.workout import workout_bp
    from app.routes.diet import diet_bp
    from app.routes.attendance import attendance_bp
    from app.routes.membership import membership_bp
    from app.routes.tracker import tracker_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.leaderboard import leaderboard_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/')
    app.register_blueprint(workout_bp, url_prefix='/workout')
    app.register_blueprint(diet_bp, url_prefix='/diet')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(membership_bp, url_prefix='/membership')
    app.register_blueprint(tracker_bp, url_prefix='/tracker')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')

    return app
