from models import db, User
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy here

class UserRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_user(self, name: str, email: str) -> User:
        try:
            new_user = User(name=name, email=email)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error creating user: {str(e)}")

    def get_user_by_id(self, user_id: int) -> User:
        try:
            return User.query.filter_by(id=user_id).first()
        except Exception as e:
            raise Exception(f"Error fetching user by ID: {str(e)}")

    def get_all_users(self) -> list:
        try:
            return User.query.all()
        except Exception as e:
            raise Exception(f"Error fetching all users: {str(e)}")

    def update_user(self, user_id: int, name: str, email: str) -> User:
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                user.name = name
                user.email = email
                self.db.session.commit()
                return user
            return None
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error updating user: {str(e)}")

    def delete_user(self, user_id: int) -> bool:
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                self.db.session.delete(user)
                self.db.session.commit()
                return True
            return False
        except Exception as e:
            self.db.session.rollback()
            raise Exception(f"Error deleting user: {str(e)}")
