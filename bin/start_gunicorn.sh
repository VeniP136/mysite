#!/bin/bash
source /var/www/env/bin/activate
exec gunicorn -c /var/www/mysite/gunicorn_config.py mysite.wsgi