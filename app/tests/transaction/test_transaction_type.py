import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestTransactionType:
    default_transaction_type: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_transaction_type")
    async def test_create_transaction_type(self, client: AsyncClient):
        # Define the transaction type details
        transaction_type_name = "prepaid_card"
        transaction_type_description = "Payment via prepaid card"

        # Check if a transaction type with the given name already exists
        response = await client.get(
            "/transaction-type/", params={"limit": 10, "offset": 0}
        )
        if response.status_code == 200:
            existing_transaction_types = response.json().get("data", [])
            for transaction_type in existing_transaction_types:
                if transaction_type["transaction_type_name"] == transaction_type_name:
                    # Use transaction_type_id for deletion
                    transaction_type_id = transaction_type["transaction_type_id"]
                    delete_response = await client.delete(
                        f"/transaction-type/{transaction_type_id}"
                    )
                    assert delete_response.status_code in [200, 204], (
                        f"Failed to delete existing transaction type: "
                        f"{delete_response.text}"
                    )

        # Create the new transaction type
        response = await client.post(
            "/transaction-type/",
            json={
                "transaction_type_name": transaction_type_name,
                "transaction_type_description": transaction_type_description,
            },
        )
        assert response.status_code == 201
        TestTransactionType.default_transaction_type = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_transaction_types(self, client: AsyncClient):
        response = await client.get(
            "/transaction-type/", params={"limit": 10, "offset": 0}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_transaction_type"], name="get_transaction_type_by_id"
    )
    async def test_get_transaction_type_by_id(self, client: AsyncClient):
        transaction_type_id = self.default_transaction_type["transaction_type_id"]

        response = await client.get(f"/transaction-type/{transaction_type_id}")

        assert response.status_code == 200
        assert response.json()["data"]["transaction_type_id"] == transaction_type_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_transaction_type_by_id"], name="update_transaction_type_by_id"
    )
    async def test_update_transaction_type(self, client: AsyncClient):
        transaction_type_id = self.default_transaction_type["transaction_type_id"]

        response = await client.put(
            f"/transaction-type/{transaction_type_id}",
            json={
                "transaction_type_name": "prepaid_card",
                "transaction_type_description": "Sale transaction type",
            },
        )
        assert response.status_code == 200
        assert (
            response.json()["data"]["transaction_type_description"]
            == "Sale transaction type"
        )

    # @pytest.mark.asyncio(loop_scope="session")
    # @pytest.mark.dependency(
    #     depends=["update_transaction_type_by_id"], name="delete_transaction_type_by_id"
    # )
    # async def test_delete_transaction_type(self, client: AsyncClient):
    #     transaction_type_id = self.default_transaction_type["transaction_type_id"]

    #     response = await client.delete(f"/transaction-type/{transaction_type_id}")
    #     assert response.status_code == 204

    #     # Verify the transaction type is deleted
    #     response = await client.get(f"/transaction-type/{transaction_type_id}")
    #     assert response.status_code == 404
