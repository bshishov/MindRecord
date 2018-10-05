import re

from mindrecord.utils.errors import HTTPError, Status


__all__ = ['Router']


class Router(object):
    routes = []

    def add_route(self, route_pattern: str, handler: callable):
        assert handler is not None, 'Handler should not be None'
        compiled_pattern = re.compile(route_pattern)
        self.routes.append((route_pattern, compiled_pattern, handler))

    def dispatch(self, request):
        request_path = request.path
        for pattern, compiled_pattern, handler in self.routes:
            match = compiled_pattern.match(request_path)
            if not match:
                continue

            kwargs = match.groupdict()  # type: dict
            return handler(request, **kwargs)

        # No route found
        raise HTTPError(Status.NOT_FOUND)
