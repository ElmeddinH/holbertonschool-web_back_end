#!/usr/bin/env python3
"""Auth module that provides all authentication logic for the application"""
import bcrypt
import uuid
from typing import Union, Optional

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a plain-text password string using bcrypt with a random salt and return bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate and return a string representation of a new random UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self) -> None:
        """Initialize a new Auth instance with a DB connection"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with email and password; raises ValueError if user exists"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed)

    def valid_login(self, email: str, password: str) -> bool:
        """Check if the provided email and password are valid login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password
            )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session ID for the user with the given email and store it"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Return the User object corresponding to the given session ID or None"""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session of the user with the given user_id by setting it to None"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a password reset token for the user; raises ValueError if not found"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError("User {} not found".format(email))

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using a valid reset token; raises ValueError if token invalid"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(
                user.id, hashed_password=hashed, reset_token=None
            )
        except NoResultFound:
            raise ValueError("Invalid reset token")
