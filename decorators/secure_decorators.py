from functools import wraps

from fastapi import Request
from fastapi.responses import Response

from utils import auth_utils


def permission_required(permission_name: str):
    def _decorate(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if 'request' in kwargs:
                request: Request = kwargs['request']
            elif '_request' in kwargs:
                request: Request = kwargs['_request']
            else:
                raise Exception(f'Not request for decorator for func: {function}')

            user = auth_utils.get_user_by_request(request)

            if user is None or user.role_id is None:
                return Response(status_code=403)

            role = auth_utils.get_role_by_id(user.role_id)

            if not role.__dict__[permission_name]:
                return Response(status_code=403)

            return function(*args, **kwargs)

        return wrapper

    return _decorate


def verify_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'request' in kwargs:
            request: Request = kwargs['request']
        elif '_request' in kwargs:
            request: Request = kwargs['_request']
        else:
            raise Exception(f'Not request for decorator for func: {function}')

        user = auth_utils.get_user_by_request(request)

        if user is None or not user.is_verified:
            return Response(status_code=403)

        return function(*args, **kwargs)

    return wrapper
