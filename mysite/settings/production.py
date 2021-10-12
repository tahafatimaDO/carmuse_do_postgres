from .base import *
from django.core.management.utils import get_random_secret_key

DEBUG = int(os.environ.get("DEBUG", default=1))
SECRET_KEY = 'django-insecure-wt2^elcpvn+a-aa7exnt92ak#l%yozhx+!el^^g1o&z246vyyb'
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

#ALLOWED_HOSTS = ["DJANGO_ALLOWED_HOSTS", "127.0.0.1"]
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# try:
#     from .local import *
# except ImportError:
#     pass

from .base import *