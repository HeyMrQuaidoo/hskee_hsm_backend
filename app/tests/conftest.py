import pytest
from fastapi import FastAPI
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

# local imports
from main import app


@pytest.fixture(scope="session")
def app_instance() -> FastAPI:
    print("Registered routes:", [route.path for route in app.routes])
    return app


@pytest.fixture(scope="session")
async def client(app_instance: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app_instance)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

