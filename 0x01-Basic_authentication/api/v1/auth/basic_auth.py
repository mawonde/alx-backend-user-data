#!/usr/bin/env python3
""" Basic Auth class
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Base64 Auth"""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic ") :]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode Base64 Auth"""
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            decoded_value = base64.b64decode(base64_authorization_header).decode(
                "utf-8"
            )
            return decoded_value
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract User Credentials"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return None, None

        # Split the decoded value into email and password using ":"
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Get User Object from Credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user in the database
        user_list = User.search({"email": user_email})

        if not user_list:
            return None

        user = user_list[0]

        # Check if the provided password is valid
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar("User"):
        """Retrieve User instance for a request"""
        if request is None or "Authorization" not in request.headers:
            return None

        authorization_header = request.headers["Authorization"]
        base64_header = self.extract_base64_authorization_header(authorization_header)

        if base64_header is None:
            return None

        decoded_value = self.decode_base64_authorization_header(base64_header)

        if decoded_value is None:
            return None

        email, password = self.extract_user_credentials(decoded_value)

        if email is None or password is None:
            return None

        return self.user_object_from_credentials(email, password)

