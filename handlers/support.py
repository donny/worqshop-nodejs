from google.appengine.ext import webapp

import view

class SupportHandler(webapp.RequestHandler):

	def get(self):
		page = view.Page()
		page.render(self, 'templates/page/support.html', {})
