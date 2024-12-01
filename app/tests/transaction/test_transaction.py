import pytest
from typing import Any, Dict
from datetime import datetime, timezone
from httpx import AsyncClient
from app.tests.invoice.test_invoice import TestInvoice
from app.tests.payment_type.test_payment_type import TestPaymentType
from app.tests.transaction.test_transaction_type import TestTransactionType
from app.tests.users.test_users import TestUsers


class TestTransaction:
    default_transaction: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[],
        name="create_transaction",
    )
    async def test_create_transaction(self, client: AsyncClient):
        # Ensure the invoice is created and available
        # invoice_number = TestInvoice.default_invoice.get("invoice_number")
        # assert (
        #     invoice_number
        # ), "Invoice number is not set. Ensure the invoice creation test runs first."

        print("TransactionTyep:", TestTransactionType.default_transaction_type)
        response = await client.post(
            "/transaction/",
            json={
                "payment_method": "one_time",
                "payment_type_id": TestPaymentType.default_payment_type.get(
                    "payment_type_id"
                ),
                "client_offered": TestUsers.default_user.get("user_id"),
                "client_requested": TestUsers.default_user.get("user_id"),
                "transaction_date": "2024-07-31T23:59:59",
                "transaction_details": "Payment for services",
                "transaction_type": TestTransactionType.default_transaction_type.get(
                    "transaction_type_id"
                ),
                "transaction_status": "pending",
                "invoice_number": TestInvoice.default_invoice.get("invoice_number"),
                "amount_gte": 150.00,
            },
        )
        assert (
            response.status_code == 201
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
    async def test_filter_transactions_by_amount2(self, client: AsyncClient):
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
        # Define a UTC timezone for comparisons
        utc = timezone.utc

        # Test filtering transactions by date greater than or equal
        response = await client.get(
            "/transaction/",
            params={
                "date_gte": "2024-07-01T00:00:00+00:00"
            },  # Use ISO 8601 format with timezone
        )
        assert response.status_code == 200
        data = response.json()
        assert all(
            datetime.fromisoformat(tx["transaction_date"])
            >= datetime(2024, 7, 1, tzinfo=utc)
            for tx in data["data"]
        )

        # Test filtering transactions by date less than or equal
        response = await client.get(
            "/transaction/",
            params={
                "date_lte": "2024-07-31T23:59:59+00:00"
            },  # Use ISO 8601 format with timezone
        )
        assert response.status_code == 200
        data = response.json()
        assert all(
            datetime.fromisoformat(tx["transaction_date"])
            <= datetime(2024, 7, 31, 23, 59, 59, tzinfo=utc)
            for tx in data["data"]
        )

    @pytest.mark.asyncio(loop_scope="session")
    async def test_filter_transactions_by_transaction_type(self, client: AsyncClient):
        response = await client.get(
            "/transaction/", params={"transaction_type": 1}
        )  # Use integer ID
        assert response.status_code == 200
        data = response.json()
        assert all(tx["transaction_type"] == 1 for tx in data["data"])

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=[], name="get_transaction_by_id")
    async def test_get_transaction_by_id(self, client: AsyncClient):
        print("Default Transaction", TestTransaction.default_transaction)
        transaction_id = TestTransaction.default_transaction["transaction_id"]

        response = await client.get(f"/transaction/{transaction_id}")

        assert response.status_code == 200
        assert response.json()["data"]["transaction_id"] == transaction_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=[], name="update_transaction_by_id")
    async def test_update_transaction(self, client: AsyncClient):
        transaction_id = TestTransaction.default_transaction["transaction_id"]
        print("Default Invoice", TestInvoice.default_invoice)

        response = await client.put(
            f"/transaction/{transaction_id}",
            json={
                "payment_method": "one_time",
                "client_offered": TestUsers.default_user.get("user_id"),
                "client_requested": TestUsers.default_user.get("user_id"),
                "transaction_date": "2024-07-31T23:59:59",
                "transaction_details": "Updated payment details",
                "transaction_type": TestTransactionType.default_transaction_type.get(
                    "transaction_type_id"
                ),
                "transaction_status": "completed",
                "invoice_number": TestInvoice.default_invoice["invoice_number"],
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["transaction_status"] == "completed"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_transaction_by_id"], name="delete_transaction_by_id"
    )
    async def test_delete_transaction(self, client: AsyncClient):
        transaction_id = TestTransaction.default_transaction["transaction_id"]

        response = await client.delete(f"/transaction/{transaction_id}")
        assert response.status_code == 204

        # Verify the transaction is deleted
        response = await client.get(f"/transaction/{transaction_id}")
        assert response.status_code == 404
        assert response.json()["data"] == None
