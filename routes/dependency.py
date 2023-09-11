from collections import namedtuple

from fastapi import Request, BackgroundTasks


async def get_book_dependency(request: Request, title: str) -> object:
    DependencyModel = namedtuple('DependencyModel', ['request', 'title'])
    return DependencyModel(request=request, title=title)


async def get_books_dependency(request: Request, skip: int = 0, limit: int = None):
    DependencyModel = namedtuple('DependencyModel', ['request', 'skip', 'limit'])
    return DependencyModel(request=request, skip=skip, limit=limit)


async def order_book_dependency(request: Request, title: str, background_tasks: BackgroundTasks):
    DependencyModel = namedtuple('DependencyModel', ['request', 'title', 'background_tasks'])
    return DependencyModel(request=request, title=title, background_tasks=background_tasks)
