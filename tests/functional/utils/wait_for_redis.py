import time

from redis import Redis

from functional.settings import settings

if __name__ == '__main__':
    host = settings.redis_host
    port = settings.redis_port
    db = settings.redis_db
    redis_client = Redis.from_url(f"redis://{host}:{port}/{db}")
    while True:
        if redis_client.ping():
            break
        time.sleep(1)
