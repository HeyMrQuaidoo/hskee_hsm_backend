import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestTransaction:
    default_invoice: Dict[str, Any] = {}
    default_transaction: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_invoice")
    async def test_create_invoice(self, client: AsyncClient):
        response = await client.post(
            "/invoice/",
            json={
                "issued_by": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "issued_to": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",
                "due_date": "2024-07-31T23:59:59",
                "status": "pending",
                "invoice_items": [
                    {
                        "name": "Item 1",
                        "amount": 0,
                        "unit_price": 200,
                        "total_price": 200,
                        "quantity": 1,
                    }
                ],
                "invoice_type": "general",
            },
        )
        assert response.status_code == 200

        TestTransaction.default_invoice = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_invoice"], name="create_transaction")
    async def test_create_transaction(self, client: AsyncClient):
        response = await client.post(
            "/transaction/",
            json={
                "payment_method": "one_time",
                "client_offered": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "client_requested": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",
                "transaction_date": "2024-07-31T23:59:59",
                "transaction_details": "Payment for services",
                "transaction_type": "credit_card",
                "transaction_status": "pending",
                "invoice_number": self.default_invoice["invoice_number"],
            },
        )

        assert response.status_code == 200

        TestTransaction.default_transaction = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_transactions(self, client: AsyncClient):
        response = await client.get("/transaction/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["create_transaction"], name="get_transaction_by_id"
    )
    async def test_get_transaction_by_id(self, client: AsyncClient):
        transaction_number = self.default_transaction["transaction_number"]

        response = await client.get(f"/transaction/{transaction_number}")

        assert response.status_code == 200
        assert response.json()["data"]["transaction_number"] == transaction_number

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["get_transaction_by_id"], name="update_transaction_by_id"
    )
    async def test_update_transaction(self, client: AsyncClient):
        transaction_number = self.default_transaction["transaction_number"]

        response = await client.put(
            f"/transaction/{transaction_number}",
            json={
                "payment_method": "one_time",
                "client_offered": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "client_requested": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",
                "transaction_date": "2024-07-31T23:59:59",
                "transaction_details": "Payment for services",
                "transaction_type": "credit_card",
                "transaction_status": "completed",
                "transaction_number": self.default_transaction["transaction_number"],
                "invoice_number": self.default_invoice["invoice_number"],
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["transaction_status"] == "completed"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["update_transaction_by_id"], name="delete_transaction_by_id"
    )
    async def test_delete_transaction(self, client: AsyncClient):
        transaction_number = self.default_transaction["transaction_number"]

        response = await client.delete(f"/transaction/{transaction_number}")
        assert response.status_code == 204

        # Verify the transaction is deleted
        response = await client.get(f"/transaction/{transaction_number}")
        assert response.status_code == 200
        assert response.json()["data"] == {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["delete_transaction_by_id"], name="delete_invoice_by_id"
    )
    async def test_delete_invoice(self, client: AsyncClient):
        invoice_number = self.default_invoice["invoice_number"]

        response = await client.delete(f"/invoice/{invoice_number}")
        assert response.status_code == 204

        # Verify the invoice is deleted
        response = await client.get(f"/invoice/{invoice_number}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
