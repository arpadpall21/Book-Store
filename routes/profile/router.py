from fastapi import APIRouter, BackgroundTasks, Request
from fastapi.responses import JSONResponse

from server import database
from utils.helpers import generate_session_id, hash_password
from utils.route_guard import check_user_credentials, check_session_id
from utils.email import send_welcome_email, send_farewell_email
from utils.constants import User
from routes.model import ProfileRequest, StatusResponse

profile_router = APIRouter(prefix='/profile')


@profile_router.post('/register', status_code=201, responses={201: {'model': StatusResponse},
                                                              409: {'model': StatusResponse}})
def register_account(body: ProfileRequest, background_tasks: BackgroundTasks):
    if database.add_user(User(email=body.email, password=hash_password(body.password))):
        background_tasks.add_task(send_welcome_email, body.email)
        return JSONResponse(status_code=201, content=StatusResponse(success=True, message='user created').model_dump())
    return JSONResponse(status_code=409,
                        content=StatusResponse(success=False, message='user already registered').model_dump())


@profile_router.post('/login', responses={200: {'model': StatusResponse},
                                          404: {'model': StatusResponse},
                                          401: {'model': StatusResponse}})
@check_user_credentials
def login(request: Request, body: ProfileRequest):
    if database.get_user_email_from_session_id(request.cookies.get('sessionId')):
        return JSONResponse(status_code=401,
                            content=StatusResponse(success=False, message='user already logged in').model_dump())

    new_session_id = generate_session_id()
    database.set_session_id(body.email, new_session_id)

    response = JSONResponse(status_code=200,
                            content=StatusResponse(success=True, message='user successfully logged in').model_dump())
    response.set_cookie(key='sessionId', value=new_session_id)
    return response


@profile_router.get('/logout', responses={200: {'model': StatusResponse},
                                          404: {'model': StatusResponse},
                                          401: {'model': StatusResponse}})
@check_session_id
def logout(request: Request):
    user_email = database.get_user_email_from_session_id(request.cookies.get('sessionId'))
    database.clear_session_id(user_email)

    response = JSONResponse(status_code=200,
                            content=StatusResponse(success=True, message='user successfully logged out').model_dump())
    response.delete_cookie(key='sessionId')
    return response


@profile_router.delete('/delete', responses={200: {'model': StatusResponse},
                                             404: {'model': StatusResponse},
                                             401: {'model': StatusResponse}})
@check_session_id
def delete_account(request: Request, background_tasks: BackgroundTasks):
    user_email = database.get_user_email_from_session_id(request.cookies.get('sessionId'))
    database.clear_session_id(user_email)
    database.delete_user(user_email)
    background_tasks.add_task(send_farewell_email, user_email)
    return StatusResponse(success=True, message='account deleted')
