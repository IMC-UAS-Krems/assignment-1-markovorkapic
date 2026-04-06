"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
import datetime
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



#Basic Methods
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
    

#Queries
    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        #if the timestamp of the session is between start and end -> add it to a total sum
        #later convert to minutes
        i = len(self._sessions)
        total = 0
        while i != 0:
            if self._sessions[i].timestamp >= start and self._sessions[i].timestamp <= end:
                total = self._sessions[i].duration_listened_seconds
            i -= 1
        return total / 60
    #not sure if this is correct, havent written a test for it yet
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        ...
    def track_with_most_distinct_listeners(self) -> Track | None:
        ...
    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        ...
    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        ...
    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        ...
    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        ...
    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        ...
    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        ...
    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        ...

#Need help with queries, kind of confusing.
#The basic methods were hard enough, Im not sure how to approach these