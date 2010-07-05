# player_management.py

import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import model

def get_current_player():
    user = users.get_current_user()
    player = model.Player.all().filter("user =", user).get()
    return player


def login_box_parameters():
    player = get_current_player()
    login_url = users.create_login_url("/validate_login")
    logout_url = users.create_logout_url("/")
    
    return { "player" : player,
             "login_url" : login_url,
             "logout_url" : logout_url }


class ValidateLogin(webapp.RequestHandler):
    template = os.path.join(os.path.dirname(__file__), "validate_login.html")
    
    def get(self):
        user = users.get_current_user()
        player = model.Player.all().filter("user =", user).get()
        
        if player:
            self.redirect("/")

        self.response.out.write(template.render(self.template, {"user" : user}))


class SignUpHandler(webapp.RequestHandler):
    template = os.path.join(os.path.dirname(__file__), "sign_up.html")
    
    def get(self):
        user = users.get_current_user()
        parameters = { "login_url" : users.create_login_url(self.request.url),
                       "user" : user,
                       "duplicate_nickname" : False }
        if user:
            dup_user = model.Player.all().filter("user =", user).get()
            parameters["duplicate_user"] = dup_user

        self.response.out.write(template.render(self.template, parameters))

    def post(self):
        user = users.get_current_user()
        nickname = self.request.get("nickname")
        
        if not user or not nickname:
            self.redirect(self.request.path)

        dup_user = model.Player.all().filter("user =", user).get()
        dup_nickname = model.Player.all().filter("nickname =", nickname).get()
        
        if dup_user or dup_nickname:
            parameters = { "user" : user,
                           "nickname" : nickname,
                           "duplicate_user" : dup_user,
                           "duplicate_nickname" : dup_nickname }
            self.response.out.write(template.render(self.template, parameters))
        else:
            player = model.Player(nickname = nickname, user = user)
            player.put()
            self.redirect("/")
