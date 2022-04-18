import time
from contextlib import contextmanager
from functools import wraps
from typing import Any

import elasticsearch
import psycopg2

from logging_settings import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный
    экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            t = start_sleep_time
            while True:
                try:
                    logger.info("Try connect to DB...")
                    return func(*args, **kwargs)
                except (
                    psycopg2.OperationalError,
                    elasticsearch.exceptions.ConnectionError,
                ):
                    logger.error("- Connection refused")
                    t = (
                        start_sleep_time * factor**n
                        if t < border_sleep_time
                        else border_sleep_time
                    )
                    time.sleep(t)
                    n += 1

        return inner

    return func_wrapper


@contextmanager
def connect_db(*args: Any, func: Any = psycopg2.connect, **kwargs: Any):
    """Метод подключения к базе данных с использованием декоратора контекстного менеджера"""
    conn = func(*args, **kwargs)
    yield conn
    conn.close()
