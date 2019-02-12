import ast
from dynaconf import settings
import redis
from urllib.parse import urlparse

from app.core.interfaces.db import DbInterface

HOST = urlparse(settings.LEDGER_URL).hostname


class RedisInterface(DbInterface):
    BOARD_NAME = "Trade"
    ORDERED_KEYS = ["created_at", "currency", "amount", "price", "final_amount"]

    class __RedisInterface:
        def __init__(self):
            self.cache = redis.StrictRedis(host=HOST)
            self.cache.ping()

    instance = None
    cache = None

    def __init__(self):
        if not RedisInterface.instance:
            RedisInterface.instance = RedisInterface.__RedisInterface()
            self.cache = RedisInterface.instance.cache
        else:
            if not self.cache or not self.cache.ping():
                self.cache = redis.StrictRedis(host=HOST)
                self.cache.ping()

    def save(self, x_rate):
        created_at = x_rate.created_at.timestamp()
        x_rate_data = [
            x_rate.created_at.isoformat(),
            x_rate.currency,
            str(x_rate.amount),
            str(x_rate.price),
            str(x_rate.final_amount),
        ]
        self.cache.zadd(self.BOARD_NAME, created_at, x_rate_data)

    def get_all(self):
        results = self.cache.zrevrange(self.BOARD_NAME, 0, -1)
        return [ast.literal_eval(res.decode()) for res in results]

    def get(self, key=None, value=None, n=None):
        no_filters = not any((key, value, n))
        results = self.get_all()
        if no_filters:
            return [results[0]] if results else []
        n = len(results) if n is None else n
        index = self.ORDERED_KEYS.index(key) if key in self.ORDERED_KEYS else None
        if index is not None:
            return self._filter_by(index, n, results, value)
        return results[:n]

    def _filter_by(self, index, n, results, value):
        filtered_results = []
        for record in results:
            if record[index] == value:
                filtered_results.append(record)
            if len(filtered_results) == n:
                return list(reversed(filtered_results))
        return list(reversed(filtered_results))
