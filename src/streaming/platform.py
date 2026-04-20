"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from datetime import datetime, timedelta
from unittest import result
from streaming import sessions
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
        
    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:
        from datetime import datetime, timedelta

        premium_users = [u for u in self._users.values() if isinstance(u, PremiumUser)]
        if not premium_users:
            return 0.0

        cutoff = datetime.now() - timedelta(days=days)
        totals = []

        for user in premium_users:
            unique_tracks = {
                s.track for s in self._sessions
                if s.user is user and s.start_time >= cutoff
            }
        totals.append(len(unique_tracks))

        return sum(totals) / len(premium_users)
 
    def track_with_most_distinct_listeners(self) -> Track | None:
        if not self._sessions:
            return None
        listeners = {}
        for s in self._sessions:
            listeners.setdefault(s.track, set()).add(s.user)

        return max(listeners.items(), key=lambda x: len(x[1]))[0]

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:
        durations = {}
        for s in self._sessions:
            tname = type(s.user).__name__
            durations.setdefault(tname, []).append(
                (s.end_time - s.start_time).total_seconds()
            )

        results = []
        for tname, durs in durations.items():
            avg = sum(durs) / len(durs) if durs else 0.0
            results.append((tname, avg))

        for cls in (FreeUser, PremiumUser, FamilyAccountUser, FamilyMember):
            tname = cls.__name__
            if tname not in durations:
                results.append((tname, 0.0))

        return sorted(results, key=lambda x: x[1], reverse=True)

    def total_listening_time_underage_sub_users_minutes(self, age_threshold: int = 18) -> float:
        underage = {u for u in self._users.values() if isinstance(u, FamilyMember) and u.age < age_threshold}

        total_seconds = sum(
            (s.end_time - s.start_time).total_seconds()
            for s in self._sessions
            if s.user in underage
        )

        return total_seconds / 60.0

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:
        artist_time = {}  

        for s in self._sessions:
            track = s.track
            if isinstance(track, Song):
                artist_time.setdefault(track.artist, 0)
                artist_time[track.artist] += (s.end_time - s.start_time).total_seconds()

        ranked = sorted(
           [(artist, secs / 60.0) for artist, secs in artist_time.items()],
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:n]

    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:
        user = next((u for u in self._users.values() if u.id == user_id), None)
        if not user:
            return None

        genre_time = {} 

        sessions = [s for s in self._sessions if s.user is user]
        if not sessions:
            return None

        for s in sessions:
            if isinstance(s.track, Song):
                genre = s.track.genre
                genre_time.setdefault(genre, 0)
                genre_time[genre] += (s.end_time - s.start_time).total_seconds()

        if not genre_time:
            return None

        total = sum(genre_time.values())
        top_genre, top_time = max(genre_time.items(), key=lambda x: x[1])
        percentage = (top_time / total) * 100

        return (top_genre, percentage)

    def collaborative_playlists_with_many_artists(self, threshold: int = 3) -> list[CollaborativePlaylist]:
        result = []

        for pl in self._playlists:
            if isinstance(pl, CollaborativePlaylist):
                artists = {
                    track.artist
                    for track in pl.tracks
                    if isinstance(track, Song)
                }
            if len(artists) > threshold:
                result.append(pl)

        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:
        playlists = [p for p in self._playlists if isinstance(p, Playlist) and not isinstance(p, CollaborativePlaylist)]
        collabs = [p for p in self._playlists if isinstance(p, CollaborativePlaylist)]

        def avg(lst):
            return sum(len(p.tracks) for p in lst) / len(lst) if lst else 0.0

        return {
            "Playlist": avg(playlists),
            "CollaborativePlaylist": avg(collabs)
        }

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        results = []

        # Precompute user → listened tracks
        user_tracks = {u: set() for u in self._users.values()}
        for s in self._sessions:
            user_tracks[s.user].add(s.track)

        for user in self._users.values():
            completed = []

        for album in self._albums:
            if not album.tracks:
                continue  # ignore empty albums

            if set(album.tracks).issubset(user_tracks[user]):
                completed.append(album.title)

        if completed:
            results.append((user, completed))

        return results


