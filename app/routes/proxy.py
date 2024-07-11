import logging
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

import grpc
import requests
import urllib.parse
from ray.core.generated import gcs_service_pb2_grpc

proxy_bp = Blueprint('proxy', __name__)

RAY_DASHBOARD_URL = 'http://localhost:8265'
RAY_GRPC_URL = 'localhost:9000'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


# Define a function to forward GRPC requests
def forward_grpc_request(method, request_data, metadata):
    channel = grpc.insecure_channel(RAY_DASHBOARD_URL)
    stub = grpc.dynamic_stub.DynamicStub(channel)
    grpc_method = stub.unary_unary(method)
    grpc_response = grpc_method(request_data, metadata=metadata)
    return grpc_response


def filter_grpc_metadata(headers):
    """
    Filter and convert headers to be valid for gRPC metadata.
    gRPC metadata keys must be lowercase and cannot include certain HTTP headers.
    """
    valid_metadata = {}
    for key, value in headers.items():
        # Convert key to lowercase
        lower_key = key.lower()
        # Filter out invalid keys
        if lower_key in ['host', 'content-length', 'content-encoding', 'transfer-encoding', 'connection', 'te', 'grpc-accept-encoding', 'grpc-timeout', 'user-agent']:
            continue
        valid_metadata[lower_key] = value
    return valid_metadata

@proxy_bp.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
# @jwt_required()
def proxy(path):

    # user_id = get_jwt_identity()

    # Perform any user-specific checks here
    # For example, restrict access based on user roles or job ownership
    # if not user_has_access(user_id, path):
    #     return Response('Forbidden', status=403)

    # Proxy the request to the Ray dashboard
    url = f"{RAY_DASHBOARD_URL}/{path}"
    headers = {key: value for key, value in request.headers if key != 'Host'}
    
    query_string = urllib.parse.urlencode(request.args)
    if query_string:
        url = f"{url}?{query_string}"

    # if request.headers.get('Content-Type') == 'application/grpc':

    #     # Setup GRPC channel
    #     channel = grpc.insecure_channel(RAY_GRPC_URL)
    #     stub = gcs_service_pb2_grpc.NodeInfoGcsServiceStub(channel)
    #     grpc_response = stub.GetClusterId
    #     # Prepare the metadata from headers
    #     metadata = [(key.lower(), value) for key, value in headers.items() if key.lower() not in ['host', 'content-length', 'content-encoding', 'transfer-encoding', 'connection']]

    #     # Prepare the request data
    #     #request_data = request.get_data()

    #     # Determine the method name
    #     #


    #     try:
    #         # Using lower-level grpc API to forward the request
    #         #stub = channel.unary_unary(method)
    #         #print("stub: ", stub)
    #         #grpc_response = stub(request_data, metadata=metadata)
    #         response_content = grpc_response
    #         print("grpc_response: ", grpc_response)
    #         response_status = 200
    #         grpc_headers = []

    #         logger.info(f"GRPC Response from {url}: {response_status}")
    #         return Response(response_content, response_status, grpc_headers)
    #     except grpc.RpcError as e:
    #         logger.error(f"GRPC request failed: {e}")
    #         return Response(f"GRPC request failed: {e}", status=500)
    

    logger.info(f" -------->>>>>> Proxying request to {url} with method {request.method} headers {headers} data {request.get_data()} cookies {request.cookies}")
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

    logger.info(f" <<<<<<-------- Response from {url}: {response.status_code}")
    # log response content
    # logger.info("response content" , response.content)
    return Response(response.content, response.status_code, headers)

def user_has_access(user_id, path):
    # Implement your access logic here
    return True
