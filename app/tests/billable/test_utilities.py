import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestUtilities:
    default_utility: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_utility")
    async def test_create_utility(self, client: AsyncClient):
        response = await client.post(
            "/utilities/",
            json={
                "name": "newutility",
                "description": "A new utility",
            },
        )
        assert response.status_code == 200

        TestUtilities.default_utility = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_utilities(self, client: AsyncClient):
        response = await client.get("/utilities/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_utility"], name="get_utility_by_id")
    async def test_get_utility_by_id(self, client: AsyncClient):
        utility_id = self.default_utility["utility_id"]

        response = await client.get(f"/utilities/{utility_id}")

        assert response.status_code == 200
        assert response.json()["data"]["utility_id"] == utility_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["get_utility_by_id"], name="update_utility_by_id")
    async def test_update_utility(self, client: AsyncClient):
        utility_id = self.default_utility["utility_id"]

        response = await client.put(
            f"/utilities/{utility_id}",
            json={
                "name": "updatedutility",
                "description": "An updated utility",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "updatedutility"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["update_utility_by_id"], name="delete_utility_by_id"
    )
    async def test_delete_utility(self, client: AsyncClient):
        utility_id = self.default_utility["utility_id"]

        response = await client.delete(f"/utilities/{utility_id}")
        assert response.status_code == 204

        # verify the utility is deleted
        response = await client.get(f"/utilities/{utility_id}")
        assert response.status_code == 404
