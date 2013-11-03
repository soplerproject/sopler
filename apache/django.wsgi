import os
import sys
 
path = '/var/www/sopler'
if path not in sys.path:
    sys.path.insert(0, '/var/www/sopler')
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'sopler.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
