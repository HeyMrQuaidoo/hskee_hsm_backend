import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestPaymentType:
    default_payment_type: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_payment_type")
    async def test_create_payment_type(self, client: AsyncClient):
        response = await client.post(
            "/payment-type/",
            json={
                "payment_type_name": "partial_pay_four_month",
                "payment_type_description": "Pay every four months payment plan",
                "num_of_invoices": 3,
            },
        )
        assert response.status_code == 200

        TestPaymentType.default_payment_type = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_payment_types(self, client: AsyncClient):
        response = await client.get("/payment-type/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_payment_type"], name="get_payment_type_by_id"
    )
    async def test_get_payment_type_by_id(self, client: AsyncClient):
        payment_type_id = self.default_payment_type["payment_type_id"]

        response = await client.get(f"/payment-type/{payment_type_id}")

        assert response.status_code == 200
        assert response.json()["data"]["payment_type_id"] == payment_type_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_payment_type_by_id"], name="update_payment_type_by_id"
    )
    async def test_update_payment_type(self, client: AsyncClient):
        payment_type_id = self.default_payment_type["payment_type_id"]

        response = await client.put(
            f"/payment-type/{payment_type_id}",
            json={
                "payment_type_name": "recurring",
                "payment_type_description": "Recurring payment",
                "num_of_invoices": 12,
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["payment_type_name"] == "recurring"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_payment_type_by_id"], name="delete_payment_type_by_id"
    )
    async def test_delete_payment_type(self, client: AsyncClient):
        payment_type_id = self.default_payment_type["payment_type_id"]

        response = await client.delete(f"/payment-type/{payment_type_id}")
        assert response.status_code == 204

        # Verify the payment type is deleted
        response = await client.get(f"/payment-type/{payment_type_id}")
        assert response.status_code == 404
