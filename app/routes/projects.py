from flask import Blueprint, jsonify, request

from app.models import db, Project

project_bp = Blueprint('project', __name__)

@project_bp.route('/api/projects/', methods=['GET'])
def get_projects():
    # Get all projects
    projects = Project.query.all()
    #project_list = [project.__dict__ for project in projects]

    return jsonify(projects), 200

@project_bp.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    # Get a specific project
    project = Project.query.get(project_id)
    return jsonify(project), 200

@project_bp.route('/api/projects/', methods=['POST'])
def create_project():
    data = request.get_json()
    new_project = Project(
        title=data['title'],
        description=data['description'],
        owner_id=data['owner_id'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify(message="Project created"), 201