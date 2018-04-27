# -*- coding: UTF-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from api import urls
from handlers.lobby_handler import GameLobby

from tornado.options import define, options
from pymongo import MongoClient

define("port", default=5000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        self.GameLobby = GameLobby()
        client = MongoClient('localhost', 27017)
        self.db = client['tangning']
        tornado.web.Application.__init__(self, urls, cookie_secret="Give me reason, but don't give me choice ",debug=True)



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()