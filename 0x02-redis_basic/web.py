#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

# Use a connection pool for Redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
store = redis.Redis(connection_pool=pool)

def count_url_access(method):
    """ Decorator counting how many times
    a URL is accessed """
    @wraps(method)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        count_key = f"count:{url}"
        try:
            html = method(url)
            store.incr(count_key)
            store.setex(cached_key, 10, html)  # Use setex for setting expiration
            return html
        except requests.RequestException as e:
            # Handle request exceptions here
            print(f"Error fetching URL: {url}. Exception: {e}")
            return ""
    return wrapper

@count_url_access
def get_page(url: str) -> str:
    """ Returns HTML content of a url """
    res = requests.get(url)
    res.raise_for_status()  # Raise HTTPError for bad responses
    return res.text
