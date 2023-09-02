import functools

from fastapi.responses import JSONResponse

from utils.utils import hash_password


def check_user_credentials(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        from routes.profile.router import ResponseBody
        from server import database

        request = kwargs['body']
        stored_user = database.get_user(request.username)
        if not stored_user:
            return JSONResponse(status_code=404, content=ResponseBody(success=False, message='user not found').dict())
        if stored_user['password'] != hash_password(request.password):
            return JSONResponse(status_code=401, content=ResponseBody(success=False, message='wrong password').dict())
        return fn(*args, **kwargs)
    return wrapper
