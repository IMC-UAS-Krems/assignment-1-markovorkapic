"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""
from datetime import *

class Albums:
    def __init__(self, album_id:str, title:str, release_year:int, tracks: None, artist: "Artist"):
        self.album_id = album_id  
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = tracks if tracks is not None else []
    def add_track(track):
        ...
    def track_ids():
        ...
    def duration_seconds():
        ...
        