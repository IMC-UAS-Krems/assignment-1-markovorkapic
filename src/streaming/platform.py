"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from streaming.albums import *
from streaming.artists import *
from streaming.playlists import *
from streaming.sessions import *
from streaming.tracks import *
from streaming.users import *

class StreamingPlatform:
    def __init__(self, name: str) -> None:
        self.name = name
        self._catalogue = {}
        self._users = {} 
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = []

    def add_track(self, track: "Track") -> None:
        self._catalogue[track.track_id] = track

    def add_user(self, user: "User") -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: "Artist") -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: "Album") -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: "Playlist") -> None:
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: "ListeningSession") -> None:
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str) -> "Track | None":
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str) -> "User | None":
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> "Artist | None":
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> "Album | None":
        return self._albums.get(album_id)

    def all_users(self) -> list:
        return list(self._users.values())

    def all_tracks(self) -> list:
        return list(self._catalogue.values())