from django.core.management.utils import get_random_secret_key

from .common import *

DEBUG = False

SECRET_KEY = get_random_secret_key()

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
