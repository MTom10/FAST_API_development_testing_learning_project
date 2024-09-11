"""
fastapi.testclient -allows to interact with api without starting the api server
httpx - to make the requests
"""
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from main.main import app
from main.routers.post import comment_table, post_table


# Configure async tests to run once for entire session, built-in async io for runing async tests
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# create the test client instead of starting the api server
# yielding allows to do something before or after the execution, set-up tear-down
@pytest.fixture()
def client() -> Generator:
    print("Getting test client")
    yield TestClient(app)


# clear the DB, run on every test
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield


# testclient to make requests within our tests
# dependencies injection (client)
@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac

"""
@pytest.fixture()
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport) as client:
        yield client
"""