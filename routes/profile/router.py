from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from server import database
from utils.helpers import generate_session_id, hash_password
from utils.decorators import check_user_credentials

profile_router = APIRouter(prefix='/profile')


class RequestBody(BaseModel):
    email: str = Field(min_length=3, max_length=50, pattern=r'^[\w._-]*@[\w]*.[a-zA-Z]{2,4}$')
    password: str = Field(min_length=3, max_length=50)


class ResponseBody(BaseModel):
    success: bool
    message: str


@profile_router.post('/register', responses={201: {'model': ResponseBody}, 409: {'model': ResponseBody}})
def register_account(body: RequestBody):
    user = database.get_user(body.email)
    if user:
        return JSONResponse(status_code=409,
                            content=ResponseBody(success=False, message='user already exist').dict())
    database.create_user(body.email, hash_password(body.password))
    return JSONResponse(status_code=201, content=ResponseBody(success=True, message='user created').dict())


@profile_router.post('/delete', responses={404: {'model': ResponseBody}, 401: {'model': ResponseBody}})
@check_user_credentials
def delete_account(body: RequestBody):
    database.delete_user(body.email)
    return ResponseBody(success=True, message='account deleted')


@profile_router.post('/login', responses={404: {'model': ResponseBody}, 401: {'model': ResponseBody}})
@check_user_credentials
def login(body: RequestBody):
    user = database.get_user(body.email)
    if user['session_id']:
        return JSONResponse(status_code=401, content=ResponseBody(success=False, message='user already logged in').dict())

    session_id = generate_session_id()
    database.set_session_id(body.email, session_id)

    response = JSONResponse(status_code=200, content=ResponseBody(success=True, message='logged in').dict())
    response.set_cookie(key='sessionId', value=session_id)
    return response


@profile_router.post('/logout', responses={404: {'model': ResponseBody}, 401: {'model': ResponseBody}})
@check_user_credentials
def logout(body: RequestBody):
    database.clear_session_id(body.email)
    return JSONResponse(status_code=200, content=ResponseBody(success=True, message='logged out').dict())
