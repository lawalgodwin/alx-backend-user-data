#!/usr/bin/env python3
"""Now you will create a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """API authentication manager"""
    def __init__(self) -> None:
        """Class constructor"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Docs strings"""
        return False
    
    def authorization_header(self, request=None) -> str:
        """request will be the Flask request object"""
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """request will be the Flask request object"""
        return None
