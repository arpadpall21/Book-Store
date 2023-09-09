from fastapi import APIRouter, Request


storage_router = APIRouter(prefix='/storage')


# @storage_router.get('/book/{title}', responses={404: {'model': ResponseBody}, 401: {'model': ResponseBody}})
# def get_book(request: Request, title: str):
#     return 'books'


# @storage_router.get('/books', responses={404: {'model': ResponseBody}, 401: {'model': ResponseBody}})
# def get_books(request: Request):
#     return 'books'


# @storage_router.get('/order/{title}', responses={404: {'model': ResponseBody}, 401: {'model': ResponseBody}})
# def order_book(request: Request):
#     pass
