import time

from elasticsearch import Elasticsearch

from tests.functional.settings import settings

if __name__ == '__main__':
    host = settings.elastic_host
    port = settings.elastic_port
    es_client = Elasticsearch(hosts=f'http://{host}:{port}', verify_certs=False)
    while True:
        if es_client.ping():
            break
        print('Wait es...')
        time.sleep(1)
