"""
WSGI config for base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

import dotenv

dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Optional APM: no-op without NEW_RELIC_LICENSE_KEY / config. Must run before
# the Django application is loaded so instrumentation can wrap the app.
from base.newrelic import initialize_newrelic  # noqa: E402

initialize_newrelic()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings.prod')

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
