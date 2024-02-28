#!/usr/bin/env python3
"""A module that tracks the live of caches"""
import requests
import redis
from functools import wraps
from typing import Callable


def count_access(method: Callable) -> Callable:
    """A function that checks and update the cache time"""
    @wraps(method)
    def wrapper(*args, **kwargs) -> str:
        """updates cache time"""
        url: str = arg[0]
        count_key: str = f"count:{url}"
        cache_key: str = f"cache:{url}"

        access_count: int = redis_client.incr(count_key)

        print(f"Access count for {url}: {access_count}")
        cached_result: bytes = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode("utf-8")

        result: str = method(*args, **kwargs)
        redis_client.set(count_key, 0)
        redis_client.setex(cache_key, 10, result)

        return result
    return wrapper


@count_access
def get_page(url: str) -> str:
    """ A function that send http request to the supplied url"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    redis_client: redis.Redis = redis.Redis()
    slow_url: str = ("http://slowwly.robertomurray.co.uk"
                     "/delay/1000/url/https://www.example.com")
    print(get_page(slow_url))
    print(get_page(slow_url))

    fast_url: str = ("https://github.com/Roo-rabab/alx-backend-storage/"
                    "blob/master/0x02-redis_basic/exercise.py")
    print(get_page(fast_url))

    import time
    time.sleep(11)
    print(get_page(slow_url))
