"""
ASGI config for trade_journal project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_journal.settings')

application = get_asgi_application()
