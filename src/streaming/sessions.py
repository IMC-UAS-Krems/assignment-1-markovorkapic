"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
import datetime

class ListeningSession:
    def __init__(self, session_id: str, user: "User", tracks: "Track", timestamp: datetime, duration_listened_seconds: int):
        self.session_id = session_id  
        self.user = user
        self.tracks = tracks if tracks is not None else []
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds
    def duration_listened_minutes():
        ...
    
