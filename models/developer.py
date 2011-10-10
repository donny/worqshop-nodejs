from google.appengine.ext import db

class Developer(db.Model):
	person = db.UserProperty(required=True)
	enabled = db.BooleanProperty(default=True)
	apikey = db.StringProperty(default='')
	publickey = db.TextProperty(default='')
	appcount = db.IntegerProperty(default=0)
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)
