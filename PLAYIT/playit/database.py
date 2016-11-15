''' playit.database - SQLite Database '''

import logging
import sqlite3
import yaml

# Database

class Database(object):
    SQLITE_PATH = 'playit.db'
    YAML_PATH   = 'assets/yaml/playit.yaml'

    def __init__(self, data=YAML_PATH, path=SQLITE_PATH):
        self.logger = logging.getLogger()
        self.data   = data
        self.path   = path
        self.conn   = sqlite3.connect(self.path)

        self._create_tables()
        self._load_tables()

    def _create_tables(self):
        artists_sql = '''
        CREATE TABLE IF NOT EXISTS Artists (
            ArtistID    INTEGER NOT NULL,
            Name        TEXT    NOT NULL,
            Image       TEXT    NOT NULL,
            PRIMARY KEY (ArtistID)
        )
        '''

        albums_sql = '''
        CREATE TABLE IF NOT EXISTS Albums (
            ArtistID    INTEGER NOT NULL,
            AlbumID     INTEGER NOT NULL,
            Name        TEXT    NOT NULL,
            Image       TEXT    NOT NULL,
            PRIMARY KEY (AlbumID),
            FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
        )
        '''

        track_sql = '''
        CREATE TABLE IF NOT EXISTS Tracks (
            AlbumID     INTEGER NOT NULL,
            TrackID     INTEGER NOT NULL,
            Number      INTEGER NOT NULL,
            Name        TEXT NOT NULL,
            PRIMARY KEY (TrackID),
            FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID)
        )
        '''

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(artists_sql)
            cursor.execute(albums_sql)
            cursor.execute(track_sql)

    def _load_tables(self):
        artist_sql = 'INSERT OR REPLACE INTO Artists (ArtistId, Name, Image) VALUES (?, ?, ?)'
        album_sql  = 'INSERT OR REPLACE INTO Albums  (ArtistID, AlbumID, Name, Image) VALUES (?, ?, ?, ?)'
        track_sql  = 'INSERT OR REPLACE INTO Tracks  (AlbumID, TrackID, Number, Name) VALUES (?, ?, ?, ?)'

        with self.conn:
            cursor    = self.conn.cursor()
            artist_id = 1
            album_id  = 1
            track_id  = 1

            for artist in yaml.load(open(self.data)):
                cursor.execute(artist_sql, (artist_id, artist['name'], artist['image']))
                self.logger.debug('Added Artist: id={}, name={}'.format(artist_id, artist['name']))

                for album in artist['albums']:
                    cursor.execute(album_sql, (artist_id, album_id, album['name'], album['image']))
                    self.logger.debug('Added Album: id={}, name={}'.format(album_id, album['name']))

                    for track_number, track_name in enumerate(album['tracks']):
                        cursor.execute(track_sql, (album_id, track_id, track_number + 1, track_name))
                        self.logger.debug('Added Track: id={}, name={}'.format(track_id, track_name))
                        track_id += 1

                    album_id += 1

                artist_id += 1

    def artists(self, artist):
        artists_sql = 'SELECT ArtistID, Name, Image FROM Artists WHERE Name LIKE ? ORDER BY Name'
        with self.conn:
            cursor = self.conn.cursor()
            return cursor.execute(artists_sql, ('%{}%'.format(artist),))

    def artist(self, artist_id=None):
        artist_sql = '''
        SELECT      AlbumID, Name, Image
        FROM        Albums
        WHERE       ArtistID = ?
        ORDER BY    Name
        '''
        with self.conn:
            cursor = self.conn.cursor()
            return cursor.execute(artist_sql, (artist_id,))

    def albums(self, album):
        albums_sql = 'SELECT AlbumID, Name, Image FROM Albums WHERE Name LIKE ? ORDER BY Name'
        with self.conn:
            cursor = self.conn.cursor()
            return cursor.execute(albums_sql, ('%{}%'.format(album),))

    def album(self, album_id=None):
        album_sql = '''
        SELECT      TrackID, Number, Name
        FROM        Tracks
        WHERE       AlbumId = ?
        ORDER BY    Number
        '''
        with self.conn:
            cursor = self.conn.cursor()
            return cursor.execute(album_sql, (album_id,))

    def tracks(self, track):
        tracks_sql = '''
        SELECT      Tracks.TrackID, Tracks.Name, Image
        FROM        Tracks
        JOIN        Albums
        ON          Tracks.AlbumID = Albums.AlbumID
        WHERE       Tracks.Name LIKE ?
        ORDER BY    Tracks.Name
        '''
        with self.conn:
            cursor = self.conn.cursor()
            return cursor.execute(tracks_sql, ('%{}%'.format(track),))

    def track(self, track_id=None):
        track_sql = '''
        SELECT      TrackID, Artists.ArtistID, Artists.Name, Albums.AlbumID, Albums.Name, Number, Tracks.Name, Albums.Image
        FROM        Tracks
        JOIN        Albums
        ON          Albums.AlbumID = Tracks.AlbumID
        JOIN        Artists
        ON          Artists.ArtistID = Albums.ArtistID
        WHERE       TrackID = ?
        '''
        with self.conn:
            cursor = self.conn.cursor()
            return cursor.execute(track_sql, (track_id,)).fetchone()

    def song(self, track_id=None):
        # TODO: Select specific song information
	trackinfo=self.track(track_id)
	if trackinfo:
	    trackdict={
	    'trackName': trackinfo[6],
	    'artistName': trackinfo[2],
	    'albumName': trackinfo[4],
	    'albumImage': trackinfo[7],
	    'trackNumber': trackinfo[5],
	    'songURL': "/assets/mp3/{:04d}.mp3".format(int(track_id))
	    }
	return trackdict

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
