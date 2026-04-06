"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

import datetime

class StreamingPlatform:
    def __init__(self, catalogue: None, users: None, artists: None, albums: None, playlists: None, sessions: None):
        self.catalogue = catalogue
        self.users = users 
        self.artists = artists
        self.albums = albums
        self.playlists = playlists
        self.sessions = sessions

    def add_track(track):
        ...
    def add_user(user):
        ...
    def add_artist(artist):
        ...
    def add_playlist(playlist):
        ...
    def record_session(session):
        ...
    def get_track(track_id):
        ...
    def get_user(user_id):
        ...
    def get_artist(artist_id):
        ...
    def get_album(album_id):
        ...
    def all_users():
        ...
    def all_tracks():
        ...