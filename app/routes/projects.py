from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models import db, Project

project_bp = Blueprint('project', __name__)

@project_bp.route('/api/projects/', methods=['GET'])
def get_projects():
    # Get all projects
    projects = Project.query.all()
    #project_list = [project.__dict__ for project in projects]

    return jsonify(projects), 200

@project_bp.route('/api/projects/<uuid:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    # Get a specific project
    project = Project.query.get(project_id)
    return jsonify(project), 200

@project_bp.route('/api/projects', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    print("data: ", data)
    # owner is current user
    user_id = get_jwt_identity()
    new_project = Project(
        title=data['title'],
        description=data['description'],
        owner_id=user_id,
        topic=data['topic'],
        is_public=data['is_public']
    )

    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project), 201