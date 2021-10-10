from .base import *

DEBUG = True # int(os.environ.get("DEBUG", default=1))
SECRET_KEY = 'django-insecure-wt2^elcpvn+a-aa7exnt92ak#l%yozhx+!el^^g1o&z246vyyb'
ALLOWED_HOSTS = ['*']

# try:
#     from .local import *
# except ImportError:
#     pass

from .base import *