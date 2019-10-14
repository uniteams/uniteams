import os

from uniteams.settings import *


ALLOWED_HOSTS.append('127.0.0.1')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
    }
}
