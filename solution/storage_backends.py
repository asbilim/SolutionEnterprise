from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False
    default_acl = 'public-read'
    querystring_auth = True
    querystring_expire = settings.AWS_QUERYSTRING_EXPIRE
    signature_version = 's3v4'
    
    def __init__(self, *args, **kwargs):
        kwargs['signature_version'] = self.signature_version
        super().__init__(*args, **kwargs)
    
    def url(self, name, parameters=None, expire=None):
        """
        Generate a signed URL for the file that expires after the specified time.
        """
        return super().url(name, parameters=parameters, expire=expire) 