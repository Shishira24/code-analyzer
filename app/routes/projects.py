from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.project import Project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    current_user_id = get_jwt_identity()
    projects = Project.query.filter_by(user_id=current_user_id).all()
    return jsonify({"projects": [p.to_dict() for p in projects]}), 200

@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"message": "Project name is required"}), 400

    project = Project(
        name=data['name'],
        repo_url=data.get('repo_url'),
        user_id=get_jwt_identity()
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({
        "message": "Project created successfully",
        "project": project.to_dict()
    }), 201

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    current_user_id = get_jwt_identity()
    project = Project.query.filter_by(
        id=project_id,
        user_id=current_user_id
    ).first()

    if not project:
        return jsonify({"message": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200