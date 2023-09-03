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

    def create_user(self, user: str, password: bytes) -> bool:
        self._check_connection()
        if user not in self.fake_database['users']:
            self.fake_database['users'][user] = {'password': password, 'session_id': None}
            return True
        return False

    def delete_user(self, user: str) -> bool:
        self._check_connection()
        if user in self.fake_database['users']:
            del self.fake_database['users'][user]
            return True
        return False

    def get_user(self, user: str) -> dict | None:
        self._check_connection()
        if user in self.fake_database['users']:
            return self.fake_database['users'][user]
        return None

    def set_session_id(self, user: str, session_id: bytes) -> bool:
        self._check_connection()
        if user in self.fake_database['users']:
            self.fake_database['users'][user]['session_id'] = session_id
            return True
        return False

    def clear_session_id(self, user: str) -> bool:
        self._check_connection()
        if user in self.fake_database['users']:
            self.fake_database['users'][user]['session_id'] = None
            return True
        return False
