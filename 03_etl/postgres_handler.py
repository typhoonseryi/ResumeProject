from datetime import datetime
from typing import Any, List

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from logging_settings import logger
from models import Movie

QUERY_PRODUCER = """
    SELECT id, modified
    FROM content.{0}
    WHERE modified > {1}
    ORDER BY modified
    LIMIT {2}
    """

QUERY_ENRICHER = """
    SELECT fw.id, fw.modified
    FROM content.film_work fw
    LEFT JOIN content.{0}_film_work g_pfw ON g_pfw.film_work_id = fw.id
    WHERE g_pfw.{0}_id IN %s
    ORDER BY fw.modified
    """

QUERY_MERGER = """
    SELECT
        fw.id AS fw_id,
        fw.title,
        fw.description,
        fw.rating,
        g.name AS genre,
        pfw.role,
        p.id AS p_id,
        p.full_name
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id=fw.id
    LEFT JOIN content.person p ON p.id = pfw.person_id
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.id IN %s
    GROUP BY fw.id, g.name, pfw.role, p.id
    ORDER BY fw.id
    """


class PostgresLoader:
    """Класс загрузчика из БД Postgres"""

    def __init__(
        self,
        connection: _connection,
        target_db: Any,
        table_name: str,
        modified: datetime,
        chunk_size: int,
    ):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.target_db = target_db
        self.table_name = table_name
        self.modified = modified
        self.chunk_size = chunk_size

    @staticmethod
    def append_person(movie: Movie, rec: DictCursor) -> None:
        """Статический метод добавления данных о персоне в датакласс Movie"""
        person_dict = {"id": rec["p_id"], "name": rec["full_name"]}
        if rec["role"] == "actor":
            if person_dict not in movie.actors:
                movie.actors.append(person_dict)
        elif rec["role"] == "writer":
            if person_dict not in movie.writers:
                movie.writers.append(person_dict)
        else:
            movie.director = rec["full_name"]

    @staticmethod
    def append_genre(movie: Movie, rec: DictCursor) -> None:
        """Статический метод добавления данных о жанре в датакласс Movie"""
        genre = rec["genre"]
        if genre not in movie.genres:
            movie.genres.append(genre)

    def extract_data(self) -> list:
        """Метод извлечения пачки данных обновленных фильмов из БД"""
        query_producer = QUERY_PRODUCER.format(
            self.table_name, "'{0}'".format(self.modified), self.chunk_size
        )
        self.cursor.execute(query_producer)
        data_producer = self.cursor.fetchall()
        if data_producer:
            last_modified = data_producer[-1]["modified"]
            self.target_db.set_last_modified(last_modified)
            ids_producer = tuple([record["id"] for record in data_producer])

            if self.table_name in ("person", "genre"):
                query_enricher = self.cursor.mogrify(
                    QUERY_ENRICHER.format(self.table_name), (ids_producer,)
                )
                self.cursor.execute(query_enricher)
                ids_enricher = tuple(
                    [record["id"] for record in self.cursor.fetchall()]
                )
            else:
                ids_enricher = ids_producer

            query_merger = self.cursor.mogrify(QUERY_MERGER, (ids_enricher,))
            self.cursor.execute(query_merger)
            return self.cursor.fetchall()
        else:
            return []

    def transform_data(self, movies_data: list) -> List[Movie]:
        """Метод трансформации сырых данных в данные датаклассов"""
        if movies_data:
            movies = []
            cur_id = ""
            movie = Movie()
            for record in movies_data:
                if record["fw_id"] != cur_id:
                    cur_id = record["fw_id"]
                    movie = Movie(
                        id=record["fw_id"],
                        title=record["title"],
                        description=record["description"],
                        rating=record["rating"],
                    )
                    movies.append(movie)
                self.append_genre(movie, record)
                self.append_person(movie, record)
            return movies
        else:
            return []

    def save_table_data(self) -> None:
        """Метод извлечения, трансформации и записи данных в ElasticSearch"""
        movies_raw = self.extract_data()
        movies_to_update = self.transform_data(movies_raw)
        if movies_to_update:
            self.target_db.update_data(movies_to_update)
        else:
            logger.info("No data to update")
