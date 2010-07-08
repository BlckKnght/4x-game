#!/usr/bin/env python


# Copyright (C) 2010  Steven Barker <steven.barker@gmail.com>

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import home
import player_management
import base

def main():
    handlers = [('/', home.HomeHandler),
                ('/index.html', home.HomeHandler),
                ('/home', home.HomeHandler),
                ('/sign_up', player_management.SignUpHandler),
                ('/validate_login', player_management.ValidateLoginHandler),
                ('/base', base.BaseHandler)]
    application = webapp.WSGIApplication(handlers,
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
