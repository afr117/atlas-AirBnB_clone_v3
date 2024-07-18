#!/usr/bin/python3
"""User object view"""
from flask import Flask, jsonify, make_response, request, abort
from models.user import User
from models import storage
from api.v1.views import app_views

@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieve the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Retrieve a User object by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Delete a User object by user_id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return {}, 200

@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Create a new User object"""
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    data = request.get_json()
    if "email" not in data:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in data:
        return make_response(jsonify({"error": "Missing password"}), 400)
    
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Update a User object by user_id"""
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    user.save()
    storage.save()
    return jsonify(user.to_dict())
