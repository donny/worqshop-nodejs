import os, sys, config

# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, config.APP_ROOT_DIR)
sys.path.insert(1, os.path.join(config.APP_ROOT_DIR, 'external'))

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from handlers import error, index, architecture, reference, support, app, api

def main():
	application = webapp.WSGIApplication([
											('/', index.IndexHandler),
											('/architecture', architecture.ArchitectureHandler),
											('/reference', reference.ReferenceHandler),
											('/support', support.SupportHandler),
											(r'/app/(.*)', app.AppHandler),
											(r'/api/(.*)', api.APIHandler),
											# If we make it this far then the page
											# we are looking for does not exist.
											('/.*', error.Error404Handler),
											], debug=True)
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
