import pytest
from typing import Any, Dict
from datetime import datetime
from httpx import AsyncClient
from app.tests.invoice.test_invoice import TestInvoice
from app.tests.transaction.test_transaction_type import TestTransactionType
from app.tests.users.test_users import TestUsers

class TestTransaction:
    default_transaction: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["TestInvoice::create_invoice",
                 "TestUsers::create_user", 
                "TestPaymentType::create_payment_type"], name="create_transaction"
    )
    async def test_create_transaction(self, client: AsyncClient):
        # Ensure the invoice is created and available
        invoice_number = TestInvoice.default_invoice.get("invoice_number")
        assert (
            invoice_number
        ), "Invoice number is not set. Ensure the invoice creation test runs first."

        response = await client.post(
            "/transaction/",
            json={
                "payment_method": "one_time",
                "client_offered": TestUsers.default_user.get("user_id"),
                "client_requested": TestUsers.default_user.get("user_id"),
                "transaction_date": "2024-07-31T23:59:59",
                "transaction_details": "Payment for services",
                "transaction_type": TestTransactionType.default_transaction_type.get("transaction_type_id"),  
                "transaction_status": "pending",
                "invoice_number": invoice_number,
                "amount_gte": 150.00,
            },
        )
        assert (
            response.status_code == 200
        ), f"Failed to create transaction: {response.text}"

        TestTransaction.default_transaction = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_transactions(self, client: AsyncClient):
        response = await client.get("/transaction/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert len(data["data"]) <= 10  # Ensuring the limit is respected

    @pytest.mark.asyncio(loop_scope="session")
    async def test_filter_transactions_by_amount(self, client: AsyncClient):
        # Test filtering transactions by amount greater than or equal
        response = await client.get("/transaction/", params={"amount_gte": 100})
        assert response.status_code == 200
        data = response.json()
        assert all(
            tx["invoice"] is not None and tx["invoice"]["invoice_amount"] >= 100
            for tx in data["data"]
            if tx.get("invoice") and tx["invoice"].get("invoice_amount") is not None
        )


    @pytest.mark.asyncio(loop_scope="session")
    async def test_filter_transactions_by_amount(self, client: AsyncClient):
        # Test filtering transactions by amount less than or equal
        response = await client.get("/transaction/", params={"amount_lte": 200})
        assert response.status_code == 200
        data = response.json()
        assert all(
            tx["invoice"] is not None and tx["invoice"]["invoice_amount"] <= 200
            for tx in data["data"]
            if tx.get("invoice") and tx["invoice"].get("invoice_amount") is not None
        )
        
    @pytest.mark.asyncio(loop_scope="session")
    async def test_filter_transactions_by_date(self, client: AsyncClient):
        # Test filtering transactions by date greater than or equal
        response = await client.get(
            "/transaction/",
            params={"date_gte": "2024-07-01T00:00:00"},
        )
        assert response.status_code == 200
        data = response.json()
        assert all(
            datetime.fromisoformat(tx["transaction_date"]) >= datetime(2024, 7, 1)
            for tx in data["data"]
        )

        # Test filtering transactions by date less than or equal
        response = await client.get(
            "/transaction/",
            params={"date_gte": "2024-07-01T00:00:00+00:00"},
        )
        assert response.status_code == 200
        data = response.json()
        assert all(
            datetime.fromisoformat(tx["transaction_date"]) <= datetime(2024, 7, 31, 23, 59, 59)
            for tx in data["data"]
        )

    @pytest.mark.asyncio(loop_scope="session")
    async def test_filter_transactions_by_transaction_type(self, client: AsyncClient):
        response = await client.get("/transaction/", params={"transaction_type": 1})  # Use integer ID
        assert response.status_code == 200
        data = response.json()
        assert all(tx["transaction_type"] == 1 for tx in data["data"])

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_transaction"], name="get_transaction_by_id"
    )
    async def test_get_transaction_by_id(self, client: AsyncClient):
        transaction_number = self.default_transaction["transaction_number"]

        response = await client.get(f"/transaction/{transaction_number}")

        assert response.status_code == 200
        assert response.json()["data"]["transaction_number"] == transaction_number

    @pytest.mark.asyncio(loop_scope="session")
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
                "transaction_details": "Updated payment details",
                "transaction_type": 1,
                "transaction_status": "completed",
                "transaction_number": transaction_number,
                "invoice_number": TestInvoice.default_invoice["invoice_number"],
                "amount_gte": 200.00,
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["transaction_status"] == "completed"
        assert response.json()["data"]["amount_gte"] == 200.00

    @pytest.mark.asyncio(loop_scope="session")
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

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["delete_transaction_by_id"], name="delete_invoice_by_id"
    )
    async def test_delete_invoice(self, client: AsyncClient):
        invoice_number = TestInvoice.default_invoice["invoice_number"]

        response = await client.delete(f"/invoice/{invoice_number}")
        assert response.status_code == 204

        # Verify the invoice is deleted
        response = await client.get(f"/invoice/{invoice_number}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
