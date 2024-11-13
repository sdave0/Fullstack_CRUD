from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from user_repository import UserRepository
from models import db
from os import environ

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

# Initialize the repository
user_repo = UserRepository(db)

@app.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return make_response(jsonify({'message': 'Name and email are required'}), 400)

        new_user = user_repo.create_user(data['name'], data['email'])
        return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201
    except Exception as e:
        return make_response(jsonify({'message': 'Error creating user', 'error': str(e)}), 500)

@app.route('/api/flask/users', methods=['GET'])
def get_users():
    try:
        users = user_repo.get_all_users()
        users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting users', 'error': str(e)}), 500)

@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = user_repo.get_user_by_id(id)
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting user', 'error': str(e)}), 500)

@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()
        if 'name' not in data or 'email' not in data:
            return make_response(jsonify({'message': 'Name and email are required'}), 400)

        updated_user = user_repo.update_user(id, data['name'], data['email'])
        if updated_user:
            return make_response(jsonify({'message': 'User updated'}), 200)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating user', 'error': str(e)}), 500)

@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        success = user_repo.delete_user(id)
        if success:
            return make_response(jsonify({'message': 'User deleted'}), 200)
        return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting user', 'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True)
