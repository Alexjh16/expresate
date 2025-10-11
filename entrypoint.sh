#!/bin/sh
set -e

# Wait for dependent services if needed (simple loop, optional improvement: use wait-for-it)
# Apply DB migrations
python manage.py migrate --noinput
# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn
exec gunicorn expresate.wsgi:application --bind 0.0.0.0:8000 --workers 3
