import logging
import uuid
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import requests
import urllib.parse

proxy_bp = Blueprint('proxy', __name__)

RAY_DASHBOARD_URL = 'http://localhost:8265'

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
    print("user_id: ", user_id)
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
        # Generate Job Id including the user_id at the end (uuid-user_id)
        job_id = str(uuid.uuid4()) + "-" + str(user_id)
        
        # override job_id set by the user if it exists, or set a custom one
        data = request.get_json()
        data.update({"job_id": job_id})

    if request.headers.get('Content-Type') == 'application/grpc':
        return proxy_grpc(url, headers)

    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=json.dumps(data) if data else None,
        cookies=request.cookies,
        allow_redirects=False,
    )

    # TODO: review this
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)

def user_has_access(user_id, path):
    # TODO: Implement access logic here
    return True

def proxy_grpc(url, headers):
    raise NotImplementedError("gRPC proxying is not yet implemented")