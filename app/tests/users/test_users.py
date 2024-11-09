import pytest
from typing import Any, Dict
from httpx import AsyncClient

class TestUsers:
    default_user: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_user")
    async def test_create_user(self, client: AsyncClient):
        response = await client.post(
            "/users/",
            json={
                "date_of_birth": "1985-05-20",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone_number": "1234567890",
                "identification_number": "123456",
                "photo_url": "",
                "gender": "male",
                "address": [
                    {
                        "address_type": "billing",
                        "primary": True,
                        "address_1": "123 Main St",
                        "address_2": "Suite 456",
                        "city": "Springfield",
                        "region": "IL",
                        "country": "USA",
                        "address_postalcode": "62704",
                    }
                ],
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": "reset_token_example",
                    "verification_token": "verification_token_example",
                    "is_subscribed_token": "subscribed_token_example",
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
                },
                "user_employer_info": {
                    "employer_name": "Acme Corp",
                    "occupation_status": "Employed",
                    "occupation_location": "Springfield",
                },
                "role": "user",
            },
        )
        assert response.status_code == 201, f"User creation failed: {response.text}"

        # Save the created user data for future tests
        TestUsers.default_user = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_users(self, client: AsyncClient):
        response = await client.get("/users/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to fetch users: {response.text}"
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_user"], name="get_user_by_id")
    async def test_get_user_by_id(self, client: AsyncClient):
        user_id = self.default_user["user_id"]

        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 200, f"Failed to get user by ID: {response.text}"
        assert response.json()["data"]["user_id"] == user_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_user_by_id"], name="update_user_by_id")
    async def test_update_user(self, client: AsyncClient):
        user_id = self.default_user["user_id"]

        response = await client.put(
            f"/users/{user_id}",
            json={
                "first_name": "John Updated",
                "last_name": "Doe Updated",
                "email": "john.updated@example.com",
                "phone_number": "9876543210",
                "identification_number": "654321",
                "photo_url": "",
                "gender": "male",
                "address": [
                    {
                        "address_type": "billing",
                        "primary": True,
                        "address_1": "456 Updated St",
                        "address_2": "Apt 789",
                        "city": "Updated City",
                        "region": "NY",
                        "country": "USA",
                        "address_postalcode": "10001",
                    }
                ],
                "user_auth_info": {
                    "password": "updatedpassword123",
                    "login_provider": "local",
                    "reset_token": "updated_reset_token",
                    "verification_token": "updated_verification_token",
                    "is_subscribed_token": "updated_subscribed_token",
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": "2024-07-21T20:52:37.078064",
                    "last_login_time": "2024-07-21T21:21:38.279Z",
                },
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Updated",
                    "emergency_contact_email": "jane.updated@example.com",
                    "emergency_contact_relation": "Mother",
                    "emergency_contact_number": "1122334455",
                },
                "user_employer_info": {
                    "employer_name": "Updated Corp",
                    "occupation_status": "Self-Employed",
                    "occupation_location": "Updated City",
                },
                "role": "admin",
            },
        )
        assert response.status_code == 200, f"User update failed: {response.text}"
        assert response.json()["data"]["first_name"] == "John Updated"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["update_user_by_id"], name="delete_user_by_id")
    async def test_delete_user(self, client: AsyncClient):
        user_id = self.default_user["user_id"]

        response = await client.delete(f"/users/{user_id}")
        assert response.status_code == 204, f"User deletion failed: {response.text}"

        # Verify that the user is deleted
        response = await client.get(f"/users/{user_id}")
        assert response.status_code == 404, f"User should be deleted but was found."
