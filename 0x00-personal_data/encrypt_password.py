#!/usr/bin/env python3
"""User passwords should NEVER be stored in plain text in databases.

Implement a hash_password function that expects one string
argument name password and returns a salted, hashed password,
which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw)
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypting passwords"""
    password_in_bytes_form = bytes(password, encoding='UTF-8')
    return bcrypt.hashpw(password_in_bytes_form, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check valid password (confirm the validity of a password)"""
    password_in_bytes_form = bytes(password, encoding='UTF-8')
    return bcrypt.checkpw(password_in_bytes_form, hashed_password)
