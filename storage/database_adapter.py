from typing import Union, List

from storage.database_types import Book


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

    def add_user(self, email: str, password: bytes) -> bool:
        self._check_connection()
        if email not in self.fake_database['users']:
            self.fake_database['users'][email] = {'password': password, 'session_id': None}
            return True
        return False

    def delete_user(self, email: str) -> bool:
        self._check_connection()
        if email in self.fake_database['users']:
            del self.fake_database['users'][email]
            return True
        return False

    def get_user(self, email: str) -> dict:
        self._check_connection()
        if email in self.fake_database['users']:
            return self.fake_database['users'][email]
        return None

    def set_session_id(self, email: str, session_id: str) -> bool:
        self._check_connection()
        if email in self.fake_database['users']:
            self.fake_database['users'][email]['session_id'] = session_id
            return True
        return False

    def clear_session_id(self, email: str) -> bool:
        self._check_connection()
        if email in self.fake_database['users']:
            self.fake_database['users'][email]['session_id'] = None
            return True
        return False

    def add_book(self, book: Union[Book, List[Book]], archive: bool = False) -> bool:
        self._check_connection()
        storage_type = 'archive' if archive else 'storage'
        if isinstance(book, list):
            for b in book:
                self.fake_database[storage_type][b.title] = b
            return True
        self.fake_database[storage_type][book.title] = book
        return True

    def get_book(self, title: str, archive: bool = False) -> Book:
        self._check_connection()
        storage_type = 'archive' if archive else 'storage'
        return self.fake_database[storage_type].get(title)

    def delete_book(self, title: str, archive: bool = False) -> bool:
        self._check_connection()
        storage_type = 'archive' if archive else 'storage'
        if self.fake_database[storage_type].get(title):
            del self.fake_database[storage_type][title]
            return True
        return False
