class DatabaseAdapter:
    def __init__(self):
        self.fake_database = {'users': {}, 'storage': {}, 'archive': {}}

    def create_account(self, user: str, password: str) -> bool:
        if user in self.fake_database['users']:
            return False
        self.fake_database['users'][user] = {'password': password, 'session_id': None}
        return True

    def delete_account(self, user: str) -> bool:
        if user not in self.fake_database['users']:
            return False
        del self.fake_database['users'][user]
        return True

    def set_session_id(self, user: str, session_id: int) -> bool:
        if user not in self.fake_database['users']:
            return False
        self.fake_database['users'][user]['session_id'] = session_id
        return True

    def clear_session_id(self, user: str) -> bool:
        if user not in self.fake_database['users']:
            return False
        self.fake_database['users'][user]['session_id'] = None
        return True

    def get_account(self, user: str) -> dict | None:
        if user not in self.fake_database['users']:
            return None
        return self.fake_database['users'][user]
