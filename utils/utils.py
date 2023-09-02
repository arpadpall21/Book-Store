import random
import string

import bcrypt

SALT = bcrypt.gensalt()


def generate_session_id() -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(16))


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), SALT)
