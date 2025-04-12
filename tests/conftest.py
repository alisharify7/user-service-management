import pytest

from core import create_app, get_config
from .utils import get_session_test, engine
from core.db import get_session, BaseModelClass
from httpx import AsyncClient


@pytest.fixture()
async def app():
    fastapp = create_app(get_config())
    fastapp.dependency_overrides[get_session] = get_session_test

    async with engine.begin() as conn:
        await conn.run_sync(BaseModelClass.metadata.drop_all)
        await conn.run_sync(BaseModelClass.metadata.create_all)
    yield fastapp


@pytest.fixture()
async def client(app):
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        print("Client is ready")
        yield client
