#!/usr/bin/env python3
"""Session authentication: Session-cookie management"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import timedelta, datetime


class SessionExpAuth(SessionAuth):
    """Session-cookie manager class"""
    def __init__(self) -> None:
        """Object initiliazer"""
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION', 0))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session ID"""
        session_id = super().create_session(user_id)
        session_key = session_id
        if not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_key] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retreive a user from its session ID"""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict['user_id']
        if session_dict is None or 'created_at' not in session_dict:
            return None
        session_duration = timedelta(seconds=self.session_duration)
        session_creation_time = session_dict['created_at']
        if session_creation_time + session_duration < datetime.now():
            return None
        return session_dict['user_id']
