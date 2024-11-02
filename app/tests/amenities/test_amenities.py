import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestAmenities:
    default_amenity: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_amenity")
    async def test_create_amenity(self, client: AsyncClient):
        response = await client.post(
            "/ammenities/",
            json={
                "amenity_name": "Dishwasher",
                "amenity_short_name": "Dishwasher",
                "amenity_value_type": "boolean",
                "description": "A dishwasher to help out in the home",
            },
        )
        assert response.status_code == 200

        TestAmenities.default_amenity = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_amenities(self, client: AsyncClient):
        response = await client.get("/ammenities/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_amenity"], name="get_amenity_by_id")
    async def test_get_amenity_by_id(self, client: AsyncClient):
        amenity_id = self.default_amenity["amenity_id"]

        response = await client.get(f"/ammenities/{amenity_id}")

        assert response.status_code == 200
        assert response.json()["data"]["amenity_id"] == amenity_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_amenity_by_id"], name="update_amenity_by_id")
    async def test_update_amenity(self, client: AsyncClient):
        amenity_id = self.default_amenity["amenity_id"]

        response = await client.put(
            f"/ammenities/{amenity_id}",
            json={
                "amenity_name": "Updated Swimming Pool",
                "amenity_short_name": "Updated Pool",
                "amenity_value_type": "boolean",
                "description": "An updated description for the pool",
                "created_at": "2024-07-21T20:46:20.553812+00:00",
                "updated_at": "2024-07-21T20:46:20.553812+00:00",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["amenity_name"] == "Updated Swimming Pool"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_amenity_by_id"], name="delete_amenity_by_id"
    )
    async def test_delete_amenity(self, client: AsyncClient):
        amenity_id = self.default_amenity["amenity_id"]

        response = await client.delete(f"/ammenities/{amenity_id}")
        assert response.status_code == 204

        # verify the amenity is deleted
        response = await client.get(f"/ammenities/{amenity_id}")
        assert response.status_code == 404
