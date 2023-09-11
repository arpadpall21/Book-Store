import functools

from fastapi.responses import JSONResponse

from utils.helpers import hash_password


def check_user_credentials(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from server import database
        from routes.model import StatusResponse

        request = kwargs['body']
        stored_user = database.get_user(request.email)
        if not stored_user:
            return JSONResponse(status_code=404,
                                content=StatusResponse(success=False, message='user not found').dict())
        if stored_user.password != hash_password(request.password):
            return JSONResponse(status_code=401,
                                content=StatusResponse(success=False, message='wrong password').dict())
        return fn(*args, **kwargs)
    return wrapper


def check_user_logged_in(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from server import database
        from routes.model import StatusResponse

        request = kwargs['body']
        stored_user = database.get_user(request.email)
        if not stored_user.session_id:
            return JSONResponse(status_code=401, content=StatusResponse(success=False, message='not logged in').dict())
        return fn(*args, **kwargs)
    return wrapper


def check_session_id(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from server import database
        from routes.model import StatusResponse

        request = kwargs['request']
        if not database.get_user_email_by_session_id(request.cookies.get('sessionId')):
            return JSONResponse(status_code=401,
                                content=StatusResponse(success=False, message='invalid session id').dict())
        return fn(*args, **kwargs)
    return wrapper
