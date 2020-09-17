#!/bin/sh

python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata ingredients.json
python manage.py collectstatic

exec "$@"