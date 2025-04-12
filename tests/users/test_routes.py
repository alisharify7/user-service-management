import pytest


@pytest.mark.asyncio
async def test_index(client):
    print(client)
    response = await client.get("/")
    assert response.status_code == 200
