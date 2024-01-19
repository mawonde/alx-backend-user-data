#!/usr/bin/env python3
""" Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
     """ Auth Class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require Authentication"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        excluded_paths = [p if p.endswith("/") else p + "/" for p in excluded_paths]

        if not path.endswith("/"):
            path += "/"

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Check Auth Header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar("User"):
        """Get Logged In User"""
        return None

