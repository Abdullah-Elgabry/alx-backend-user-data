#!/usr/bin/env python3
"""
Database operations module utilizing SQLAlchemy for ORM management.
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from user import Base, User


class DB:
    """
    Class to manage the database actions for user-related data.
    """

    def __init__(self) -> None:
        """
        Constructor to establish a new instance of the DB class.
        Sets up the database engine and initializes the schema.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Property to create and return a session object.
        Caches the session object for reuse to avoid re-instantiation.
        Returns:
            An active database session instance.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method to insert a new user into the database.

        Args:
            email: The email address of the new user.
            hashed_password: The hashed password of the new user.

        Returns:
            The newly created user object, or None if failed.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Method to search for a user by specified attribute(s).

        Args:
            kwargs: Arbitrary keyword arguments representing user attributes.

        Returns:
            The user object that matches the search criteria.

        Raises:
            InvalidRequestError: If the attribute isn't found in the User class
            NoResultFound: If no user matches the search criteria.
        """
        fields, values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*fields).in_([tuple(values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method to modify a user's attributes based on user ID.

        Args:
            user_id: The unique identifier of the user to be updated.
            kwargs: Arbitrary arguments representing the new attributes.

        Raises:
            ValueError: If the attribute does not exist in the User class.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_source = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_source[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_source,
            synchronize_session=False,
        )
        self._session.commit()
