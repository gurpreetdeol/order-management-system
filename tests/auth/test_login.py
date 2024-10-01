import pytest

from httpx import AsyncClient

from conf_test_db import app


@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login", data={'username': 'gurpreet@gmail.com', 'password': 'gur123'})
        print("Response : ", response.json())
    assert response.status_code == 200
