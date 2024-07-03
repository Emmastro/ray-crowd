from flask import Blueprint, jsonify

version_bp = Blueprint('version', __name__)

@version_bp.route('/api/version', methods=['GET'])
def get_version():
    version_info = {
        "version": "1.0.0",
        "description": "Crowd Computing Platform API"
    }
    return jsonify(version_info), 200