import pytest
from typing import Any, Dict
from httpx import AsyncClient

class TestAmenities:
    default_amenity: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_amenity")
    async def test_create_amenity(self, client: AsyncClient):
        response = await client.post(
            "/amenities/",
            json={
                "amenity_name": "Dishwasher",
                "amenity_short_name": "Dishwasher",
                "amenity_value_type": "boolean",
                "description": "A dishwasher to help out in the home",
            },
        )
        # Correcting expected status code to 201 (Created)
        print("Response:", response)
        assert response.status_code == 201, response.text

        TestAmenities.default_amenity = response.json().get("data", {})

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_amenities(self, client: AsyncClient):
        response = await client.get("/amenities/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, response.text
        assert isinstance(response.json(), dict), response.text

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_amenity"], name="get_amenity_by_id")
    async def test_get_amenity_by_id(self, client: AsyncClient):
        amenity_id = self.default_amenity["amenity_id"]
        response = await client.get(f"/amenities/{amenity_id}")
        assert response.status_code == 200, response.text
        assert response.json().get("data", {}).get("amenity_id") == amenity_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["get_amenity_by_id"], name="update_amenity_by_id")
    async def test_update_amenity(self, client: AsyncClient):
        amenity_id = self.default_amenity["amenity_id"]
        response = await client.put(
            f"/amenities/{amenity_id}",
            json={
                "amenity_name": "Updated Dishwasher",
                "amenity_short_name": "Updated Dishwasher",
                "amenity_value_type": "boolean",
                "description": "Updated description",
            },
        )
        assert response.status_code == 200, response.text
        assert response.json().get("data", {}).get("amenity_name") == "Updated Dishwasher"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["update_amenity_by_id"], name="delete_amenity_by_id"
    )
    async def test_delete_amenity(self, client: AsyncClient):
        amenity_id = self.default_amenity["amenity_id"]
        response = await client.delete(f"/amenities/{amenity_id}")
        assert response.status_code == 204, response.text

        # verify the amenity is deleted
        response = await client.get(f"/amenities/{amenity_id}")
        assert response.status_code == 404, response.text
