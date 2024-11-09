import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestContractType:
    default_contract_type: Dict[str, Any] = {}


    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_contract_type")
    async def test_create_contract_type(self, client: AsyncClient):
        response = await client.post(
            "/contract-type/",
            json={
                "contract_type_name": "rent",
                "fee_percentage": 20,
            },
        )
        assert response.status_code == 201
        TestContractType.default_contract_type = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_contract_types(self, client: AsyncClient):
        response = await client.get(
            "/contract-type/", params={"limit": 10, "offset": 0}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_contract_type"], name="get_contract_type_by_id"
    )
    async def test_get_contract_type_by_id(self, client: AsyncClient):
        contract_type_id = self.default_contract_type["contract_type_id"]

        response = await client.get(f"/contract-type/{contract_type_id}")

        assert response.status_code == 200
        assert response.json()["data"]["contract_type_id"] == contract_type_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_contract_type_by_id"], name="update_contract_type_by_id"
    )
    async def test_update_contract_type(self, client: AsyncClient):
        contract_type_id = self.default_contract_type["contract_type_id"]

        response = await client.put(
            f"/contract-type/{contract_type_id}",
            json={"contract_type_name": "lease", "fee_percentage": 5},
        )
        assert response.status_code == 200
        assert response.json()["data"]["contract_type_name"] == "lease"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_contract_type_by_id"], name="delete_contract_type_by_id"
    )
    async def test_delete_contract_type(self, client: AsyncClient):
        contract_type_id = self.default_contract_type["contract_type_id"]

        response = await client.delete(f"/contract-type/{contract_type_id}")
        assert response.status_code == 204

        # Verify the contract type is deleted
        response = await client.get(f"/contract-type/{contract_type_id}")
        assert response.status_code == 404
