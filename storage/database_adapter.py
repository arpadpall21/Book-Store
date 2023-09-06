from datetime import date


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

    def create_user(self, email: str, password: bytes) -> bool:
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

    def get_user(self, email: str) -> dict | None:
        self._check_connection()
        if email in self.fake_database['users']:
            return self.fake_database['users'][email]
        return None

    def set_session_id(self, email: str, session_id: bytes) -> bool:
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

    def add_book(self, title: str, author: str, released: date, rank: 1, archive=False) -> bool:
        self._check_connection()
        if archive:
            if title in self.fake_database['archive']:
                return False
            self.fake_database['archive'][title] = {'author': author, 'released': released, 'rank': rank}
            return True

        if title in self.fake_database['storage']:
            return False
        self.fake_database['storage'][title] = {'author': author, 'released': released, 'rank': rank}
        return True
