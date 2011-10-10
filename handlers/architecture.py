from google.appengine.ext import webapp

import view

class ArchitectureHandler(webapp.RequestHandler):

	def get(self):
		page = view.Page()
		page.render(self, 'templates/page/architecture.html', {})
