''' playit.web - Web Application '''

from playit.database import Database

import json
import logging
import socket
import socket
import sys

import tornado.ioloop
import tornado.web

# Application

class Application(tornado.web.Application):
    DEFAULT_PORT  = 9877
    TEMPLATE_PATH = 'assets/html'

    def __init__(self, port=DEFAULT_PORT):
	tornado.web.Application.__init__(self, debug=True, template_path=Application.TEMPLATE_PATH)
        self.logger   = logging.getLogger()
        self.database = Database()
        self.ioloop   = tornado.ioloop.IOLoop.instance()
        self.port     = port

        # TODO: Add Index, Album, Artist, and Track Handlers
        self.add_handlers('', [
            (r'/'           , IndexHandler),
            (r'/search'     , SearchHandler),
            (r'/artist/(.*)', ArtistHandler),
            (r'/album/(.*)' , AlbumHandler),
            (r'/track/(.*)' , TrackHandler),
            (r'/song/(.*)'  , SongHandler),
            (r'/assets/(.*)', tornado.web.StaticFileHandler, {'path': 'assets'}),


        ])

    def run(self):
        try:
            self.listen(self.port)
        except socket.error as e:
            self.logger.fatal('Unable to listen on {} = {}'.format(self.port, e))
            sys.exit(1)

        self.ioloop.start()

# Handlers

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('playit.html')

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO: Implement Index Handler
        query   = self.get_argument('query', '')
        table   = self.get_argument('table', '')
        results = []

        if table == 'Artists':
            results = self.application.database.artists(query)
        elif table == 'Albums':
            results = self.application.database.albums(query)
        elif table == 'Tracks':
            results = self.application.database.tracks(query)

        self.write(json.dumps({
            'render' : 'gallery',
            'prefix' : table[:-1],
            'results': list(results),
        }))

class ArtistHandler(tornado.web.RequestHandler):
    def get(self, artist_id=None):
        # TODO: Implement Artist Handler
        if not artist_id:
            self.write(json.dumps({
                'render' : 'gallery',
                'prefix' : 'Artist',
                'results': list(self.application.database.artists('')),
            }))
        else:
            self.write(json.dumps({
                'render' : 'gallery',
                'prefix' : 'Album',
                'results': list(self.application.database.artist(artist_id)),
            }))

class AlbumHandler(tornado.web.RequestHandler):
    def get(self, album_id=None):
        # TODO: Implement Album Handler
        if not album_id:
            self.write(json.dumps({
                'render' : 'gallery',
                'prefix' : 'Album',
                'results': list(self.application.database.albums('')),
            }))
        else:
            self.write(json.dumps({
                'render' : 'album',
                'results': list(self.application.database.album(album_id)),
            }))

class TrackHandler(tornado.web.RequestHandler):
    def get(self, track_id=None):
        # TODO: Implement Track Handler
        if not track_id:
            self.write(json.dumps({
                'render' : 'gallery',
                'prefix' : 'Track',
                'results': list(self.application.database.tracks('')),
            }))
        else:
            self.write(json.dumps({
                'render' : 'track',
                'results': list(self.application.database.track(track_id)),
            }))

class SongHandler(tornado.web.RequestHandler):
    def get(self, track_id=None):
        self.write(json.dumps({
            'song': self.application.database.song(track_id),
        }))

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
