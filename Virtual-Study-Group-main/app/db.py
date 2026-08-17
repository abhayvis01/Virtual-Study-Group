import os
import logging
from pymongo import MongoClient
import firebase_admin
from firebase_admin import credentials

logger = logging.getLogger(__name__)

class MongoWrapper:
    def __init__(self):
        self.client = None
        self.db = None
        self.is_connected = False

    def init_app(self, app):
        mongo_uri = app.config.get('MONGO_URI', 'mongodb://localhost:27017/virtual_study_group')
        db_name = app.config.get('MONGO_DBNAME', 'virtual_study_group')
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.is_connected = True
            logger.info("Successfully connected to MongoDB!")
            print(f"[DB] Connected to MongoDB database: {db_name}")
            
            # Ensure DB indexes
            from app.services.mongo_service import ensure_indexes
            ensure_indexes()
        except Exception as e:
            logger.warning(f"MongoDB connection failed: {e}. Falling back to simulated MongoDB memory store.")
            print(f"[DB Warning] MongoDB connection failed ({e}). Operating with local fallback data engine.")
            self.client = None
            self.db = None
            self.is_connected = False

mongo = MongoWrapper()
firebase_app = None

def init_firebase(app):
    global firebase_app
    cred_path = app.config.get('FIREBASE_CREDENTIALS_PATH')
    bucket_name = app.config.get('FIREBASE_STORAGE_BUCKET')
    
    if cred_path and os.path.exists(cred_path):
        try:
            cred = credentials.Certificate(cred_path)
            options = {'storageBucket': bucket_name} if bucket_name else {}
            firebase_app = firebase_admin.initialize_app(cred, options)
            print("[Firebase] Successfully initialized Firebase Admin SDK.")
        except Exception as e:
            print(f"[Firebase Warning] Failed to initialize Firebase Admin SDK: {e}")
    else:
        print("[Firebase Note] No valid FIREBASE_CREDENTIALS_PATH provided. Running with local auth/storage fallback mode.")
