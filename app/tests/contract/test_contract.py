import pytest
from typing import Any, Dict
from httpx import AsyncClient

from app.tests.users.test_users import TestUsers
from app.tests.properties.test_property import TestProperties
from app.tests.payment_type.test_payment_type import TestPaymentType
from app.tests.contract.test_contract_type import TestContractType
from app.modules.common.schema.base_schema import BaseFaker


class TestContract:
    default_contract: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="create_contract",
    )
    async def test_create_contract(self, client: AsyncClient):

        response = await client.post(
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
                "num_invoices": 0,
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
        contract_id = self.default_contract["contract_id"]

        response = await client.get(f"/contract/{contract_id}")

        assert response.status_code == 200
        assert response.json()["data"]["contract_id"] == contract_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_contract_by_id"], name="update_contract_by_id"
    )
    async def test_update_contract(self, client: AsyncClient):
        contract_id = self.default_contract["contract_id"]

        response = await client.put(
            f"/contract/{contract_id}",
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
                        "contract_id": contract_id,
                        "property_unit_assoc": TestProperties.default_property.get(
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

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_contract_by_id"], name="delete_contract_by_id"
    )
    async def test_delete_contract(self, client: AsyncClient):
        contract_id = self.default_contract["contract_id"]

        response = await client.delete(f"/contract/{contract_id}")
        assert response.status_code == 204

        # Verify the contract is deleted
        response = await client.get(f"/contract/{contract_id}")
        assert response.status_code == 404
        assert response.json()["data"] == None
