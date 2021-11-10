import os
from settings import *  # noqa
import dj_database_url


SECRET_KEY = os.environ['PRODUCTION_KEY']
ALLOWED_HOSTS = ['herokuapp.com', ]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DATABASES['default'] = dj_database_url.config(conn_max_age=600)
DATABASES['default'] = dj_database_url.config(default=os.environ['DATABASE_URL'])

DEBUG = True
MIDDLEWARE_DEBUG = False


REDIRECT_TO = None
