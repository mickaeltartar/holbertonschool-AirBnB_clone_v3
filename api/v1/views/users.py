#!/usr/bin/python3
"""user_management.py"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


# Route definition for retrieving all users
# ============================================================================

@app_views.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def get_users():

    """Retrieves a list of all User objects in the system"""

    users = storage.all(User).values()
    list_users = [user.to_dict() for user in users]
    return jsonify(list_users)


# Route definition for retrieving a specific user
# ============================================================================
@app_views.route('/api/v1/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a specific User object based on its ID."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


# Route definition for deleting a user
# ============================================================================
@app_views.route('/api/v1/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a specific User object based on its ID."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


# Route definition for creating a new user
# ============================================================================
@app_views.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def post_user():
   """
    Creates a new User object in the system"""
   user_data = request.get_json()
   if not user_data:
        return make_response(jsonify({'error': 'Missing JSON data'}), 400)
   if 'email' not in user_data:
        return make_response(jsonify({'error': 'Email is required'}), 400)
   if 'password' not in user_data:
        return make_response(jsonify({'error': 'Password is required'}), 400)
   new_user = User(**user_data)
   new_user.save()
   return make_response(jsonify(new_user.to_dict()), 201)


# Route definition for updating a user
# ============================================================================
@app_views.route('/api/v1/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """
    Updates an existing User object in the system."""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        return make_response(jsonify({'error': 'Missing JSON data'}), 400)
    for field, value in user_data.items():
        if field not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, field, value)
    user.save()
    return jsonify(user.to_dict())
