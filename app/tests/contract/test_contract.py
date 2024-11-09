import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.users.test_users import TestUsers  
from app.tests.properties.test_property import TestProperties
from app.tests.payment_type.test_payment_type import TestPaymentType
from contract.test_contract_type import TestContractType

class TestContract:
    default_contract: Dict[str, Any] = {}
    default_property: Dict[str, Any] = TestProperties.default_property
    default_utility: Dict[str, Any] = TestProperties.default_utility
    default_payment_type: Dict[str, Any] = TestPaymentType.default_payment_type
    default_contract_type: Dict[str, Any] = TestContractType.default_contract_type
    default_user: Dict[str, Any] = TestUsers.default_user
    default_invoice: Dict[str, Any] = {}


    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_invoice")
    async def test_create_invoice(self, client: AsyncClient):
        response = await client.post(
            "/invoice/",
            json={
                "issued_by": TestContract.default_user.get("user_id"),
                "issued_to": TestContract.default_user.get("user_id"),
                "invoice_details": "Test invoice",
                "invoice_amount": 1000,
                "due_date": "2024-06-23T19:11:07.570Z",
                "invoice_type": "standard",
                "status": "pending",
                "invoice_items": [
                    {
                        "description": "Test item",
                        "quantity": 1,
                        "unit_price": 1000
                    }
                ]
            },
        )
        assert response.status_code == 201
        TestContract.default_invoice = response.json()["data"]


    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_property", "create_payment_type", "create_contract_type", "create_user", "create_invoice"], name="create_contract")
    async def test_create_contract(self, client: AsyncClient):
        response = await client.post(
            "/contract/",
            json={
                "contract_type_id": TestContract.default_contract_type.get("contract_type_id"),
                "payment_type_id": TestContract.default_payment_type.get("payment_type_id"),
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
                        "property_unit_assoc": TestContract.default_property.get("property_unit_assoc_id"),
                        "contract_status": "active",
                        "client_id": TestContract.default_user.get("user_id"),
                        "employee_id": TestContract.default_user.get("user_id"),
                    }
                ],
                "utilities": [
                    {
                        "payment_type": "one_time",
                        "billable_amount": "100",
                        "apply_to_units": False,
                        "billable_id": TestContract.default_utility.get("utility_id"),
                    }
                ],
            },
        )
        assert response.status_code == 201
        TestContract.default_contract = response.json()["data"]


    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_contract"], name="get_contract_by")
    async def test_get_all_contracts(self, client: AsyncClient):
        response = await client.get("/contract/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_contract"], name="get_contract_by_id")
    async def test_get_contract_by_id(self, client: AsyncClient):
        contract_id = self.default_contract["contract_number"]

        response = await client.get(f"/contract/{contract_id}")

        assert response.status_code == 200
        assert response.json()["data"]["contract_number"] == contract_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_contract_by_id"], name="update_contract_by_id"
    )
    async def test_update_contract(self, client: AsyncClient):
        contract_number = TestContract.default_contract["contract_number"]
        # contract_id = TestContract.default_contract["contract_id"]

        response = await client.put(
            f"/contract/{contract_number}",
            json={
                "contract_type": "sale",
                "payment_type": "monthly",
                "contract_status": "active",
                "contract_details": "updated details",
                "payment_amount": 5000,
                "fee_percentage": 10,
                "fee_amount": 500,
                "date_signed": "2024-06-23T19:11:07.570Z",
                "start_date": "2024-06-23T19:11:07.570Z",
                "end_date": "2024-06-23T19:11:07.570Z",
                "contract_info": [
                    {
                        "contract_id": contract_number,
                        "property_unit_assoc": TestContract.default_property.get(
                            "property_unit_assoc_id"
                        ),
                        "contract_status": "active",
                        "client_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                        "employee_id": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",
                    }
                ],
                "utilities": [],
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["contract_type"] == "sale"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_contract_by_id"], name="delete_contract_by_id"
    )
    async def test_delete_contract(self, client: AsyncClient):
        contract_id = self.default_contract["contract_number"]

        response = await client.delete(f"/contract/{contract_id}")
        assert response.status_code == 204

        # Verify the contract is deleted
        response = await client.get(f"/contract/{contract_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
