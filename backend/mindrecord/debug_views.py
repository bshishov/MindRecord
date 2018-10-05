import logging
import os

from mindrecord.utils import Request, JsonResponse, Status, HTTPError, Response, allow_methods, FileResponse, allow_cors
from mindrecord.app import config
from mindrecord.auth import *


logger = logging.getLogger(__name__)


@allow_cors()
@requires_auth()
def private_view(request):
    user = get_user_from_request(request)
    return JsonResponse({
        'message': 'private section',
        'user': {'role': user.role, 'id': user.id}
    })


@allow_cors()
@allow_methods('GET')
def get_param_view(request, id):
    return JsonResponse({'message': 'test', 'id': id})


@allow_cors()
@allow_methods('POST')
def upload_view(request):
    print(request.data)
    return JsonResponse({'message': 'upload test'})


@allow_cors()
@allow_methods('GET')
def download_view(request):
    path = request.data.get('path', None)
    if not path or not os.path.exists(path):
        raise HTTPError(Status.NOT_FOUND)
    return FileResponse(path[0], chunk_size=4096)
