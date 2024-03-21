import datetime

import backoff
from mixin import ConnMixin
from redis import Redis
from redis.exceptions import ConnectionError


class RedisStorage(ConnMixin):

    @backoff.on_exception(backoff.expo, ConnectionError, max_tries=3)
    def _create_connection(self):
        self.connection_name = 'Redis'
        host = self.config.REDIS_HOST
        port = self.config.REDIS_PORT
        return Redis.from_url(f"redis://{host}:{port}")

    @backoff.on_exception(backoff.expo, ConnectionError, max_tries=3)
    def set_state(self, key, value):
        value = str(value)
        self.connection.set(key, value)

    @backoff.on_exception(backoff.expo, ConnectionError, max_tries=3)
    def get_state(self, key):
        value_bytes = self.connection.get(key)
        if value_bytes:
            return value_bytes.decode('utf-8')
        return datetime.datetime.min
