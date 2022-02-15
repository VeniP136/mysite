"""
cd /var/www/mysite
. ./bin/start_gunicorn.sh
"""
command = '/var/www/mysite/env/bin/gunicorn'
pythonpath = '/var/www/mysite/siteparser'
bind = '127.0.0.1:8001'
workers = 3
user = 'root'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=mysite.settings'