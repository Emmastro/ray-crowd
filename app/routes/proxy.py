from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

import requests
import urllib.parse

proxy_bp = Blueprint('proxy', __name__)

RAY_DASHBOARD_URL = 'http://localhost:8265'

@proxy_bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@jwt_required()
def proxy(path):
    user_id = get_jwt_identity()

    # Perform any user-specific checks here
    # For example, restrict access based on user roles or job ownership
    if not user_has_access(user_id, path):
        return Response('Forbidden', status=403)

    # Proxy the request to the Ray dashboard
    url = f"{RAY_DASHBOARD_URL}/{path}"
    headers = {key: value for key, value in request.headers if key != 'Host'}

    query_string = urllib.parse.urlencode(request.args)
    if query_string:
        url = f"{url}?{query_string}"

    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for name, value in response.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)

def user_has_access(user_id, path):
    # Implement your access logic here
    return True
