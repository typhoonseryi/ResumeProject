from datetime import datetime
from typing import Any, List

from elasticsearch import Elasticsearch, helpers

from logging_settings import logger
from models import Movie


class ESSaver:
    """Класс сохранения данных в ElasticSearch"""

    def __init__(self, connection: Elasticsearch, state_storage: Any, state_key: str):
        self.connection = connection
        self.state_storage = state_storage
        self.last_modified = datetime.min
        self.state_key = state_key

    @staticmethod
    def map_doc(movie: Movie) -> dict:
        """Статический метод преобразования данных датаклассов под схему индекса"""
        doc = {
            "id": movie.id,
            "imdb_rating": movie.rating,
            "genre": movie.genres,
            "title": movie.title,
            "description": movie.description,
            "director": movie.director,
            "actors_names": [person["name"] for person in movie.actors],
            "writers_names": [person["name"] for person in movie.writers],
            "actors": movie.actors,
            "writers": movie.writers,
        }
        return doc

    def set_last_modified(self, modified: datetime) -> None:
        """Метод добавления последнего обновления в данные экземпляра"""
        self.last_modified = modified

    def update_data(self, movies: List[Movie]) -> None:
        """Метод сохранения пачки данных в схему индекса"""
        logger.info("Data extracted")
        logger.info("Last modified: {0}".format(self.last_modified))
        actions = [
            {"_index": "movies", "_id": movie.id, "_source": self.map_doc(movie)}
            for movie in movies
        ]

        for success, info in helpers.parallel_bulk(self.connection, actions):
            if not success:
                logger.error("Data Write Error")
                break
        else:
            self.state_storage.set_state(self.state_key, self.last_modified)
            logger.info("Data saved. Count of movies: {0}".format(len(movies)))
