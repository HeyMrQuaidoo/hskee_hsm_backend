import pytest
from typing import Any, Dict
from httpx import AsyncClient


# TODO:
# - Make GET, PUT and DELETE use same unique ID
# - Test for when maintenance request is linked to a property
# - Add test for updating property_unit_assoc_id of maintenance request
class TestMaintenanceRequest:
    default_maintenance_request: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_maintenance_request")
    async def test_create_maintenance_request(self, client: AsyncClient):
        response = await client.post(
            "/maintenance_request/",
            json={
                "title": "Fix AC",
                "description": "Air conditioning needs repair",
                "status": "pending",
                "priority": 1,
                "requested_by": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "scheduled_date": "2024-07-21T21:28:24.590Z",
                "completed_date": "2024-07-21T21:28:24.590Z",
                "is_emergency": False,
            },
        )
        assert response.status_code == 200

        TestMaintenanceRequest.default_maintenance_request = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_maintenance_requests(self, client: AsyncClient):
        response = await client.get(
            "/maintenance_request/", params={"limit": 10, "offset": 0}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["create_maintenance_request"], name="get_maintenance_request_by_id"
    )
    async def test_get_maintenance_request_by_id(self, client: AsyncClient):
        maintenance_request_id = self.default_maintenance_request["task_number"]

        response = await client.get(f"/maintenance_request/{maintenance_request_id}")

        assert response.status_code == 200
        assert response.json()["data"]["task_number"] == maintenance_request_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["get_maintenance_request_by_id"],
        name="update_maintenance_request_by_id",
    )
    async def test_update_maintenance_request(self, client: AsyncClient):
        maintenance_request_id = self.default_maintenance_request["task_number"]

        response = await client.put(
            f"/maintenance_request/{maintenance_request_id}",
            json={
                "title": "Fix AC and Heater",
                "description": "AC and Heater need repair",
                "status": "in_progress",
                "priority": 2,
                "requested_by": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "scheduled_date": "2024-07-21T21:28:24.590Z",
                "completed_date": "2024-07-21T21:28:24.590Z",
                "is_emergency": True,
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Fix AC and Heater"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["update_maintenance_request_by_id"],
        name="delete_maintenance_request_by_id",
    )
    async def test_delete_maintenance_request(self, client: AsyncClient):
        maintenance_request_id = self.default_maintenance_request["task_number"]

        response = await client.delete(f"/maintenance_request/{maintenance_request_id}")
        assert response.status_code == 204

        # Verify the maintenance request is deleted
        response = await client.get(f"/maintenance_request/{maintenance_request_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
