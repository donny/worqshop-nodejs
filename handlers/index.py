import uuid
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db

import view
import config
import notifo
from models import developer

class IndexHandler(webapp.RequestHandler):

	def get(self):
		user = users.get_current_user()

		if user:
			q = db.GqlQuery("SELECT * FROM Developer WHERE person = :1", user)
			dev_user = q.get()
			if not dev_user:
				apikey = str(uuid.uuid4()).replace('-', '')
				dev_user = developer.Developer(person=user, apikey=apikey)
				dev_user.put()
				notifo.send_notification(config.NOTIFO_SERVICE, config.NOTIFO_KEY, config.NOTIFO_USER, title='New User', msg=user.email())

			q = db.GqlQuery("SELECT * FROM Application WHERE person = :1", user)
			dev_user_apps = q.fetch(config.WORQ_CONFIG['max_app_user'])

			values = {'dev_user': dev_user, 'dev_user_apps': dev_user_apps}
		else:
			values = {}

		page = view.Page()
		page.render(self, 'templates/page/index.html', values)
