"""Production settings and globals."""

from .setting_helpers import Environment

env = Environment(strict=False)
aws = Environment('AWS')


# Use File system in local development instead of Amazon S3


# Defaults for development and testing
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE =\
    'django.contrib.staticfiles.storage.StaticFilesStorage'
THUMBNAIL_STORAGE = 'utils.local_file_storage.OverwriteStorage'

MEDIA_ROOT = env.MEDIA_DIR or '/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = env.STATIC_DIR or '/static/'
STATIC_URL = '/static/'


if env.aws_enabled:
    # AMAZON WEB SERVICES

    # STATICFILES_STORAGE = 'utils.aws_custom_storage.StaticStorage'
    DEFAULT_FILE_STORAGE = 'utils.aws_custom_storage.MediaStorage'
    THUMBNAIL_STORAGE = 'utils.aws_custom_storage.ThumbStorage'

    AWS_DEFAULT_ACL = 'public-read'
    AWS_STORAGE_BUCKET_NAME = aws.storage_bucket_name
    AWS_ACCESS_KEY_ID = aws.access_key_id
    AWS_SECRET_ACCESS_KEY = aws.secret_access_key
    AWS_S3_HOST = aws.s3_host
    AWS_S3_CUSTOM_DOMAIN = aws.s3_custom_domain  # cname
    AWS_S3_SECURE_URLS = False
    AWS_S3_USE_SSL = False
    AWS_S3_FILE_OVERWRITE = True

    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}/media/'
    # STATIC_URL = f'http://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATIC_URL = '/static/'


if env.digitalocean_enabled:
    # DIGITAL OCEAN SPACES

    STATICFILES_STORAGE =\
        'django.contrib.staticfiles.storage.StaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'utils.aws_custom_storage.MediaStorage'
    THUMBNAIL_STORAGE = 'utils.aws_custom_storage.ThumbStorage'

    AWS_STORAGE_BUCKET_NAME = aws.storage_bucket_name
    AWS_ACCESS_KEY_ID = aws.access_key_id
    AWS_SECRET_ACCESS_KEY = aws.secret_access_key

    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = True
    AWS_S3_ENDPOINT_URL = aws.s3_endpoint_url
    AWS_S3_REGION_NAME = 'ams3'
    AWS_S3_HOST = 'digitaloceanspaces.com'
    AWS_S3_CUSTOM_DOMAIN = (f'{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}'
                            '.digitaloceanspaces.com')
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}/media/'
    STATIC_URL = '/static/'
