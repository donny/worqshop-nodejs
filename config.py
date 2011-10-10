import os

APP_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# AWS Configuration
AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
AWS_HOSTS = ['', '']

NOTIFO_USER = ''
NOTIFO_SERVICE = ''
NOTIFO_KEY = ''

WORQ_CONFIG = {
	'config_name': 'worq_config',
	'max_app_site': 1000,
	'max_app_user': 3,
	'port_start' : 4000,
}

SETTINGS = {
	'title': 'Worqshop',
	'description': 'Worqshop',
	'author': 'Worqshop',
}
