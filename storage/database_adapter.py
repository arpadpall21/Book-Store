from typing import Union, Optional, List
import itertools

from storage.database_types import User, Book
from utils.database_guard import check_connection


class BaseDatabaseAdapter:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def _check_connection(self):
        if not self.connected:
            raise ConnectionError('database is not connected')


class DatabaseAdapter(BaseDatabaseAdapter):
    def __init__(self):
        super().__init__()
        self.fake_database = {'users': {}, 'storage': {}, 'archive': {}}

    @check_connection
    def add_user(self, user: User) -> bool:
        if self.get_user(user.email):
            return False
        self.fake_database['users'][user.email] = user
        return True

    @check_connection
    def get_user(self, email: str) -> Optional[User]:
        return self.fake_database['users'].get(email)

    def get_user_email_by_session_id(self, session_id: str) -> Optional[User]:
        for user in self.fake_database['users'].values():
            if user.session_id == session_id:
                return user.email
        return None

    @check_connection
    def delete_user(self, email: str) -> bool:
        if self.get_user(email):
            del self.fake_database['users'][email]
            return True
        return False

    @check_connection
    def set_session_id(self, email: str, session_id: str) -> bool:
        if user := self.get_user(email):
            user.session_id = session_id
            return True
        return False

    @check_connection
    def get_session_id(self, email: str) -> Optional[str]:
        if user := self.get_user(email):
            return user.session_id
        return None

    @check_connection
    def clear_session_id(self, email: str) -> bool:
        if user := self.get_user(email):
            user.session_id = None
            return True
        return False

    @check_connection
    def add_book(self, book: Union[Book, List[Book]], archive: bool = False) -> bool:
        storage_type = 'archive' if archive else 'storage'
        if isinstance(book, list):
            for b in book:
                self.fake_database[storage_type][b.title] = b
            return True
        self.fake_database[storage_type][book.title] = book
        return True

    @check_connection
    def get_book(self, title: str, archive: bool = False) -> Optional[Book]:
        storage_type = 'archive' if archive else 'storage'
        return self.fake_database[storage_type].get(title)

    @check_connection
    def get_books(self, start: int = 0, end: int = None, archive: bool = False) -> list[Book]:
        storage_type = 'archive' if archive else 'storage'
        if start >= len(self.fake_database[storage_type]):
            return []

        result = []
        for title, book in dict(itertools.islice(self.fake_database[storage_type].items(), start, end)).items():
            result.append(book)
        return result

    @check_connection
    def delete_book(self, title: str, archive: bool = False) -> bool:
        storage_type = 'archive' if archive else 'storage'
        if self.fake_database[storage_type].get(title):
            del self.fake_database[storage_type][title]
            return True
        return False
