#!/usr/bin/env python3
"""Now you will create a class to manage the API authentication.
"""
from flask import request, Request
from typing import List, TypeVar


class Auth:
    """API authentication manager"""
    def __init__(self) -> None:
        """Class constructor"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which routes don't need authentication"""
        if path is None or (excluded_paths is None) or (excluded_paths == []):
            return True

        for ex_path in excluded_paths:
            if ex_path in [path, path + '/']:
                return False
            elif ex_path.endswith('*') and path.startswith(ex_path[:-1]):
                return False
        return True

    def authorization_header(self, request: Request = None) -> str:
        """Request validation!
        Validate all requests to secure the API.
        """
        auth_header = request.headers.get('Authorization')
        if (request is None) or (auth_header is None):
            return None
        return auth_header

    def current_user(self, request: Request = None) -> TypeVar('User'):
        """request will be the Flask request object """
        return None
