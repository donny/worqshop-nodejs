from google.appengine.ext import webapp

import view

class ReferenceHandler(webapp.RequestHandler):

	def get(self):
		page = view.Page()
		page.render(self, 'templates/page/reference.html', {})
