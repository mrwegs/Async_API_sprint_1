import asyncio

import pytest_asyncio

pytest_plugins = [
    "tests.functional.conftest_library.film",
    "tests.functional.conftest_library.genre",
    "tests.functional.conftest_library.person",
    "tests.functional.conftest_library.elasticsearch",
    "tests.functional.conftest_library.redis",
    "tests.functional.conftest_library.http_client"
]


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
