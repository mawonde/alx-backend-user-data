#!/usr/bin/env python3
"""
Definition of class Auth for API Authentication
"""

import os
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Manages API authentication.

    Methods:
    - require_auth(path: str, excluded_paths: List[str]) -> bool:
      Determines whether a given path requires authentication or not.

    - authorization_header(request=None) -> str:
      Returns the authorization header from a request object.

    - current_user(request=None) -> TypeVar('User'):
      Returns a User instance from information in a request object.

    - session_cookie(request=None):
      Returns a cookie from a request.

    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not.

        Args:
            - path (str): Url path to be checked.
            - excluded_paths (List of str): List of paths that do not require authentication.

        Returns:
            - True if path is not in excluded_paths, else False.
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path) or path.startswith(i) or (i[-1] == "*" and path.startswith(i[:-1])):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object.

        Args:
            - request: Flask request object.

        Returns:
            - Authorization header value if present, else None.
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information in a request object.

        Args:
            - request: Flask request object.

        Returns:
            - User instance or None.
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie from a request.

        Args:
            - request: Flask request object.

        Returns:
            - Value of _my_session_id cookie from request object or None.
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)

