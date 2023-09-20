from dataclasses import dataclass
from datetime import date
from enum import Enum


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
    ranked: int


class StorageType(Enum):
    STORAGE = 'storage'
    ARCHIVE = 'archive'
