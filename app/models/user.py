"""User model for the Code Analyzer application"""
from app import db

class User(db.Model):
    """Represents a registered user in the system"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        """Return user data as a dictionary"""
        return {
            "id": self.id,
            "email": self.email
        }
    