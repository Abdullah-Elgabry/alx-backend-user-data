#!/usr/bin/env python3
"""
This is an app for pass chiper.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    this function will # the pass.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    this fuction will search for the right ## pass
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
