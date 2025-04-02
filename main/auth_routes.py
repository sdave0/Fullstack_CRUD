
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from functools import wraps

auth_bp = Blueprint('auth_bp', __name__)

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.get(current_user)  # Fetch user from DB using ID
            if not user or user.role != role:
                return make_response(jsonify({'message': 'Access denied'}), 403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return make_response(jsonify({'message': 'Email and password are required'}), 400)
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return make_response(jsonify({'message': 'Invalid email or password'}), 401)
    # Use user ID as string identity, add role as additional claim
    access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
    return jsonify(access_token=access_token), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()  # Returns string ID
    return jsonify(logged_in_as=current_user_id), 200

@auth_bp.route('/admin-only', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_only():
    return jsonify(message='Welcome, admin!'), 200