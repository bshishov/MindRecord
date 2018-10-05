import logging

from mindrecord.app import config
from mindrecord.utils import Request, Response, JsonResponse, HTTPError, Status
from mindrecord.urls import router

_logger = logging.getLogger(__name__)


def application(env, start_response):
    try:
        request = Request(env)
        response = router.dispatch(request)
        if not response or not isinstance(response, Response):
            raise HTTPError(Status.INTERNAL_SERVER_ERROR, message='Unable to respond')
        else:
            _logger.info('{} {} {}'.format(request.method, request.path, response.status_string))
    except HTTPError as http_error:
        response = JsonResponse({'message': http_error.message},
                                status_code=http_error.status_code,
                                status_message=http_error.status_message)
        _logger.error('{} {} {}: message={}'.format(
            env.get('REQUEST_METHOD', ''),
            env.get('PATH_INFO', ''),
            response.status_string,
            http_error.message))
    except Exception as error:
        response = JsonResponse({'message': 'Internal server error, please contact server administrator'}, status_code=500)
        _logger.error('{0} {1}'.format(env.get('PATH_INFO', ''), response.status_string))
        _logger.exception(error, exc_info=True)
    if response is not None:
        start_response(response.status_string, response.headers_as_tuples())
        for chunk in response:
            yield chunk


if __name__ == '__main__':
    import wsgiserver
    import argparse

    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host')
    parser.add_argument('--port', type=int, default=8081, help='Port')
    parser.add_argument('--name', type=str, default='MindRecord API', help='Server name')
    args = parser.parse_args()

    access_host = 'localhost' if args.host.endswith('.0') else args.host
    logging.info('Starting WSGI server on: http://{0}:{1}'.format(access_host, args.port))

    # Running
    server = wsgiserver.WSGIServer(application, host=args.host, port=args.port, server_name=args.name)
    server.start()
