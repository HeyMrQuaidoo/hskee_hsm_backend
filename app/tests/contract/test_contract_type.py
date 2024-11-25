import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestContractType:
    default_contract_type: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_contract_type")
    async def test_create_contract_type(self, client: AsyncClient):
        # Check if the contract type already exists and delete it if found
        check_response = await client.get(
            "/contract-type/", params={"contract_type_name": "lease"}
        )
        print("Contract response", check_response.text)
        if check_response.status_code == 200 and check_response.json().get("data"):
            existing_contract_type = check_response.json()["data"][0]
            contract_type_id = existing_contract_type.get("contract_type_id")
            if contract_type_id:
                delete_response = await client.delete(
                    f"/contract-type/{contract_type_id}"
                )
                assert delete_response.status_code in [
                    200,
                    204,
                ], f"Failed to delete existing contract type: {delete_response.text}"

        # Proceed to create a new contract type
        response = await client.post(
            "/contract-type/",
            json={
                "contract_type_name": "lease",
                "fee_percentage": 20,
            },
        )
        assert (
            response.status_code == 201
        ), f"Failed to create contract type: {response.text}"
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
        print("Contract Type is", self.default_contract_type)
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

    # @pytest.mark.asyncio(loop_scope="session")
    # @pytest.mark.dependency(
    #     depends=["test_create_contract_type"], name="delete_contract_type_by_id"
    # )
    # async def test_delete_contract_type(self, client: AsyncClient):
    #     contract_type_id = self.default_contract_type["contract_type_id"]

    #     response = await client.delete(f"/contract-type/{contract_type_id}")
    #     assert response.status_code == 204

    #     # Verify the contract type is deleted
    #     response = await client.get(f"/contract-type/{contract_type_id}")
    #     assert response.status_code == 404
