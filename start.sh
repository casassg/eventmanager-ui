#!/bin/sh
python manage.py migrate --noinput
python manage.py loaddata events/start_query.json
gunicorn -b 0.0.0.0:80 eventmanager.wsgi --log-file -