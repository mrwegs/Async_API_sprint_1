import logging

import backoff
import redis
from redis import Redis

from tests.functional.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo, redis.ConnectionError, max_time=30, max_tries=5)
def check_redis(host, port, db):
    redis_client = Redis.from_url(f"redis://{host}:{port}/{db}")
    redis_client.ping()


if __name__ == '__main__':
    host = settings.redis_host
    port = settings.redis_port
    db = settings.redis_db

    logger.info("Wait for redis %s:%s", host, port)
    check_redis(host, port, db)
    logger.info("Redis %s:%s is ready", host, port)
