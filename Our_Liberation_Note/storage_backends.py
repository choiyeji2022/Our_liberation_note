from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Static files configuration backend"""

    location = "static"
    default_acl = "public-read"


class PublicMediaStorage(S3Boto3Storage):
    """COnfiguration for public media files"""

    location = "media"
    default_acl = "public-read"
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    """COnfiguration for pricate media files"""

    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
