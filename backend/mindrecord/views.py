import logging

from mindrecord.utils import Request, JsonResponse, Status, HTTPError, Response, allow_methods, FileResponse, \
    allow_cors
from mindrecord.app import config
from mindrecord.auth import *


logger = logging.getLogger(__name__)


@allow_cors()
@allow_methods('GET')
def home_view(request: Request):
    return JsonResponse({'message': 'Hello'})


@allow_cors()
@allow_methods('GET', 'POST', 'DELETE')
def auth_view(request: Request):
    if request.method == 'POST':
        # Create new token
        return JsonResponse({'token': create_access_token(User.create_anonymous())})
    if request.method == 'DELETE':
        # TODO: Implement
        raise HTTPError(Status.NOT_IMPLEMENTED)

@allow_cors()
@requires_auth()
@allow_methods('GET', 'PUT')
def user_view(request):
    user = get_user_from_request(request)
    return JsonResponse({'id': user.id, 'role': user.role})

