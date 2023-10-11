from functools import wraps

from fastapi import Request

from fastapi.responses import Response

from utils import auth_utils


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'request' in kwargs:
            request: Request = kwargs['request']
        elif '_request' in kwargs:
            request: Request = kwargs['_request']
        else:
            raise Exception(f'Not request for decorator for func: {func}')

        user = auth_utils.get_user_by_request(request)

        if user is None:
            # Not authed
            return Response(status_code=403)

        if not user.is_active:
            return Response(status_code=403)

        return func(*args, **kwargs)

    return wrapper


def not_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'request' in kwargs:
            request: Request = kwargs['request']
        elif '_request' in kwargs:
            request: Request = kwargs['_request']
        else:
            raise Exception(f'Not request for decorator for func: {func}')

        user = auth_utils.get_user_by_request(request)

        if user is not None:
            return Response(status_code=403)

        return func(*args, **kwargs)

    return wrapper
