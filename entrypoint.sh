#!/bin/sh
echo 'running migration'
/usr/local/bin/python3 manage.py migrate
/usr/local/bin/python3 manage.py collectstatic --noinput
exec "$@"
