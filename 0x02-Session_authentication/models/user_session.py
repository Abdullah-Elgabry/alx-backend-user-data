#!/usr/bin/env python3
"""User session module.
"""
from models.base import Base


class UserSession(Base):
    """
    this is the user class.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        this is the inti def.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
