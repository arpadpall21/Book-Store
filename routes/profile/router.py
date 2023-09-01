from random import randint

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from server import database
from utils.utils import generate_session_id

profile_router = APIRouter(prefix='/profile')


class RequestBody(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern='[a-zA-Z0-9]*')
    password: str = Field(min_length=3, max_length=50)


class ResponseBody(BaseModel):
    success: bool
    message: str


@profile_router.post('/register', responses={201: {'model': ResponseBody}, 409: {'model': ResponseBody}})
def register_account(body: RequestBody):
    if database.create_account(body.username, body.password):
        return JSONResponse(status_code=201, content=ResponseBody(success=True, message='account created').dict())
    return JSONResponse(status_code=409, content=ResponseBody(success=False, message='account already exist').dict())


@profile_router.post('/delete', responses={404: {'model': ResponseBody}})
def delete_account(body: RequestBody):
    if database.delete_account(body.username):
        return ResponseBody(success=True, message='account deleted')
    return JSONResponse(status_code=404, content=ResponseBody(success=False, message='account not found').dict())


@profile_router.post('/login', responses={404: {'model': ResponseBody}})
def login(body: RequestBody):
    account = database.get_account(body.username)
    if account and account['password'] == body.password:
        session_id = generate_session_id()
        database.set_session_id(body.username, session_id)

        response = JSONResponse(status_code=200, content=ResponseBody(success=True, message='logged in').dict())
        response.set_cookie(key='session_id', value=session_id)
        return response
    return JSONResponse(status_code=404, content=ResponseBody(success=False, message='account not found').dict())


@profile_router.post('/logout', responses={404: {'model': ResponseBody}})
def logout(body: RequestBody):
    account = database.get_account(body.username)
    if account and account['password'] == body.password:
        database.clear_session_id(body.username)
        return JSONResponse(status_code=200, content=ResponseBody(success=True, message='logged out').dict())
    return JSONResponse(status_code=404, content=ResponseBody(success=False, message='account not found').dict())
