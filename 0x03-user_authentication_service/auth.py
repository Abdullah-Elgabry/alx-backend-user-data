#!/usr/bin/env python3
"""Module containing logic for handling user authentication tasks.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Convert a plaintext password into a hashed version.

    Utilizes bcrypt to securely hash a password.

    Args:
        password: The plaintext password to hash.

    Returns:
        A byte string representing the hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Create a new unique identifier string.

    Returns:
        A new UUID formatted as a string.
    """
    return str(uuid4())


class Auth:
    """Class that provides methods to authenticate users and manage sessions.
    """

    def __init__(self):
        """Constructor for initializing the Auth class.

        Sets up a new instance of the database interface.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user in the system.

        Checks if a user email exists and adds a new user if not.

        Args:
            email: The email address of the user to register.
            password: The user's password to be hashed and stored.

        Returns:
            The newly created user object.

        Raises:
            ValueError: If the user already exists in the database.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Verifies if the provided login credentials are correct.

        Args:
            email: The user's email address.
            password: The plaintext password provided for login.

        Returns:
            True if the login details are correct, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Generates a session ID for an authenticated user.

        Args:
            email: The email of the user to create a session for.

        Returns:
            A string containing the session ID, or None if user not found.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Fetches a user corresponding to a given session ID.

        Args:
            session_id: The session ID associated with the user.

        Returns:
            The user object or None if not found.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Terminates a user's session by removing their session ID.

        Args:
            user_id:the idf of the user whose session is to be terminated.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for the purpose of password recovery.

        Args:
            email: The email address of the user requesting password reset.

        Returns:
            A string representing the reset token.

        Raises:
            ValueError: If the user with the provided email does not exist.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password using the reset token.

        Args:
            reset_token: The token that verifies the password reset request.
            password: The new password to set for the user.

        Raises:
            ValueError: If the reset token is invalid or user not found.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
