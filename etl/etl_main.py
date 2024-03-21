import logging
import time

from elastic.elastic_services import DataTransform, ElasticLoader
from redis_state.redis_services import RedisStorage
from schemas import GenresDTO, MoviesDTO, PersonsDTO
from settings import settings_db, settings_es, settings_redis

from db.postgres_services import PostgresExtractor
from db.query import get_filmwork_query, get_genres_query, get_persons_query

logging.basicConfig(level=logging.INFO)


def etl(pg: PostgresExtractor, es: ElasticLoader):
    movies_modified = es.state.get_state('movies_last_modified')
    movies = pg.extract_data(get_filmwork_query(movies_modified))
    for data in movies:
        transformed_data = DataTransform.get_transformed_data(data, MoviesDTO)
        es.load_to_es(transformed_data, index_name='movies')

    persons_modified = es.state.get_state('persons_last_modified')
    persons = pg.extract_data(get_persons_query(persons_modified))
    for data in persons:
        transformed_data = DataTransform.get_transformed_data(data, PersonsDTO)
        es.load_to_es(transformed_data, index_name='persons')

    genres_modified = es.state.get_state('genres_last_modified')
    genres = pg.extract_data(get_genres_query(genres_modified))
    for data in genres:
        transformed_data = DataTransform.get_transformed_data(data, GenresDTO)
        es.load_to_es(transformed_data, index_name='genres')


if __name__ == '__main__':
    while True:
        with RedisStorage(settings_redis) as redis_state, \
                PostgresExtractor(settings_db) as pg_extractor, \
                ElasticLoader(settings_es, redis_state) as es_loader:
            es_loader.check_index()
            etl(pg_extractor, es_loader)
        time.sleep(settings_es.INTERVAL)
