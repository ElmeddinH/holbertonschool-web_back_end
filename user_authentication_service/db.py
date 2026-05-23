#!/usr/bin/env python3
"""DB module for database operations using SQLAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class that handles all database interactions"""

    def __init__(self) -> None:
        """Initialize a new DB instance and create tables"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object for database transactions"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the User object"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments matching column names"""
        if not kwargs:
            raise InvalidRequestError("No filter arguments provided")
        valid_columns = User.__table__.columns.keys()
        for key in kwargs:
            if key not in valid_columns:
                raise InvalidRequestError(f"Invalid column: {key}")
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found matching the criteria")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes by user_id"""
        user = self.find_user_by(id=user_id)
        valid_columns = User.__table__.columns.keys()
        for key in kwargs:
            if key not in valid_columns:
                raise ValueError(f"Invalid attribute: {key}")
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._session.commit()
