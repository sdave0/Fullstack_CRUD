# user_routes.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from user_repository import UserRepository
from auth_routes import role_required

user_bp = Blueprint('user_bp', __name__)
user_repo = UserRepository(db)

@user_bp.route('/users', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    try:
        data = request.get_json()
        if 'name' not in data or 'email' not in data or 'password' not in data:
            return make_response(jsonify({'message': 'Name, email, and password are required'}), 400)
        role = data.get('role', 'user')
        print(f"Received role: {role}")
        new_user = user_repo.create_user(data['name'], data['email'], data['password'], role)
        return jsonify(new_user.json()), 201
    except Exception as e:
        return make_response(jsonify({'message': 'Error creating user', 'error': str(e)}), 500)

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = user_repo.get_all_users()
        users_data = [user.json() for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting users', 'error': str(e)}), 500)

@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = user_repo.get_user_by_id(id)
        if user:
            return jsonify(user.json()), 200
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting user', 'error': str(e)}), 500)

@user_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(id):
    try:
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return make_response(jsonify({'message': 'Name and email are required'}), 400)
        updated_user = user_repo.update_user(id, data['name'], data['email'])
        if updated_user:
            return jsonify({'message': 'User updated', 'user': updated_user.json()}), 200
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating user', 'error': str(e)}), 500)

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(id):
    try:
        success = user_repo.delete_user(id)
        if success:
            return jsonify({'message': 'User deleted'}), 200
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting user', 'error': str(e)}), 500)