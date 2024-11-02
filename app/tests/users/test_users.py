import pytest
from typing import Any, Dict
from httpx import AsyncClient


# TODO:
# - Deleting user should delete underlying address
# - Deleting user should delete emergency_info
class TestUsers:
    default_user: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_user")
    async def test_create_user(self, client: AsyncClient):
        response = await client.post(
            "/users/",
            json={
                "date_of_birth": "2024-07-21",
                "first_name": "John",
                "last_name": "Doe",
                "email": "daniel.quaidoo@gmail.com",
                "phone_number": "1234567890",
                "identification_number": "12345",
                "photo_url": "",
                "gender": "male",
                "address": {
                    "address_type": "billing",
                    "primary": True,
                    "address_1": "123 Main St",
                    "address_2": "",
                    "city": "Springfield",
                    "region": "IL",
                    "country": "USA",
                    "address_postalcode": "62704",
                },
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": "",
                    "verification_token": "",
                    "is_subscribed_token": "",
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": "2024-07-21T20:52:37.078064",
                    "last_login_time": "2024-07-21T21:21:38.279Z",
                },
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_email": "jane.doe@example.com",
                    "emergency_contact_relation": "Sister",
                    "emergency_contact_number": "0987654321",
                    "emergency_address_hash": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                },
                "user_employer_info": {
                    "employer_name": "Acme Corp",
                    "occupation_status": "Employed",
                    "occupation_location": "Springfield",
                },
                "role": "user",
            },
        )
        assert response.status_code == 200

        TestUsers.default_user = response.json()["data"][0]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_users(self, client: AsyncClient):
        response = await client.get("/users/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_user"], name="get_user_by_id")
    async def test_get_user_by_id(self, client: AsyncClient):
        user_id = self.default_user["user_id"]

        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        assert response.json()["data"]["user_id"] == user_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["get_user_by_id"], name="update_user_by_id")
    async def test_update_user(self, client: AsyncClient):
        user_id = self.default_user["user_id"]

        response = await client.put(
            f"/users/{user_id}",
            json={
                "first_name": "John Updated",
                "last_name": "Doe Updated",
                "email": "john.doe@example.com",
                "phone_number": "1234567890",
                "identification_number": "12345",
                "photo_url": "",
                "gender": "male",
                "address": {
                    "address_type": "billing",
                    "primary": True,
                    "address_1": "123 Main St",
                    "address_2": "",
                    "city": "Springfield",
                    "region": "IL",
                    "country": "USA",
                    "address_postalcode": "62704",
                },
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": "",
                    "verification_token": "",
                    "is_subscribed_token": "",
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": "2024-07-21T20:52:37.078064",
                    "last_login_time": "2024-07-21T21:21:38.279Z",
                },
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_email": "jane.doe@example.com",
                    "emergency_contact_relation": "Sister",
                    "emergency_contact_number": "0987654321",
                    "emergency_address_hash": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                },
                "user_employer_info": {
                    "employer_name": "Acme Corp",
                    "occupation_status": "Employed",
                    "occupation_location": "Springfield",
                },
                "role": "user",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["first_name"] == "John Updated"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["update_user_by_id"], name="delete_user_by_id")
    async def test_delete_user(self, client: AsyncClient):
        user_id = self.default_user["user_id"]

        response = await client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # verify the user is deleted
        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
