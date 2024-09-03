#!/usr/bin/env python3
"""
This module is for manage the usr authAuthentication module for the API.
"""
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """
    THIS CLASS FOR THE USER AUTH PERPOSE
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """this function for the usr path checking.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        this func is for the auth info.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        this function for select the user data.
        """
        return None
