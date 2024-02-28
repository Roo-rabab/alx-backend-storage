# web.py
import requests
import redis
import time

store = redis.Redis()

def count_url_access(method):
    @wraps(method)
    def wrapper(url):
        count_key = f"count:{url}"
        store.incr(count_key)
        return method(url)

    return wrapper

def cache_with_expiration(expiration_time):
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            cached_key = f"cached:{url}"
            cached_data = store.get(cached_key)
            if cached_data:
                return cached_data.decode("utf-8")

            html = func(url)

            store.setex(cached_key, expiration_time, html)
            return html

        return wrapper

    return decorator

@count_url_access
@cache_with_expiration(expiration_time=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
