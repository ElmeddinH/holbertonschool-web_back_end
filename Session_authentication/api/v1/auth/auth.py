#!/usr/bin/env python3
"""
Auth module for API authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns the authorization header from a request"""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user from a request"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
