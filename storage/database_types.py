from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    email: str
    password: str
    session_id: str = None


@dataclass
class Book:
    title: str
    author: str
    release_date: date
    rank: int
