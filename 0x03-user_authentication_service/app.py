#!/usr/bin/env python3
"""A simple flask app set up"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """Home page route view"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def new_user() -> str:
    """new User registeration end-point view(handler)"""
    try:
        email = request.form['email']
        password = request.form['password']
        user = AUTH.register_user(email, password)
    except KeyError:
        abort(400)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """A fuction that handles session login"""
    try:
        email = request.form['email']
        password = request.form['password']
        is_valid_credentials = AUTH.valid_login(email, password)
    except KeyError:
        abort(400)
    if not is_valid_credentials:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """A function that handles session logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Return the profile of a user based on its session ID"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """A function that handles password reset"""
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({
        "email": "<{}>".format(email),
        "reset_token": "<{}>".format(reset_token)
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
