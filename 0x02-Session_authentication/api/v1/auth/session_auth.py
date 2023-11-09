#!/usr/bin/env python3
"""A module containing session authentication manager class"""

from api.v1.auth.auth import Auth
from uuid import uuid4
import os
from models.user import User


class SessionAuth(Auth):
    """Session manager class"""
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """class object initializer"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id
        user_id can now be retreived nased on the Session ID"""
        if user_id is None or (not isinstance(user_id, str)):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retreive user_id based on its Session ID in the session store"""
        if session_id is None or (not isinstance(session_id, str)):
            return None
        user_id = SessionAuth.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """Use Session ID for identifying a User"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user
