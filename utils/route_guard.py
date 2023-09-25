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
                                content=StatusResponse(success=False, message='user not found').model_dump())
        if stored_user.password != hash_password(request.password):
            return JSONResponse(status_code=401,
                                content=StatusResponse(success=False, message='wrong password').model_dump())
        return fn(*args, **kwargs)
    return wrapper


def check_session_id(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from server import database
        from routes.model import StatusResponse

        session_id = (kwargs.get('request').cookies.get('sessionId')
                      if kwargs.get('request')
                      else kwargs.get('params').request.cookies.get('sessionId'))
        if not database.get_user_email_from_session_id(session_id):
            return JSONResponse(status_code=401,
                                content=StatusResponse(success=False,
                                                       message='invalid session id (user not logged in)').model_dump())
        return fn(*args, **kwargs)
    return wrapper
