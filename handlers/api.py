import cgi, logging
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import urlfetch

import uuid
import config
import notifo
import urllib
from models import developer, application, configuration

# Do not send requests to worqshop.com.
APPENGINE_ONLY = False

class APIHandler(webapp.RequestHandler):

	def post(self, action):
		self.response.headers['Content-Type'] = 'application/json'

		key = cgi.escape(self.request.get('key'))
		arg = cgi.escape(self.request.get('arg'))

		# Check for 'key'.
		if key == '':
			self.response.set_status(400) # Bad Request
			self.response.out.write('{"error": "Bad Request"}\n')
			return

		# Check for 'arg' and 'action' that does not require an argument.
		if action not in ['refresh_api_key'] and arg == '':
			self.response.set_status(400) # Bad Request
			self.response.out.write('{"error": "Bad Request"}\n')
			return

		# Get the Developer object.
		q = db.GqlQuery("SELECT * FROM Developer WHERE apikey = :1", key)
		dev_user = q.get()
		if not dev_user:
			self.response.set_status(401) # Unauthorized
			self.response.out.write('{"error": "Unauthorized"}\n')
			return

		# Check for the account status.
		if dev_user.enabled == False:
			self.response.set_status(401) # Unauthorized
			self.response.out.write('{"error": "Unauthorized"}\n')
			return

		# Perform the action.

		#######################################
		# Perform the refresh_api_key action. #
		#######################################
		if action == 'refresh_api_key':
			apikey = str(uuid.uuid4()).replace('-', '')
			dev_user.apikey = apikey
			dev_user.put()

			result = apikey

		#########################################
		# Perform the change_public_key action. #
		#########################################
		elif action == 'change_public_key':
			dev_user.publickey = arg
			dev_user.put()

			if not APPENGINE_ONLY:
				form_data = '{"action": "%s", "username": "%s", "publickey": "%s"}' % (action, dev_user.person.email(), dev_user.publickey)
				form_result = urlfetch.fetch(url='http://worqshop.com:8000', payload=form_data, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})

				if form_result.status_code != 200:
					self.response.set_status(500) # Internal Server Error
					self.response.out.write('{"error": "Internal Server Error"}\n')

			result = 'OK'

		##########################################
		# Perform the create_application action. #
		##########################################
		elif action == 'create_application':
			if arg in ['gitosis-admin']:
				self.response.set_status(400) # Bad Request
				self.response.out.write('{"error": "Bad Request"}\n')
				return

			q = db.GqlQuery("SELECT * FROM Application WHERE name = :1", arg)
			app = q.get()
			if app:
				self.response.set_status(400) # Bad Request
				self.response.out.write('{"error": "Bad Request"}\n')
				return
			
			appcount = dev_user.appcount
			if appcount >= config.WORQ_CONFIG['max_app_user']:
				self.response.set_status(400) # Bad Request
				self.response.out.write('{"error": "Bad Request"}\n')
				return

			w_conf = configuration.Configuration.get_or_insert(config.WORQ_CONFIG['config_name'])
			appcount = w_conf.appcount
			if appcount >= config.WORQ_CONFIG['max_app_site']:
				self.response.set_status(400) # Bad Request
				self.response.out.write('{"error": "Bad Request"}\n')
				return

			host = config.AWS_HOSTS[appcount % len(config.AWS_HOSTS)]
			port = str(config.WORQ_CONFIG['port_start'] + appcount)

			app = application.Application(person=dev_user.person, name=arg, host=host, port=port)
			app.put()
			notifo.send_notification(config.NOTIFO_SERVICE, config.NOTIFO_KEY, config.NOTIFO_USER, title='New Application', msg='%s %s' % (arg, dev_user.person.email()))

			dev_user.appcount += 1
			dev_user.put()

			w_conf.appcount += 1
			w_conf.put()

			if not APPENGINE_ONLY:
				form_data = '{"action": "%s", "username": "%s", "appname": "%s", "host": "%s", "port": "%s"}' % (action, dev_user.person.email(), app.name, host, port)
				form_result = urlfetch.fetch(url='http://worqshop.com:8000', payload=form_data, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})

				if form_result.status_code != 200:
					self.response.set_status(500) # Internal Server Error
					self.response.out.write('{"error": "Internal Server Error"}\n')

			result = port

		###########################################
		# Perform the destroy_application action. #
		###########################################
		elif action == 'destroy_application':
			q = db.GqlQuery("SELECT * FROM Application WHERE name = :1", arg)
			app = q.get()
			if not app:
				self.response.set_status(400) # Bad Request
				self.response.out.write('{"error": "Bad Request"}\n')
				return

			if not APPENGINE_ONLY:
				form_data = '{"action": "%s", "username": "%s", "appname": "%s"}' % (action, dev_user.person.email(), app.name)
				form_result = urlfetch.fetch(url='http://worqshop.com:8000', payload=form_data, method=urlfetch.POST, headers={'Content-Type': 'application/x-www-form-urlencoded'})

				if form_result.status_code != 200:
					self.response.set_status(500) # Internal Server Error
					self.response.out.write('{"error": "Internal Server Error"}\n')

			app.delete()

			result = 'OK'

		##################################
		# Cannot find an action handler. #
		##################################
		else:
			self.response.set_status(400) # Bad Request
			self.response.out.write('{"error": "Bad Request"}\n')
			return
			
		self.response.set_status(200) # OK
		self.response.out.write('{"result": "%s"}\n' % result)
