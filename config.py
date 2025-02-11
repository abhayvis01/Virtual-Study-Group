import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configuration class to hold application settings
class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Provide a default if not set
    DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']  # Convert to boolean

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here' # Added load_dotenv and set this to an environment variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False