import cgi, logging
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import memcache

from models import application

class AppHandler(webapp.RequestHandler):

	def get(self, appname):
		appurl_index = appname.find('/')

		if appurl_index != -1:
			appurl = appname[appurl_index:]
			appname = appname[:appurl_index]
		else:
			appurl = '/'

		app = memcache.get(appname)
		if app is None:
			# Get the Application object.
			q = db.GqlQuery("SELECT * FROM Application WHERE name = :1", appname)
			app = q.get()
			if not app:
				self.response.set_status(404) # Not Found
				self.response.out.write('Not Found')
				return
			memcache.set(key=appname, value=app, time=3600)

		url = 'http://' + app.host + ':' + app.port + appurl

		result = urlfetch.fetch(url)

		self.response.set_status(result.status_code)
		self.response.out.write(result.content)
