import time

from elasticsearch import Elasticsearch

from functional.settings import settings

if __name__ == '__main__':
    host = settings.elastic_host
    port = settings.elastic_port
    es_client = Elasticsearch(hosts=f'http://{host}:{port}', validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
