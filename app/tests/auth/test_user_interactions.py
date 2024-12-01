import pytest
from typing import Any, Dict, List
from httpx import AsyncClient
from app.tests.properties.test_property import TestProperties
from app.tests.users.test_users import TestUsers
from faker import Faker
from datetime import datetime, timedelta

class TestUserInteractions:
    default_interaction: Dict[str, Any] = {}
    additional_interactions: List[Dict[str, Any]] = []
    employee_user: Dict[str, Any] = {}
    faker = Faker()
    contact_times = []

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="TestUserInteractions::create_employee_user",
    )
    async def test_create_employee_user(self, client: AsyncClient):
        # Create an employee user
        response = await client.post(
            "/users/",
            json={
                "date_of_birth": "1990-01-01",
                "first_name": "Employee",
                "last_name": "User",
                "email": self.faker.unique.email(),
                "phone_number": self.faker.phone_number(),
                "identification_number": str(self.faker.random_number(digits=6, fix_len=True)),
                "photo_url": "",
                "gender": "female",
                "address": [],
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": "",
                    "verification_token": "",
                    "is_subscribed_token": "",
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": None,
                    "last_login_time": None,
                    "current_login_time": datetime.now().isoformat() + 'Z'
                },
                "user_emergency_info": {},
                "user_employer_info": {},
                "role": "employee",
            },
        )
        assert response.status_code == 201, f"Employee user creation failed: {response.text}"
        TestUserInteractions.employee_user = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="TestUserInteractions::create_user_interaction",
    )
    async def test_create_user_interaction(self, client: AsyncClient):
        contact_time = datetime.now().isoformat() + 'Z'
        self.contact_times.append(contact_time)
        response = await client.post(
            "/user-interactions/",
            json={
                "user_id": TestUsers.default_user.get("user_id"),
                "employee_id": TestUserInteractions.employee_user.get("user_id"),
                "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
                "contact_time": contact_time,
                "contact_details": "User contacted employee regarding property viewing.",
            },
        )
        assert response.status_code == 201, f"User interaction creation failed: {response.text}"
        TestUserInteractions.default_interaction = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUserInteractions::create_user_interaction"], 
                            name="TestUserInteractions::create_additional_interactions")
    async def test_create_additional_interactions(self, client: AsyncClient):
        # Create additional interactions for filtering tests
        for i in range(2):
            contact_time = (datetime.now() - timedelta(days=i+1)).isoformat() + 'Z'
            self.contact_times.append(contact_time)
            response = await client.post(
                "/user-interactions/",
                json={
                    "user_id": TestUsers.default_user.get("user_id"),
                    "employee_id": TestUserInteractions.employee_user.get("user_id"),
                    "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
                    "contact_time": contact_time,
                    "contact_details": f"Additional interaction {i}",
                },
            )
            assert response.status_code == 201, f"Additional interaction creation failed: {response.text}"
            interaction_data = response.json()["data"]
            self.additional_interactions.append(interaction_data)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUserInteractions::create_additional_interactions"],
                            name="TestUserInteractions::get_user_interaction_by_id")
    async def test_get_all_user_interactions(self, client: AsyncClient):
        response = await client.get("/user-interactions/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to fetch user interactions: {response.text}"
        data = response.json()["data"]
        assert isinstance(data, list)
        assert len(data) >= 3, "Expected at least 3 user interactions"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUserInteractions::create_user_interaction"], name="TestUserInteractions::get_user_interaction_by_id")
    async def test_get_user_interaction_by_id(self, client: AsyncClient):
        interaction_id = self.default_interaction["user_interaction_id"]
        response = await client.get(f"/user-interactions/{interaction_id}")
        assert response.status_code == 200, f"Failed to get user interaction by ID: {response.text}"
        assert response.json()["data"]["user_interaction_id"] == interaction_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUserInteractions::create_user_interaction"], name="TestUserInteractions::filter_user_interactions")
    async def test_filter_user_interactions(self, client: AsyncClient):
        # Filter by user_id
        user_id = TestUsers.default_user.get("user_id")
        response = await client.get("/user-interactions/", params={"user_id": user_id})
        assert response.status_code == 200, f"Failed to filter interactions by user_id: {response.text}"
        data = response.json()["data"]
        assert all(interaction["user_id"] == user_id for interaction in data), "Filtering by user_id failed"

        # Filter by employee_id
        employee_id = TestUserInteractions.employee_user.get("user_id")
        response = await client.get("/user-interactions/", params={"employee_id": employee_id})
        assert response.status_code == 200, f"Failed to filter interactions by employee_id: {response.text}"
        data = response.json()["data"]
        assert all(interaction["employee_id"] == employee_id for interaction in data), "Filtering by employee_id failed"

        # Filter by property_unit_assoc_id
        property_id = TestProperties.default_property.get("property_unit_assoc_id")
        response = await client.get("/user-interactions/", params={"property_unit_assoc_id": property_id})
        assert response.status_code == 200, f"Failed to filter interactions by property_unit_assoc_id: {response.text}"
        data = response.json()["data"]
        assert all(interaction["property_unit_assoc_id"] == property_id for interaction in data), "Filtering by property_unit_assoc_id failed"

        # Filter by date range
        date_gte = (datetime.now() - timedelta(days=2)).isoformat() + 'Z'
        date_lte = datetime.now().isoformat() + 'Z'
        response = await client.get("/user-interactions/", params={"date_gte": date_gte, "date_lte": date_lte})
        assert response.status_code == 200, f"Failed to filter interactions by date range: {response.text}"
        data = response.json()["data"]
        assert len(data) > 0, "Expected at least one interaction in the date range"
        for interaction in data:
            contact_time = datetime.fromisoformat(interaction["contact_time"].replace('Z', '+00:00'))
            assert datetime.fromisoformat(date_gte.replace('Z', '+00:00')) <= contact_time <= datetime.fromisoformat(date_lte.replace('Z', '+00:00')), "Filtering by date range failed"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUserInteractions::get_user_interaction_by_id"], name="TestUserInteractions::update_user_interaction_by_id")
    async def test_update_user_interaction(self, client: AsyncClient):
        interaction_id = self.default_interaction["user_interaction_id"]
        response = await client.put(
            f"/user-interactions/{interaction_id}",
            json={
                "contact_details": "Updated contact details: User requested more information.",
            },
        )
        assert response.status_code == 200, f"User interaction update failed: {response.text}"
        assert response.json()["data"]["contact_details"] == "Updated contact details: User requested more information."

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUserInteractions::update_user_interaction_by_id"], name="TestUserInteractions::delete_user_interaction_by_id")
    async def test_delete_user_interaction(self, client: AsyncClient):
        interaction_id = self.default_interaction["user_interaction_id"]
        response = await client.delete(f"/user-interactions/{interaction_id}")
        assert response.status_code == 204, f"User interaction deletion failed: {response.text}"

        # Verify that the interaction is deleted
        response = await client.get(f"/user-interactions/{interaction_id}")
        assert response.status_code == 404, f"Failed to get user interaction by ID after deletion: {response.text}"
        assert response.json()["data"] == None
