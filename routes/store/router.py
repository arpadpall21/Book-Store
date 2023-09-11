from typing import List, Dict

from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from routes.model import StatusResponse
from storage.database_types import Book
from utils.route_guard import check_session_id
from server import database
from utils.email import send_book_order_email

store_router = APIRouter(prefix='/store')


@store_router.get('/book/{title}', responses={200: {'model': Book},
                                              404: {'model': Dict},
                                              401: {'model': StatusResponse}})
@check_session_id
def get_book(request: Request, title: str):
    book = database.get_book(title.replace('_', ' '))
    if not book:
        return JSONResponse(status_code=404, content={})
    return JSONResponse(status_code=200, content=jsonable_encoder(book))


@store_router.get('/books', responses={200: {'model': List[Book]},
                                       404: {'model': List},
                                       401: {'model': StatusResponse}})
@check_session_id
def get_books(request: Request, skip: int = 0, limit: int = None):
    if limit:
        limit = skip + limit
    books = database.get_books(skip, limit)
    if not books:
        return JSONResponse(status_code=404, content=[])
    return JSONResponse(status_code=200, content=jsonable_encoder([jsonable_encoder(book) for book in books]))


@store_router.get('/order_book/{title}', responses={200: {'model': StatusResponse},
                                                    404: {'model': StatusResponse},
                                                    401: {'model': StatusResponse}})
@check_session_id
def order_book(request: Request, title: str, background_tasks: BackgroundTasks):
    book = database.get_book(title.replace('_', ' '))
    if not book:
        return JSONResponse(status_code=404, content=StatusResponse(success=False, message='book not found').dict())

    database.delete_book(title.replace('_', ' '))   # book ordered -> remove from storage
    email = database.get_user_email_by_session_id(request.cookies.get('session_id'))
    background_tasks.add_task(send_book_order_email, email)
    return JSONResponse(status_code=200,
                        content=StatusResponse(success=True, message=f'order placed for: {book.title}').dict())
