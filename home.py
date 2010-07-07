# home.py

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import player_management

class HomeHandler(webapp.RequestHandler):
    def get(self):
        params = { "header" : player_management.login_box(),
                   "content" : "Nothing here yet!" }
        self.response.out.write(template.render("home.html", params))

