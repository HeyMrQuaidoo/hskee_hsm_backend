import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.users.test_users import TestUsers


class TestInvoice:
    default_invoice: Dict[str, Any] = {}
    default_user: Dict[str, Any] = TestUsers.default_user

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_invoice")
    async def test_create_invoice(self, client: AsyncClient):
        response = await client.post(
            "/invoice/",
            json={
                "issued_by": TestInvoice.default_user.get("user_id"),
                "issued_to": TestInvoice.default_user.get("user_id"),
                "invoice_details": "Test invoice for services rendered",
                "invoice_amount": 1500.50,
                "due_date": "2024-06-23T19:11:07.570Z",
                "date_paid": "2024-06-24T19:11:07.570Z",
                "invoice_type": "standard", 
                "status": "pending", 
                "invoice_items": [
                    {
                        "description": "Item 1 - Consulting service",
                        "quantity": 2,
                        "unit_price": 750.25,
                        "reference_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", 
                    },
                    {
                        "description": "Item 2 - Support service",
                        "quantity": 1,
                        "unit_price": 500,
                        "reference_id": "f1e2d3c4-b5a6-7890-cbda-ab1234567890", 
                    }
                ]
            },
        )
        assert response.status_code == 201, f"Failed with response: {response.text}"
        TestInvoice.default_invoice = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_invoices(self, client: AsyncClient):
        response = await client.get("/invoice/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_invoice"], name="get_invoice_by_id")
    async def test_get_invoice_by_id(self, client: AsyncClient):
        invoice_number = self.default_invoice["invoice_number"]

        response = await client.get(f"/invoice/{invoice_number}")

        assert response.status_code == 200
        assert response.json()["data"]["invoice_number"] == invoice_number

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_invoice_by_id"], name="update_invoice_by_id")
    async def test_update_invoice(self, client: AsyncClient):
        invoice_number = self.default_invoice["invoice_number"]
        invoice_items = self.default_invoice["invoice_items"][0]

        response = await client.put(
            f"/invoice/{invoice_number}",
            json={
                "issued_by": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "issued_to": "4dbc3019-1884-4a0d-a2e6-feb12d83186e",
                "due_date": "2024-07-31T23:59:59",
                "status": "pending",
                "invoice_details": "Updated consulting services for July 2024",
                "invoice_items": [
                    {
                        "invoice_item_id": invoice_items["invoice_item_id"],
                        "name": "Item 2",
                        "amount": 100,
                        "unit_price": 10,
                        "total_price": 10,
                        "quantity": 1,
                        "description": "Updated consulting services and utilities for the month of June 2024",
                    }
                ],
                "invoice_type": "general",
            },
        )
        assert response.status_code == 200
        assert (
            response.json()["data"]["invoice_items"][0]["description"]
            == "Updated consulting services and utilities for the month of June 2024"
        )

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_invoice_by_id"], name="delete_invoice_by_id"
    )
    async def test_delete_invoice(self, client: AsyncClient):
        invoice_number = self.default_invoice["invoice_number"]

        response = await client.delete(f"/invoice/{invoice_number}")
        assert response.status_code == 204

        # Verify the invoice is deleted
        response = await client.get(f"/invoice/{invoice_number}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
