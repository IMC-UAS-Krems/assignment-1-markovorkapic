"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

from datetime import *

class User:
    def __init__(self, user_id:str, name:str, age:int, sessions:None):
        self.user_id = user_id  
        self.name = name
        self.age = age
        self.sessions = sessions if sessions is not None else []
    def add_session(session):
        ... 
    def total_listening_seconds():
        ...
    def total_listening_minutes():
        ...
    def unique_tracks_listened():
        ...


class FamilyAccountUser(User):
    def __init__(self, user_id:str, name:str, age:int, sessions: None, sub_users: None):
        super().__init__(user_id, name, age, sessions)
        self.sub_users = sub_users if sub_users is not None else []
            
    def add_sub_users(sub_user):
        ...
    def all_members():
        ...
        
class FamilyMember(FamilyAccountUser):
    def __init__(self, user_id:str, name:str, age:int, sessions: None, sub_users: None, parent: "FamilyAccountUser"):
        super().__init__(user_id, name, age, sessions, sub_users)
        self.parent = parent


class FreeUser(User):
    def __init__(self, user_id:str, name:str, age:int, sessions: None, MAX_SKIPS_PER_HOUR: int = 6):
        super().__init__(user_id, name, age, sessions)
        self.MAX_SKIPS_PER_HOUR = MAX_SKIPS_PER_HOUR

class PremiumUser(User):
    def __init__(self, user_id:str, name:str, age:int, sessions: None, subscription_start):
        super().__init__(user_id, name, age, sessions)
        self.subscription_start = subscription_start