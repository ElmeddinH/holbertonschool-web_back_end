#!/usr/bin/env python3
"""
Redis basic exercise module.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class to interact with Redis.
    """

    def __init__(self) -> None:
        """
        Initialize the Cache instance.
        Creates a Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
