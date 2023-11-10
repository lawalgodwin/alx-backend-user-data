#!/usr/bin/env python3
"""A module containing login handler(view)"""

from api.v1.views import app_views
from flask import request, jsonify, session
from models.user import User
import os


@app_views.route('auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handle login request"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({ "error": "email missing" }), 400
    if password is None or password == '':
        return jsonify({ "error": "password missing" }), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({ "error": "no user found for this email" }), 404
    if not users:
        return jsonify({ "error": "no user found for this email" }), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    # create session_id for the user
    session_cookie = os.getenv('SESSION_NAME')
    session_id= auth.create_session(user.id)
    # set session cookie on response header
    # then send the user as response body in json string
    response = jsonify(user.to_json())
    response.set_cookie(session_cookie, session_id)
    return response
