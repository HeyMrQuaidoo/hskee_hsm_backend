import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestInvoice:
    default_invoice: Dict[str, Any] = {}

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
        TestInvoice.default_invoice = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_invoices(self, client: AsyncClient):
        response = await client.get("/invoice/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_invoice"], name="get_invoice_by_id")
    async def test_get_invoice_by_id(self, client: AsyncClient):
        invoice_number = self.default_invoice["invoice_number"]

        response = await client.get(f"/invoice/{invoice_number}")

        assert response.status_code == 200
        assert response.json()["data"]["invoice_number"] == invoice_number

    @pytest.mark.asyncio(scope="session")
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

    @pytest.mark.asyncio(scope="session")
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
