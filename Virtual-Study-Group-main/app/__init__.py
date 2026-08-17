# Werkzeug 3.x compatibility patch for Flask-Login legacy imports
import urllib.parse
import werkzeug.urls
if not hasattr(werkzeug.urls, 'url_encode'):
    werkzeug.urls.url_encode = urllib.parse.urlencode
if not hasattr(werkzeug.urls, 'url_decode'):
    werkzeug.urls.url_decode = lambda s, **kw: {k: v[0] if len(v) == 1 else v for k, v in urllib.parse.parse_qs(s, **kw).items()}
if not hasattr(werkzeug.urls, 'url_quote'):
    werkzeug.urls.url_quote = urllib.parse.quote

from flask import Flask
from flask_login import LoginManager
from config import Config
from app.db import mongo, init_firebase
from app.services.mongo_service import User

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB & Firebase Services
    mongo.init_app(app)
    init_firebase(app)

    # Context Processor for Firebase Web Config
    @app.context_processor
    def inject_firebase():
        return dict(firebase_config=app.config.get('FIREBASE_CONFIG'))

    # Initialize LoginManager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)

    # Register Blueprints
    from app.auth.routes import bp as auth_bp
    from app.main.routes import bp as main_bp
    from app.groups.routes import bp as groups_bp
    from app.resources.routes import bp as resources_bp
    from app.chat import chat_bp
    from app.api.routes import bp as api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(groups_bp, url_prefix='/groups')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    app.register_blueprint(chat_bp, url_prefix='/chat')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app