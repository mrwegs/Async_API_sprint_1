from elasticsearch import AsyncElasticsearch

from src.core.config import settings

es: AsyncElasticsearch | None = AsyncElasticsearch(settings.elastic_url)


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return es
