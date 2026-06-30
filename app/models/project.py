"""Project model for the Code Analyzer application"""
from datetime import datetime, timezone
from app import db

class Project(db.Model):
    """Represents a project owned by a registered user"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    repo_url = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        """Return project data as a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "repo_url": self.repo_url,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }
    