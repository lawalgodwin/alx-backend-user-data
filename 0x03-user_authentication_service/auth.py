#!/usr/bin/env python3
"""A module containing password encryptionn functionality"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Encrypt the given plain text password"""
    plain_password = password.encode('utf-8')
    encrypted_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())
    return encrypted_password


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Class initializer"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user with the specified email and password"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            password_hash = _hash_password(password)

            new_user: User = self._db.add_user(email, password_hash)
            return new_user
        else:
            raise ValueError('User <{}> already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Generate session ID for a user and store it in the database"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = _generate_uuid()
        self._db.update_user(user.id)
        return user.session_id
