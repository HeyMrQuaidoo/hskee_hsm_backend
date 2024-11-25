import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.modules.contract.enums.contract_enums import ContractStatusEnum
from app.tests.contract.test_contract_type import TestContractType
from app.tests.payment_type.test_payment_type import TestPaymentType
from app.tests.properties.test_property import (
    TestProperties,
)
from app.tests.contract.test_contract import TestContract

from app.modules.common.schema.base_schema import BaseFaker
from app.tests.users.test_users import TestUsers

class TestContractAssignments:
    default_contract_assignment: Dict[str, Any] = {}
    default_contract: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="create_contract_assignment",
    )
    async def test_create_contract_assignment(self, client: AsyncClient):
        # Fetch necessary data from the dependencies

        contract_response = await client.post(
            "/contract/",
            json={
                "contract_type_id": TestContractType.default_contract_type.get(
                    "contract_type_id"
                ),
                "payment_type_id": TestPaymentType.default_payment_type.get(
                    "payment_type_id"
                ),
                "contract_status": "active",
                "contract_details": "string",
                "payment_amount": 0,
                "fee_percentage": 0,
                "fee_amount": 0,
                "date_signed": "2024-06-23T19:11:07.570Z",
                "start_date": "2024-06-23T19:11:07.570Z",
                "end_date": "2024-06-23T19:11:07.570Z",
                "contract_info": [
                    {
                        "property_unit_assoc": TestProperties.default_property.get(
                            "property_unit_assoc_id"
                        ),
                        "contract_status": "active",
                        "client_id": TestUsers.default_user.get("user_id"),
                        "employee_id": TestUsers.default_user.get("user_id"),
                    }
                ],
            },
        )
        assert contract_response.status_code == 201
        self.default_contract = contract_response.json()["data"]
        print("DEFAULT:", self.default_contract.get("contract_number"))
        contract_number = self.default_contract.get("contract_number")
        property_unit_assoc_id = TestProperties.default_property.get(
            "property_unit_assoc_id"
        )

        # Ensure required values are available
        assert (
            contract_number
        ), "Contract ID is not available. Ensure the contract creation test runs first."
        assert property_unit_assoc_id, "Property Unit Association ID is not available. Ensure the property creation test runs first."

        _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
        _start_date = BaseFaker.date_this_year()
        _end_date = BaseFaker.future_date()
        _next_payment_due = BaseFaker.future_datetime()

        response = await client.post(
            "assign-contracts/",
            json={
                  "property_unit_assoc_id": property_unit_assoc_id,
                    "contract_status": _contract_status,
                    "contract_number": contract_number,
                    "client_id": TestUsers.default_user.get("user_id"),
                    "employee_id": TestUsers.default_user.get("user_id"),
                    "start_date": _start_date.isoformat(),
                    "end_date": _end_date.isoformat(),
                    "next_payment_due": _next_payment_due.isoformat()
            },
        )
        assert (
            response.status_code == 201
        ), f"Failed to create contract assignment: {response.text}"
        TestContractAssignments.default_contract_assignment = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_contract_assignment"], name="get_contract_assignment_by_id"
    )
    async def test_get_contract_assignment_by_id(self, client: AsyncClient):
        under_contract_id = self.default_contract_assignment["under_contract_id"]

        response = await client.get(f"assign-contracts/{under_contract_id}")
        assert response.status_code == 200
        assert response.json()["data"]["under_contract_id"] == under_contract_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_contract_assignment_by_id"],
        name="update_contract_assignment_by_id",
    )
    async def test_update_contract_assignment(self, client: AsyncClient):
        under_contract_id = self.default_contract_assignment["under_contract_id"]

        response = await client.put(
            f"assign-contracts/{under_contract_id}",
            json={
                "contract_id": self.default_contract_assignment["contract_number"],
                "client_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",  # Replace with dynamic value if needed
                "employee_id": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",  # Replace with dynamic value if needed
                "contract_status": "inactive",
                "property_unit_assoc_id": TestProperties.default_property.get(
                    "property_unit_assoc_id"
                ),
                "start_date": "2024-06-23T19:11:07.570Z",
                "end_date": "2024-06-23T19:11:07.570Z",
                "next_payment_due": "2024-06-23T19:11:07.570Z",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["contract_status"] == "inactive"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_contract_assignment_by_id"],
        name="delete_contract_assignment_by_id",
    )
    async def test_delete_contract_assignment(self, client: AsyncClient):
        under_contract_id = self.default_contract_assignment["under_contract_id"]

        response = await client.delete(f"assign-contracts/{under_contract_id}")
        assert response.status_code == 204

        # Verify the contract assignment is deleted
        response = await client.get(f"assign-contracts/{under_contract_id}")
        assert response.status_code == 404
