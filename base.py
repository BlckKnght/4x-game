# base.py

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import model

def get_current_player():
    user = users.get_current_user()
    player = model.Player.all().filter("user =", user).get()
    return player

class BaseHandler(webapp.RequestHandler):
    def base_params(self):
        return { "location" : "base",
                 "player" : get_current_player(),
                 "login_url" : users.create_login_url(self.request.url),
                 "logout_url" : users.create_logout_url(self.request.url),
                 "content" : "<p>I have nothing to say to you!</p>" }

    def get(self):
        self.response.out.write(template.render("base.html",
                                                self.base_params()))
