DB_SCHEMA_NAME = "content"
CHUNK_SIZE = 30

FILMWORK_SQLITE_TABLE_VALUES = "%(id)s, %(title)s, %(description)s, %(creation_date)s,\
    %(rating)s, %(type)s, %(created_at)s, %(updated_at)s"
FILMWORK_POSTGRES_TABLE_SCHEMA = (
    "id, title, description, creation_date, rating, type, created, modified"
)
FILMWORK_POSTGRES_TABLE_NAME = "film_work"
FILMWORK_OPTIONS = (
    FILMWORK_SQLITE_TABLE_VALUES,
    FILMWORK_POSTGRES_TABLE_SCHEMA,
    DB_SCHEMA_NAME,
    FILMWORK_POSTGRES_TABLE_NAME,
)

PERSON_SQLITE_TABLE_VALUES = "%(id)s, %(full_name)s, %(created_at)s, %(updated_at)s"
PERSON_POSTGRES_TABLE_SCHEMA = "id, full_name, created, modified"
PERSON_POSTGRES_TABLE_NAME = "person"
PERSON_OPTIONS = (
    PERSON_SQLITE_TABLE_VALUES,
    PERSON_POSTGRES_TABLE_SCHEMA,
    DB_SCHEMA_NAME,
    PERSON_POSTGRES_TABLE_NAME,
)

GENRE_SQLITE_TABLE_VALUES = (
    "%(id)s, %(name)s, %(description)s, %(created_at)s, %(updated_at)s"
)
GENRE_POSTGRES_TABLE_SCHEMA = "id, name, description, created, modified"
GENRE_POSTGRES_TABLE_NAME = "genre"
GENRE_OPTIONS = (
    GENRE_SQLITE_TABLE_VALUES,
    GENRE_POSTGRES_TABLE_SCHEMA,
    DB_SCHEMA_NAME,
    GENRE_POSTGRES_TABLE_NAME,
)

PERSON_FILMWORK_SQLITE_TABLE_VALUES = (
    "%(id)s, %(person_id)s, %(film_work_id)s, %(role)s, %(created_at)s"
)
PERSON_FILMWORK_POSTGRES_TABLE_SCHEMA = "id, person_id, film_work_id, role, created"
PERSON_FILMWORK_POSTGRES_TABLE_NAME = "person_film_work"
PERSON_FILMWORK_OPTIONS = (
    PERSON_FILMWORK_SQLITE_TABLE_VALUES,
    PERSON_FILMWORK_POSTGRES_TABLE_SCHEMA,
    DB_SCHEMA_NAME,
    PERSON_FILMWORK_POSTGRES_TABLE_NAME,
)

GENRE_FILMWORK_SQLITE_TABLE_VALUES = (
    "%(id)s, %(genre_id)s, %(film_work_id)s, %(created_at)s"
)
GENRE_FILMWORK_POSTGRES_TABLE_SCHEMA = "id, genre_id, film_work_id, created"
GENRE_FILMWORK_POSTGRES_TABLE_NAME = "genre_film_work"
GENRE_FILMWORK_OPTIONS = (
    GENRE_FILMWORK_SQLITE_TABLE_VALUES,
    GENRE_FILMWORK_POSTGRES_TABLE_SCHEMA,
    DB_SCHEMA_NAME,
    GENRE_FILMWORK_POSTGRES_TABLE_NAME,
)

tuple_options = (
    FILMWORK_OPTIONS,
    PERSON_OPTIONS,
    GENRE_OPTIONS,
    PERSON_FILMWORK_OPTIONS,
    GENRE_FILMWORK_OPTIONS,
)
