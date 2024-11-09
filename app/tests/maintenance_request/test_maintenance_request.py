import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.users.test_users import TestUsers  # Ensure this import exists and points to your TestUsers setup

class TestMaintenanceRequest:
    default_maintenance_request: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestUsers::test_create_user"], name="create_maintenance_request")
    async def test_create_maintenance_request(self, client: AsyncClient):
        # Fetching user ID from TestUsers
        user_id = TestUsers.default_user.get("user_id")
        assert user_id, "User ID is not set. Ensure the user creation test runs first."

        response = await client.post(
            "/maintenance-request/",
            json={
                "title": "Fix AC",
                "description": "Air conditioning needs repair",
                "status": "pending",  
                "priority": "medium",  
                "requested_by": user_id,  
                "scheduled_date": "2024-07-21T21:28:24.590Z",
                "completed_date": "2024-07-21T21:28:24.590Z",
                "is_emergency": False,
            },
        )
        assert response.status_code == 201, f"Failed to create maintenance request: {response.text}"
        TestMaintenanceRequest.default_maintenance_request = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_maintenance_requests(self, client: AsyncClient):
        response = await client.get(
            "/maintenance-request/", params={"limit": 10, "offset": 0}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_maintenance_request"], name="get_maintenance_request_by_id"
    )
    async def test_get_maintenance_request_by_id(self, client: AsyncClient):
        maintenance_request_id = self.default_maintenance_request["task_number"]

        response = await client.get(f"/maintenance-request/{maintenance_request_id}")

        assert response.status_code == 200, f"Failed to get maintenance request by ID: {response.text}"
        assert response.json()["data"]["task_number"] == maintenance_request_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_maintenance_request_by_id"],
        name="update_maintenance_request_by_id",
    )
    async def test_update_maintenance_request(self, client: AsyncClient):
        maintenance_request_id = self.default_maintenance_request["task_number"]
        user_id = TestUsers.default_user.get("user_id")
        assert user_id, "User ID is not set. Ensure the user creation test runs first."

        response = await client.put(
            f"/maintenance-request/{maintenance_request_id}",
            json={
                "title": "Fix AC and Heater",
                "description": "AC and Heater need repair",
                "status": "in_progress",
                "priority": "high",  # Matches PriorityEnum
                "requested_by": user_id,  # Fetched dynamically
                "scheduled_date": "2024-07-21T21:28:24.590Z",
                "completed_date": "2024-07-21T21:28:24.590Z",
                "is_emergency": True,
            },
        )
        assert response.status_code == 200, f"Failed to update maintenance request: {response.text}"
        assert response.json()["data"]["title"] == "Fix AC and Heater"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_maintenance_request_by_id"],
        name="delete_maintenance_request_by_id",
    )
    async def test_delete_maintenance_request(self, client: AsyncClient):
        maintenance_request_id = self.default_maintenance_request["task_number"]

        response = await client.delete(f"/maintenance-request/{maintenance_request_id}")
        assert response.status_code == 204, f"Failed to delete maintenance request: {response.text}"

        # Verify the maintenance request is deleted
        response = await client.get(f"/maintenance-request/{maintenance_request_id}")
        assert response.status_code == 404, f"Maintenance request not properly deleted: {response.text}"
