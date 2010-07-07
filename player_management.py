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


def signup_required(func):
    """Return a wrapper function that checks that the user has a nickname.

    This function should be used as a decorator on "get" request handler
    methods, like this:

    @signup_required
    def get(self):
        ...
    """
    def get(self):
        user = users.get_current_user()
        player = model.Player.all().filter("user =", user).get()
        if player:
            return func(self)
        else:
            params = { "login_url" : users.create_login_url(self.request.url),
                       "user" : user }
            self.response.out.write(template.render("signup_required.html",
                                                    params))
    return get


def login_box_parameters():
    player = get_current_player()
    login_url = users.create_login_url("/validate_login")
    logout_url = users.create_logout_url("/")
    
    return { "player" : player,
             "login_url" : login_url,
             "logout_url" : logout_url }


class ValidateLoginHandler(webapp.RequestHandler):
    @signup_required
    def get(self):
        self.redirect("/")


class SignUpHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        parameters = { "login_url" : users.create_login_url(self.request.url),
                       "user" : user,
                       "duplicate_nickname" : False }
        if user:
            dup_user = model.Player.all().filter("user =", user).get()
            parameters["duplicate_user"] = dup_user

        self.response.out.write(template.render("sign_up.html", parameters))

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
            self.response.out.write(template.render("sign_up.html", parameters))
        else:
            player = model.Player(nickname = nickname, user = user)
            player.put()
            self.redirect("/")
