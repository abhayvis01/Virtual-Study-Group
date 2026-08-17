import os
from dotenv import load_dotenv

# Load environment variables from a .env file if available
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'AIzaSyCmeN6ZIODz3G3p09ELhVJWxsPJJeLEGn0')
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ['true', '1', 't']
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://vhost150506_db_user:[EMAIL_ADDRESS]/virtual_study_group')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'virtual_study_group')
    
    # Firebase Service Account Credentials Path
    FIREBASE_CREDENTIALS_PATH = os.environ.get('FIREBASE_CREDENTIALS_PATH', '')
    FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET', 'virtual-study-group-8c560.firebasestorage.app')
    
    # Firebase Web App JS Config
    FIREBASE_CONFIG = {
        'apiKey': os.environ.get('FIREBASE_API_KEY', 'AIzaSyz3G3p09ELhVJWxsPJJeLEGn0'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', 'virtual-study-group-8c560.firebaseapp.com'),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID', 'virtual-studoup-560'),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', 'virtual-study-group-8c560.firebasestorage.app'),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', '295693778'),
        'appId': os.environ.get('FIREBASE_APP_ID', '1:295678ad52c7a24f787c0d9a9ab'),
        'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID', 'G-N3Z9W9M8')
    }

    # File Upload Config
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'ppt', 'pptx', 'zip'}