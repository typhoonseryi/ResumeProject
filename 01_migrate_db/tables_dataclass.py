import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Filmwork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = field(default="")
    description: str = field(default="")
    creation_date: datetime = field(default=datetime.now)
    file_path: str = field(default="")
    rating: float = field(default=0.0)
    type: str = field(default="movie")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Person:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = field(default="")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Genre:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = field(default="")
    description: str = field(default="")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class PersonFilmwork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: str = field(default="")
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GenreFilmwork:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)


tuple_tables = (Filmwork, Person, Genre, PersonFilmwork, GenreFilmwork)
