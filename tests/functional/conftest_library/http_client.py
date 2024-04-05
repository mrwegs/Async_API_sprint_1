from typing import Mapping

import aiohttp
import pytest_asyncio

from tests.functional.settings import settings


@pytest_asyncio.fixture(scope="session")
async def client_session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def make_get_request(client_session: aiohttp.ClientSession):
    async def inner(uri: str, data: Mapping | None = None):
        url = settings.service_url + uri

        async with client_session.get(url, params=data) as response:
            body = await response.json()
            status = response.status

            return body, status

    return inner
