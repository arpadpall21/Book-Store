from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

profile_router = APIRouter(prefix='/profile')


class RequestBody(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern='[a-zA-Z0-9]*')
    password: str = Field(min_length=3, max_length=50)


class ResponseBody(BaseModel):
    success: bool
    message: str


@profile_router.post(
    '/register_account',
    response_model=ResponseBody,
    )
def register_account(body: RequestBody):
    return ResponseBody(success=True, message='new account created')


@profile_router.post(
    '/delete_account',
    responses={
        200: {'model': ResponseBody},
        404: {'model': ResponseBody},
    })
def delete_account(body: RequestBody):
    return ResponseBody(success=True, message='account deleted')
    
    return JSONResponse(status_code=404, content=ResponseBody(success=False, message='account not found').dict())


@profile_router.post(
    '/login',
    responses={
        200: {'model': ResponseBody},
        404: {'model': ResponseBody},
    })
def login(body: RequestBody):
    return ResponseBody(success=True, message='successfully logged in')
    
    return JSONResponse(status_code=404, content=ResponseBody(success=False, message='account not found').dict())


@profile_router.post(
    '/logout',
    responses={
        200: {'model': ResponseBody},
        404: {'model': ResponseBody},
    })
def logout(body: RequestBody):
    return ResponseBody(success=True, message='successfully logged out')
    
    return JSONResponse(status_code=404, content=ResponseBody(success=False, message='account not found').dict())
