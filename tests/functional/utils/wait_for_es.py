import logging

import backoff
from elastic_transport import TransportError
from elasticsearch import Elasticsearch

from tests.functional.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@backoff.on_exception(backoff.expo, TransportError, max_time=30, max_tries=5)
def check_elasticsearch(host, port):
    es_client = Elasticsearch(hosts=f"http://{host}:{port}", verify_certs=False, request_timeout=3)
    es_client.ping()


if __name__ == '__main__':
    host = settings.elastic_host
    port = settings.elastic_port

    logger.info("Wait for elastic %s:%s", host, port)
    check_elasticsearch(host, port)
    logger.info("Elasticsearch %s:%s is ready", host, port)
