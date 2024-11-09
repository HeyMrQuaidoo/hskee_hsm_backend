import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.properties.test_property import TestProperties  # Assuming these exist and follow the established structure
from app.tests.contract.test_contract import TestContract

class TestContractAssignments:
    default_contract_assignment: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[
            "TestProperties::test_create_property",
            "TestContract::test_create_contract"
        ], 
        name="create_contract_assignment"
    )
    async def test_create_contract_assignment(self, client: AsyncClient):
        # Fetch necessary data from the dependencies
        contract_id = TestContract.default_contract.get("contract_number")
        property_unit_assoc_id = TestProperties.default_property.get("property_unit_assoc_id")

        # Ensure required values are available
        assert contract_id, "Contract ID is not available. Ensure the contract creation test runs first."
        assert property_unit_assoc_id, "Property Unit Association ID is not available. Ensure the property creation test runs first."

        response = await client.post(
            "assign-contracts/",
            json={
                "contract_id": contract_id,
                "client_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",  # Replace with dynamic value if necessary
                "employee_id": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",  # Replace with dynamic value if necessary
                "contract_status": "active",
                "property_unit_assoc": property_unit_assoc_id,
                "start_date": "2024-06-23T19:11:07.570Z",
                "end_date": "2024-06-23T19:11:07.570Z",
                "next_payment_due": "2024-06-23T19:11:07.570Z",
            },
        )
        assert response.status_code == 201, f"Failed to create contract assignment: {response.text}"
        TestContractAssignments.default_contract_assignment = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_contract_assignment"], name="get_contract_assignment_by_id")
    async def test_get_contract_assignment_by_id(self, client: AsyncClient):
        under_contract_id = self.default_contract_assignment["under_contract_id"]

        response = await client.get(f"assign-contracts/{under_contract_id}")
        assert response.status_code == 200
        assert response.json()["data"]["under_contract_id"] == under_contract_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_contract_assignment_by_id"], name="update_contract_assignment_by_id")
    async def test_update_contract_assignment(self, client: AsyncClient):
        under_contract_id = self.default_contract_assignment["under_contract_id"]

        response = await client.put(
            f"assign-contracts/{under_contract_id}",
            json={
                "contract_id": self.default_contract_assignment["contract_number"],
                "client_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",  # Replace with dynamic value if needed
                "employee_id": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",  # Replace with dynamic value if needed
                "contract_status": "inactive",
                "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
                "start_date": "2024-06-23T19:11:07.570Z",
                "end_date": "2024-06-23T19:11:07.570Z",
                "next_payment_due": "2024-06-23T19:11:07.570Z",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["contract_status"] == "inactive"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["update_contract_assignment_by_id"], name="delete_contract_assignment_by_id")
    async def test_delete_contract_assignment(self, client: AsyncClient):
        under_contract_id = self.default_contract_assignment["under_contract_id"]

        response = await client.delete(f"assign-contracts/{under_contract_id}")
        assert response.status_code == 204

        # Verify the contract assignment is deleted
        response = await client.get(f"assign-contracts/{under_contract_id}")
        assert response.status_code == 404
