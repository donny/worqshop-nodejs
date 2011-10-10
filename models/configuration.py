from google.appengine.ext import db

class Configuration(db.Model):
	appcount = db.IntegerProperty(default=0)
