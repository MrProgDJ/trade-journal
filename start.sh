#!/bin/bash
# Run migrations on startup
python manage.py migrate --noinput

# Create superuser if it doesn't exist
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@test.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Start gunicorn
exec gunicorn trade_journal.wsgi
