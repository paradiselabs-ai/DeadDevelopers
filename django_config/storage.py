"""
Google Cloud Storage configuration for Django media files.
This allows uploading user avatars and other media to GCS.
"""
import os
from datetime import timedelta
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage


# Privacy note for `default_acl = 'publicRead'`:
# Avatars are world-readable at their GCS URL once uploaded. The route layer
# (routes/profile.py) gates *who can fetch the URL* — non-owners cannot view a
# private profile page, so they never receive the avatar URL through normal
# flow. URL guessing remains a residual risk: if an attacker learns the
# username and file extension, they can construct the public URL directly.
#
# Strict privacy (signed URLs that expire) requires:
#   1. default_acl = None (bucket default; bucket must be private)
#   2. Override `url()` to return a signed URL via `blob.generate_signed_url()`
#   3. Add a Django view that proxies avatar fetches with auth checks, OR
#      let GCS's signed URLs do the gating directly (preferred — no proxy cost)
# Tracked for post-MVP: avatar fetch should use generate_signed_url(expiration=...)
# whenever the owning user has is_public=False.


class MediaStorage(GoogleCloudStorage):
    """
    Custom storage backend for media files (avatars, uploads).
    Uses Google Cloud Storage for production.
    """
    bucket_name = os.getenv('GCS_BUCKET_NAME', 'deaddevelopers-media')
    file_overwrite = False
    default_acl = 'publicRead'

    def signed_url(self, name, expiration_seconds=3600):
        """Generate a time-limited signed URL for a private file.

        Use this for avatars/media belonging to users with is_public=False
        once we cut the bucket over to private-by-default.
        """
        blob = self.bucket.blob(self._normalize_name(name))
        return blob.generate_signed_url(
            expiration=timedelta(seconds=expiration_seconds),
            method='GET',
        )

    def __init__(self, *args, **kwargs):
        # Only use GCS if credentials are configured
        if os.getenv('GCS_CREDENTIALS_PATH') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            super().__init__(*args, **kwargs)
        else:
            # Fall back to local storage in development
            from django.core.files.storage import FileSystemStorage
            self.__class__ = FileSystemStorage
            super(FileSystemStorage, self).__init__(*args, **kwargs)
