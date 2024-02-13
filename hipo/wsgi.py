"""
WSGI config for hipo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hipo.settings")

application = get_wsgi_application()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_root = os.path.join(BASE_DIR, 'staticfiles')

# Wrap the Django application with WhiteNoise
application = WhiteNoise(application, root=static_root)
