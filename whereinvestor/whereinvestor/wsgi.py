"""
WSGI config for whereinvestor project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whereinvestor.settings')

application = get_wsgi_application()
