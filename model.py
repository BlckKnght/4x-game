# model classes

from google.appengine.ext import db

class Player(db.Model):
    nickname    = db.StringProperty(required=True)
    user        = db.UserProperty(required=True)
    when_joined = db.DateTimeProperty(auto_now_add=True)
