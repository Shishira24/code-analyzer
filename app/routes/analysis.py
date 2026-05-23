"""Analysis routes for triggering and retrieving code analysis results"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.project import Project
from app.models.analysis import AnalysisResult
from app.services.analyzer import analyze_repo


analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/<int:project_id>/analyze', methods=['POST'])
@jwt_required()
def trigger_analysis(project_id):
    """Trigger code analysis for a project"""
    current_user_id = get_jwt_identity()

    project = Project.query.filter_by(
        id=project_id,
        user_id=current_user_id
    ).first()

    if not project:
        return jsonify({"message": "Project not found"}), 404

    if not project.repo_url:
        return jsonify({"message": "Project has no repo URL"}), 400

    try:
        results = analyze_repo(project.repo_url)
        analysis = AnalysisResult(
            project_id=project_id,
            complexity_score=results['complexity_score'],
            pylint_score=results['pylint_score'],
            pylint_warnings=results['pylint_warnings'],
            pylint_errors=results['pylint_errors']
        )
        db.session.add(analysis)
        db.session.commit()
        return jsonify({
            "message": "Analysis completed successfully",
            "results": analysis.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"message": f"Analysis failed: {str(e)}"}), 500


@analysis_bp.route('/<int:project_id>/results', methods=['GET'])
@jwt_required()
def get_results(project_id):
    """Get all analysis results for a project"""
    current_user_id = get_jwt_identity()

    project = Project.query.filter_by(
        id=project_id,
        user_id=current_user_id
    ).first()

    if not project:
        return jsonify({"message": "Project not found"}), 404

    results = AnalysisResult.query.filter_by(
        project_id=project_id
    ).order_by(AnalysisResult.analyzed_at.desc()).all()

    return jsonify({
        "project": project.name,
        "results": [r.to_dict() for r in results]
    }), 200
