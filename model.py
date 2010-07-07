# model classes

from google.appengine.ext import db

class Player(db.Model):
    nickname    = db.StringProperty(required=True)
    user        = db.UserProperty(required=True)
    when_joined = db.DateTimeProperty(auto_now_add=True)


class Game(db.Model):
    name    = db.StringProperty(required=True)
    number_of_players = db.IntegerProperty(required=True)

    creator = db.ReferenceProperty(Player, required=True,
                                   collection_name="created_games")

    rules_version = db.IntegerProperty(default=1)
    when_created  = db.DateTimeProperty(auto_now_add=True)

    state = db.StringProperty(default="startup",
                              choices=["startup", "playing",
                                       "updating", "ended"])


class Race(db.Model): # this relates a player to a game
    game   = db.ReferenceProperty(Game,
                                  required=True,
                                  collection_name="races")
    player = db.ReferenceProperty(Player,
                                  required=True,
                                  collection_name="races")

    growth_rate = db.IntegerProperty(required=True)
    name        = db.StringProperty(required=True)
    adjective   = db.StringProperty(required=True)
    homeworld   = db.StringProperty(required=True)
