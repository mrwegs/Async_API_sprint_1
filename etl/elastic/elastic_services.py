import json
from typing import Any, Type

import backoff
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
from elasticsearch.helpers import bulk
from mixin import ConnMixin
from pydantic import BaseModel
from redis_state.redis_services import RedisStorage
from settings import SettingsES


class ElasticLoader(ConnMixin):
    def __init__(self, config: SettingsES, state: RedisStorage):
        super().__init__(config)
        self.state = state

    @backoff.on_exception(backoff.expo, Exception, max_tries=5)
    def _create_connection(self):
        self.connection_name = 'Elasticsearch'
        host = self.config.ES_HOST
        port = self.config.ES_PORT
        return Elasticsearch(f"http://{host}:{port}")

    def _generate_doc(self, data: list[tuple[dict[str, Any], str]], index_name: str) -> tuple[list[dict[str, Any]], str]:
        """
        Генерирует список документов в формате пригодном для helpers.bulk elasticsearch
        :param data: Список из кортежей для каждого фильма (словарь полей, датавремя последней модификации)
        :return: Кортеж из двух элементов (подготовлений список фильмов,
        датавремя последней модификации для фильма который изменялся последним)
        """
        res = []
        modified = self.state.get_state(f'{index_name}_last_modified')
        for item, modified_item in data:
            modified = modified_item
            res.append({
                "_index": index_name,
                "_id": item.get('uuid'),
                "_source": item
            })
        return res, modified

    def check_index(self):
        for index in self.config.INDEX_NAMES:
            if not self.connection.indices.exists(index=index):
                with open(f'elastic/{index}.json', encoding='utf-8') as f:
                    settings_index = json.load(f)
                self.connection.indices.create(index=index, body=settings_index, request_timeout=70)

    @backoff.on_exception(backoff.expo, ConnectionError, max_tries=15)
    def load_to_es(self, data: list[tuple[dict[str, Any], str]], index_name: str):
        """
        Загружает пачку фильмов в elasticsearch. При успешной записи фильмов в es, state принимает значение
        датавремя последнего фильма из пачки (модифицировался последним). При возникновении исключения
        запись всей пачки начинается сначала.
        :param data: Список котежей (словарь полей фильма, датавремя модификации)
        :return: None
        """
        docs, modified = self._generate_doc(data, index_name)
        success, failed = bulk(self.connection, docs)
        self.state.set_state(f'{index_name}_last_modified', modified)
        self.logger.info("%s -> Результат: успешно=%s неудач=%s", index_name, success, failed)


class DataTransform:
    @staticmethod
    def get_transformed_data(data: list[dict[str, Any]], dto: Type[BaseModel]) -> list[tuple[dict[str, Any], str]]:
        """
        С помощью pydentic модели подготавливает поля которые будут загружаться в elasticsearch.
        :param data: Пачка записей из postgres в виде словаря
        :param dto: Pydentic модель к которой будут приводится записи из postgres
        :return: Список котежей (словарь полей фильма, датавремя модификации)
        """
        res = []
        for row in data:
            item = dto(**dict(row)).model_dump(by_alias=True)
            modified = item.pop('modified')
            res.append((item, modified))
        return res
