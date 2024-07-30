import logging
import os
import uuid
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import json
import requests
import urllib.parse

from app.models import Job, Project, db

proxy_bp = Blueprint('proxy', __name__)

RAY_DASHBOARD_URL = 'http://localhost:8265'
UPLOAD_FOLDER = "uploads" 

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


@proxy_bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@jwt_required()
def proxy(path):

    user_id = get_jwt_identity()

    if not user_has_access(user_id, path):
        return Response('Forbidden', status=403)

    # Proxy the request to the Ray dashboard
    url = f"{RAY_DASHBOARD_URL}/{path}"
    headers = {key: value for key, value in request.headers if key != 'Host'}
    headers.update({"user_id": str(user_id)})

    data = None

    if request.headers.get('Content-Type') == 'application/json':
        data = request.get_json()

    if path == "api/jobs/" and request.method == "POST":

        # if "file" in request.files:
        #     file = request.files["file"]
        #     filename = secure_filename(file.filename)
        #     file_path = os.path.join(UPLOAD_FOLDER, filename)
        #     file.save(file_path)
        #     # data.update({"file_path": file_path})

        # os.system(f"python {file_path}")

        # Generate Job Id including the user_id at the end (uuid-user_id)
        submission_id = str(uuid.uuid4()) + "-" + str(user_id)
        
        # override job_id set by the user if it exists, or set a custom one
        data.update({"submission_id": submission_id})

        # check if the project exists

        project_id = data.get("metadata").get("project_id")
        if project_id:
            # check if the project exists
            # change project_id type to uuid
            project_id = uuid.UUID(project_id)
            project = Project.query.get(project_id)
            if not project:
                return Response({"message": 'Project not found'}, status=404)

    if request.headers.get('Content-Type') == 'application/grpc':
        return proxy_grpc(url, headers)

    # query arguments for get
    query_args = urllib.parse.urlencode(request.args)
    if query_args:
        url += f"?{query_args}"

    headers['User-Agent'] = 'CustomAPIClient/1.0'

    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=json.dumps(data) if data else None,
        cookies=request.cookies,
        allow_redirects=False,
    )

    if path == "api/jobs/" and request.method == "POST":
        # create a job with the response
        job = Job(
            submission_id=submission_id,
            project_id=project_id,
        )
        db.session.add(job)
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)

def user_has_access(user_id, path):
    # TODO: Implement access logic here
    return True

def proxy_grpc(url, headers):
    raise NotImplementedError("gRPC proxying is not yet implemented")