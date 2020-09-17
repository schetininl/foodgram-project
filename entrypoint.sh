#!/bin/sh

python manage.py collectstatic

exec "$@"