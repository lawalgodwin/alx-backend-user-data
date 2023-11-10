#!/usr/bin/env python3
"""Sessions in database"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session data persistence manager"""
    def __init__(self) -> None:
        """Class object initializer"""
        super().__init__()

    
    def create_session(self, user_id=None):
        """Create and store new instance of Usersession"""
        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = self.create_session(user_id)
        user_session.save()
        return user_session.session_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID
        from the request cookie
        """
        user = self.destroy_session(request)
        user.remove()
        user.save()
