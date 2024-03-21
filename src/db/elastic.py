from typing import Optional
from elasticsearch import AsyncElasticsearch

import os

es: Optional[AsyncElasticsearch] = AsyncElasticsearch(os.getenv('ES_URL'))


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return es
