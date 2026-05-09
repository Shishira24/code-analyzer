from app import db
from datetime import datetime

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    complexity_score = db.Column(db.Float, nullable=True)
    pylint_score = db.Column(db.Float, nullable=True)
    pylint_warnings = db.Column(db.Integer, nullable=True)
    pylint_errors = db.Column(db.Integer, nullable=True)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "complexity_score": self.complexity_score,
            "pylint_score": self.pylint_score,
            "pylint_warnings": self.pylint_warnings,
            "pylint_errors": self.pylint_errors,
            "analyzed_at": self.analyzed_at.isoformat()
        }