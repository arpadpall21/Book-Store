from typing import List, Dict
from typing import Annotated
from collections import namedtuple

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from routes.model import StatusResponse
from utils.constants import Book
from utils.route_guard import check_session_id
from utils.email import send_book_order_email
from server import database
from routes.dependency import get_book_dependency, get_books_dependency, order_book_dependency
from routes.ws.router import admin_connection_manager

store_router = APIRouter(prefix='/store')


@store_router.get('/book/{title}', responses={200: {'model': Book},
                                              404: {'model': Dict},
                                              401: {'model': StatusResponse}})
@check_session_id
def get_book(params: Annotated[namedtuple, Depends(get_book_dependency)]):
    book = database.get_book(params.title.replace('_', ' '))
    if not book:
        return JSONResponse(status_code=404, content={})
    return JSONResponse(status_code=200, content=jsonable_encoder(book))


@store_router.get('/books', responses={200: {'model': List[Book]},
                                       404: {'model': List},
                                       401: {'model': StatusResponse}})
@check_session_id
def get_books(params: Annotated[namedtuple, Depends(get_books_dependency)]):
    books = database.get_books(params.skip,
                               params.skip + params.limit if params.limit else None)

    if not books:
        return JSONResponse(status_code=404, content=[])
    return JSONResponse(status_code=200, content=[jsonable_encoder(book) for book in books])


@store_router.get('/order_book/{title}', responses={200: {'model': StatusResponse},
                                                    404: {'model': StatusResponse},
                                                    401: {'model': StatusResponse}})
@check_session_id
def order_book(params: Annotated[namedtuple, Depends(order_book_dependency)]):
    book = database.get_book(params.title.replace('_', ' '))
    if not book:
        return JSONResponse(status_code=404, content=StatusResponse(success=False, message='book not found').dict())

    database.delete_book(book.title)
    email = database.get_user_email_from_session_id(params.request.cookies.get('sessionId'))
    params.background_tasks.add_task(send_book_order_email, email)
    params.background_tasks.add_task(admin_connection_manager.broadcast_book_order_to_admins, book)

    return JSONResponse(status_code=200,
                        content=StatusResponse(success=True, message=f'order placed for: {book.title}').dict())
