"""
Google Cloud Storage configuration for Django media files.
This allows uploading user avatars and other media to GCS.
"""
import os
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage


class MediaStorage(GoogleCloudStorage):
    """
    Custom storage backend for media files (avatars, uploads).
    Uses Google Cloud Storage for production.
    """
    bucket_name = os.getenv('GCS_BUCKET_NAME', 'deaddevelopers-media')
    file_overwrite = False
    default_acl = 'publicRead'
    
    def __init__(self, *args, **kwargs):
        # Only use GCS if credentials are configured
        if os.getenv('GCS_CREDENTIALS_PATH') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            super().__init__(*args, **kwargs)
        else:
            # Fall back to local storage in development
            from django.core.files.storage import FileSystemStorage
            self.__class__ = FileSystemStorage
            super(FileSystemStorage, self).__init__(*args, **kwargs)
