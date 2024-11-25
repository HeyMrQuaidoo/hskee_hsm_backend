import pytest
from typing import Any, Dict, List
from httpx import AsyncClient
from faker import Faker

from app.tests.properties.test_property import TestProperties
from app.tests.users.test_users import TestUsers

class TestFavoriteProperties:
    faker = Faker()

    default_favorite: Dict[str, Any] = {}
    additional_favorites: List[Dict[str, Any]] = []
    user_ids: List[str] = []
    property_ids: List[str] = []

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="test_create_favorite_property",
    )
    async def test_create_favorite_property(self, client: AsyncClient):
        response = await client.post(
            "/favorite-properties/",
            json={
                "user_id": TestUsers.default_user.get("user_id"),
                "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
            },
        )
        assert response.status_code == 201, f"Favorite property creation failed: {response.text}"
        TestFavoriteProperties.default_favorite = response.json()["data"]
        self.user_ids.append(TestUsers.default_user.get("user_id"))
        self.property_ids.append(TestProperties.default_property.get("property_unit_assoc_id"))

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["test_create_favorite_property"],
        name="test_create_additional_favorites",
    )
    async def test_create_additional_favorites(self, client: AsyncClient):
        # Create additional users and properties
        for i in range(2):
            # Create a new user
            user_response = await client.post(
                "/users/",
                json={
                    "date_of_birth": "1990-01-01",
                    "first_name": f"User{i}",
                    "last_name": f"Test{i}",
                    "email": self.faker.unique.email(),
                    "phone_number": self.faker.phone_number(),
                    "identification_number": str(
                        self.faker.random_number(digits=6, fix_len=True)
                    ),
                    "photo_url": "",
                    "gender": "male",
                    "address": [],
                    "user_emergency_info": {},
                    "user_employer_info": {},
                    "role": "user",
                },
            )
            assert user_response.status_code == 201, f"User creation failed: {user_response.text}"
            user_data = user_response.json()["data"]
            self.user_ids.append(user_data["user_id"])

            # Create a new property
            property_response = await client.post(
                "/property/",
                json={
                    "name": f"Property{i}",
                    "property_type": "residential",
                    "amount": 50000 + i * 10000,
                    "security_deposit": 5000,
                    "commission": 500,
                    "floor_space": 100 + i * 50,
                    "num_units": 1,
                    "num_bathrooms": 1,
                    "num_garages": 0,
                    "has_balconies": False,
                    "has_parking_space": False,
                    "pets_allowed": True,
                    "description": "Test property",
                    "property_status": "available",
                    "address": [],
                    "media": [],
                    "amenities": [],
                    "utilities": [],
                },
            )
            assert property_response.status_code == 201, f"Property creation failed: {property_response.text}"
            property_data = property_response.json()["data"]
            self.property_ids.append(property_data["property_unit_assoc_id"])

            # Add to favorites
            response = await client.post(
                "/favorite-properties/",
                json={
                    "user_id": user_data["user_id"],
                    "property_unit_assoc_id": property_data["property_unit_assoc_id"],
                },
            )
            assert response.status_code == 201, f"Favorite property creation failed: {response.text}"
            favorite_data = response.json()["data"]
            self.additional_favorites.append(favorite_data)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["test_create_additional_favorites"],
        name="test_get_all_favorite_properties",
    )
    async def test_get_all_favorite_properties(self, client: AsyncClient):
        response = await client.get("/favorite-properties/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to fetch favorite properties: {response.text}"
        data = response.json()["data"]
        assert isinstance(data, list)
        assert len(data) >= 3, "Expected at least 3 favorite properties"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["test_create_favorite_property"],
        name="test_get_favorite_property_by_id",
    )
    async def test_get_favorite_property_by_id(self, client: AsyncClient):
        favorite_id = self.default_favorite["favorite_id"]
        response = await client.get(f"/favorite-properties/{favorite_id}")
        assert response.status_code == 200, f"Failed to get favorite property by ID: {response.text}"
        assert response.json()["data"]["favorite_id"] == favorite_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["test_create_favorite_property"],
        name="test_filter_favorites",
    )
    async def test_filter_favorites(self, client: AsyncClient):
        # Filter by user_id
        user_id = self.user_ids[0]
        response = await client.get("/favorite-properties/", params={"user_id": user_id})
        assert response.status_code == 200, f"Failed to filter favorites by user_id: {response.text}"
        data = response.json()["data"]
        assert all(fav["user_id"] == user_id for fav in data), "Filtering by user_id failed"

        # Filter by property_unit_assoc_id
        property_id = self.property_ids[1]
        response = await client.get("/favorite-properties/", params={"property_unit_assoc_id": property_id})
        assert response.status_code == 200, f"Failed to filter favorites by property_unit_assoc_id: {response.text}"
        data = response.json()["data"]
        assert all(fav["property_unit_assoc_id"] == property_id for fav in data), "Filtering by property_unit_assoc_id failed"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="test_delete_favorite_property",
    )
    async def test_delete_favorite_property(self, client: AsyncClient):
        favorite_id = self.default_favorite["favorite_id"]
        response = await client.delete(f"/favorite-properties/{favorite_id}")
        assert response.status_code == 204, f"Favorite property deletion failed: {response.text}"

        # Verify that the favorite property is deleted
        response = await client.get(f"/favorite-properties/{favorite_id}")
        assert response.status_code == 404, f"Failed to get favorite property by ID after deletion: {response.text}"
        assert response.json()["data"] == None
