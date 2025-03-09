# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from models import db


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:4000"]}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_ECHO'] = False
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")



db.init_app(app) 

jwt = JWTManager(app)

# Register blueprints
from auth_routes import auth_bp
from user_routes import user_bp

app.register_blueprint(auth_bp, url_prefix='/api/flask')
app.register_blueprint(user_bp, url_prefix='/api/flask')
from models import db, User
from app import app  # Import the Flask app instance
from werkzeug.security import generate_password_hash


def setup_database():
    '''
    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Check if an admin user already exists
        admin = User.query.filter_by(email="admin@admin.com").first()
        if not admin:
            print("Creating default admin user...")
            admin_user = User(
                name="Admin",
                email="admin@admin.com",
                role="admin",
                password_hash=generate_password_hash("admin")  # Hash password
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully.")
        else:
            print("Admin user already exists.")
'''
if __name__ == "__main__":
    setup_database()  # Ensure DB setup before starting
    app.run(debug=True, host='0.0.0.0', port=4000)
