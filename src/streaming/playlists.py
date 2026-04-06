"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self, playlist_id:str, name:str, owner: "User", tracks: None):
        self.playlist_id = playlist_id  
        self.name = name
        self.owner = owner
        self.tracks = tracks if tracks is not None else []
    def add_track(track):
        ...
    def remove_track(track):
        ...
    def total_duration_seconds():
        ...

class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id:str, name:str, owner: "User", tracks: None, contributors: None):
        super().__init__(playlist_id, name, owner, tracks)
        self.contributors = contributors if contributors is not None else []
    def add_contributor(User):
        ...
    def remove_contributor(User):
        ...