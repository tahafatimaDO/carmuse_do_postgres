from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vb7q_xxf5yp==!n9a*h)w6pmtv--@rsul@5h73t_zleqy7+1-b'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["DJANGO_ALLOWED_HOSTS", '*']
#ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", '*', "127.0.0.1").split(",")


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'mysite/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AWS_ACCESS_KEY_ID = '6R2WIBANZN4DYD5P3LTA'
AWS_SECRET_ACCESS_KEY = 'InP8ybNzDljW59HlsL8KxxQZVyaXrCOuVCJ96Hk/+6o'
AWS_STORAGE_BUCKET_NAME = 'bucket1'
AWS_S3_ENDPOINT_URL = 'https://sfo3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'taha_new'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mysite/static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#STATIC_URL = "/static/"
#STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
