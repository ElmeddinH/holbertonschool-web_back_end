#!/usr/bin/env python3
"""Module for Redis cache implementation with decorators."""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a Cache method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increment call count in Redis and call the original method."""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs for a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store input args and output result in Redis lists."""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    r = method.__self__._redis
    name = method.__qualname__
    count = r.get(name)
    count = int(count) if count else 0
    print("{} was called {} times:".format(name, count))
    inputs = r.lrange(name + ":inputs", 0, -1)
    outputs = r.lrange(name + ":outputs", 0, -1)
    for inp, out in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            name,
            inp.decode("utf-8"),
            out.decode("utf-8")
        ))


class Cache:
    """Cache class that uses Redis to store and retrieve data."""

    def __init__(self) -> None:
        """Initialize Cache with a Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random UUID key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float,
                                                    None]:
        """Retrieve data from Redis and optionally apply a conversion."""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieve a string value from Redis by decoding bytes."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Retrieve an integer value from Redis."""
        return self.get(key, fn=int)
