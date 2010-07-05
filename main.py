#!/usr/bin/env python


# Copyright (C) 2010  Steven Barker <steven.barker@gmail.com>

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import player_management

class MainHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), "main.html")
    def get(self):
        params = { "content" : "Nothing here yet!" }
        params.update(player_management.login_box_parameters())
        self.response.out.write(template.render(self.path, params))

def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/sign_up',
                                           player_management.SignUpHandler),
                                          ('/validate_login',
                                           player_management.ValidateLogin)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
