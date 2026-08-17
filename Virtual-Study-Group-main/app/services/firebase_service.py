import os
import uuid
import logging
from flask import current_app
import firebase_admin
from firebase_admin import storage, auth

logger = logging.getLogger(__name__)

class FirebaseService:
    @staticmethod
    def verify_id_token(id_token):
        """Verifies a Firebase ID token sent from the client UI."""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            logger.error(f"Firebase token verification failed: {e}")
            return None

    @staticmethod
    def upload_file(file_storage, folder="resources"):
        """
        Uploads file to Firebase Storage bucket if configured,
        otherwise saves locally into app/static/uploads/.
        """
        filename = file_storage.filename
        if not filename:
            return None, ""

        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        
        # Check if Firebase Storage Bucket is initialized
        try:
            bucket_name = current_app.config.get('FIREBASE_STORAGE_BUCKET')
            if bucket_name and firebase_admin._apps:
                bucket = storage.bucket(bucket_name)
                blob = bucket.blob(f"{folder}/{unique_name}")
                blob.upload_from_file(file_storage, content_type=file_storage.content_type)
                blob.make_public()
                logger.info(f"Uploaded file to Firebase Storage: {blob.public_url}")
                return filename, blob.public_url
        except Exception as e:
            logger.warning(f"Firebase Storage upload failed: {e}. Falling back to local filesystem storage.")

        # Local Filesystem Storage Fallback
        upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(current_app.root_path, 'static', 'uploads'))
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_name)
        file_storage.seek(0)
        file_storage.save(file_path)
        
        local_url = f"/static/uploads/{unique_name}"
        return filename, local_url
