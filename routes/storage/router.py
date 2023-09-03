from fastapi import APIRouter


storage_router = APIRouter(prefix='/storage')


@storage_router.post('/books')
def get_books():
    return 'books'


@storage_router.post('/book')
def get_book():
    return 'books'
