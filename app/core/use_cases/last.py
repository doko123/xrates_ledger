import logging

logger = logging.getLogger(__name__)


class LastUC:
    def last(self, n=None, currency=None):
        from app.core.interfaces import my_sql, redis

        key = "currency" if currency else None

        cached_trades = redis.RedisInterface().get(key=key, value=currency, n=n)
        saved_trades = my_sql.MySqlInterface().get(key=key, value=currency, n=n)
        return cached_trades, saved_trades
