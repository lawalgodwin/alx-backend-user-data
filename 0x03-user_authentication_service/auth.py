#!/usr/bin/env python3
"""A module containing password encryptionn functionality"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypt the given plain text password"""
    plain_password = password.encode('utf-8')
    encrypted_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())
    return encrypted_password
