#!/usr/bin/env python3
"""A simple flask app set up"""

from flask import Flask, jsonify, request, abort
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
        return jsonify({"email": user.email, "message": "user created"}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
