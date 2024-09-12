#!/usr/bin/env python3
"""Module defining the user data model for the authentication system.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Creating a base class for declarative models using SQLAlchemy
Base = declarative_base()


class User(Base):
    """
    Defines a User entity corresponding to the 'users' table in the database.
    This class maps to the user table and includes
    columns to store user credentials
    and session management data.
    """
    __tablename__ = "users"

    # Defining the columns for the users table
    id = Column(Integer, primary_key=True)  # Unique identifier for each user
    email = Column(String(250), nullable=False)  # User's email address
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
