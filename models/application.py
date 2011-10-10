from google.appengine.ext import db

class Application(db.Model):
	person = db.UserProperty(required=True)
	name = db.StringProperty(default='')
	host = db.StringProperty(default='')
	port = db.StringProperty(default='')
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)
