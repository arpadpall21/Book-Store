import random
import string
import json
from datetime import date

import bcrypt

from storage.database_types import Book
from storage.database_adapter import DatabaseAdapter

SALT = bcrypt.gensalt()


def generate_session_id() -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(16))


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), SALT)


def fill_db_with_fake_books(database: DatabaseAdapter) -> None:
    STORAGE = 250
    ARCHIVE = 50
    raw_data = json.load(open('.data/fake_data.json', 'r'))

    database.add_book([_generate_fake_book(raw_data) for _ in range(STORAGE)])
    database.add_book([_generate_fake_book(raw_data) for _ in range(ARCHIVE)], archive=True)


def _generate_fake_book(data: dict) -> Book:
    artistic_words, names = data['artistic words'], data['names']
    return Book(title=f'{random.choice(artistic_words)} {random.choice(artistic_words)}',
                author=f'{random.choice(names)} {random.choice(names)}',
                release_date=date(random.randint(1950, 2022), random.randint(1, 12), random.randint(1, 28)),
                rank=random.randint(1, 5))
