class DatabaseAdapter:
    def __init__(self):
        self.fake_database = {'users': {}, 'storage': {}, 'archive': {}}

    def create_user(self, user: str, password: bytes) -> bool:
        if user not in self.fake_database['users']:
            self.fake_database['users'][user] = {'password': password, 'session_id': None}
            return True
        return False

    def delete_user(self, user: str) -> bool:
        if user in self.fake_database['users']:
            del self.fake_database['users'][user]
            return True
        return False

    def get_user(self, user: str) -> dict | None:
        if user in self.fake_database['users']:
            return self.fake_database['users'][user]
        return None

    def set_session_id(self, user: str, session_id: bytes) -> bool:
        if user in self.fake_database['users']:
            self.fake_database['users'][user]['session_id'] = session_id
            return True
        return False

    def clear_session_id(self, user: str) -> bool:
        if user in self.fake_database['users']:
            self.fake_database['users'][user]['session_id'] = None
            return True
        return False

