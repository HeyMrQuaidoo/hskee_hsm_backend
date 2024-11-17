import pytest
from typing import Any, Dict
from httpx import AsyncClient
from faker import Faker


class TestUsers:
    default_user: Dict[str, Any] = {}
    faker = Faker()

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="TestUsers::create_user")
    async def test_create_user(self, client: AsyncClient):
        response = await client.post(
            "/users/",
            json={
                "date_of_birth": "1985-05-20",
                "first_name": "John",
                "last_name": "Doe",
                "email": self.faker.unique.email(),
                "phone_number": self.faker.phone_number(),
                "identification_number": str(
                    self.faker.random_number(digits=6, fix_len=True)
                ),
                "photo_url": "",
                "gender": "male",
                "address": [
                    {
                        "address_type": "billing",
                        "primary": True,
                        "address_1": self.faker.street_address(),
                        "address_2": self.faker.secondary_address(),
                        "city": self.faker.city(),
                        "region": self.faker.state_abbr(),
                        "country": "USA",
                        "address_postalcode": self.faker.postcode(),
                    }
                ],
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": self.faker.uuid4(),
                    "verification_token": self.faker.uuid4(),
                    "is_subscribed_token": self.faker.uuid4(),
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": "2024-07-21T20:52:37.078064",
                    "last_login_time": "2024-07-21T21:21:38.279Z",
                },
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_email": self.faker.unique.email(),
                    "emergency_contact_relation": "Sister",
                    "emergency_contact_number": self.faker.phone_number(),
                },
                "user_employer_info": {
                    "employer_name": self.faker.company(),
                    "occupation_status": "Employed",
                    "occupation_location": self.faker.city(),
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
    @pytest.mark.dependency(depends=["TestUsers::create_user"], name="get_user_by_id")
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
                "email": self.faker.unique.email(),
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

    # @pytest.mark.asyncio(loop_scope="session")
    # @pytest.mark.dependency(depends=["update_user_by_id"], name="delete_user_by_id")
    # async def test_delete_user(self, client: AsyncClient):
    #     user_id = self.default_user["user_id"]

    #     response = await client.delete(f"/users/{user_id}")
    #     assert response.status_code == 204, f"User deletion failed: {response.text}"

    #     # Verify that the user is deleted
    #     response = await client.get(f"/users/{user_id}")
    #     assert response.status_code == 404, "User should be deleted but was found."
