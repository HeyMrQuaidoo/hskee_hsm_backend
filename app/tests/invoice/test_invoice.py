import pytest
from typing import Any, Dict
from httpx import AsyncClient
from faker import Faker



class TestInvoice:
    default_user: Dict[str, Any] = {}
    faker = Faker()

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[], name="TestInvoice::create_invoice"
    )
    async def test_create_invoice(self, client: AsyncClient):
        # Ensure the user is created and available
        user_response = await client.post(
            "/users/",
            json={
                "date_of_birth": "1985-05-20",
                "first_name": "John",
                "last_name": "Doe",
                "email": self.faker.unique.email(),
                "phone_number": self.faker.phone_number(),
                "identification_number": str(
                    self.faker.random_number(digits=6, fix_len=True)
                ),
                "photo_url": "",
                "gender": "male",
                "address": [
                    {
                        "address_type": "billing",
                        "primary": True,
                        "address_1": self.faker.street_address(),
                        "address_2": self.faker.secondary_address(),
                        "city": self.faker.city(),
                        "region": self.faker.state_abbr(),
                        "country": "USA",
                        "address_postalcode": self.faker.postcode(),
                    }
                ],
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": self.faker.uuid4(),
                    "verification_token": self.faker.uuid4(),
                    "is_subscribed_token": self.faker.uuid4(),
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": "2024-07-21T20:52:37.078064",
                    "last_login_time": "2024-07-21T21:21:38.279Z",
                },
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_email": self.faker.unique.email(),
                    "emergency_contact_relation": "Sister",
                    "emergency_contact_number": self.faker.phone_number(),
                },
                "user_employer_info": {
                    "employer_name": self.faker.company(),
                    "occupation_status": "Employed",
                    "occupation_location": self.faker.city(),
                },
                "role": "user",
            },
        )
        assert user_response.status_code == 201, f"User creation failed: {user_response.text}"

        # Save the created user data for future tests
        self.default_user = user_response.json()["data"]

        user_id = self.default_user.get("user_id")
        assert user_id, "User ID is not set. Ensure the user creation test runs first."

        response = await client.post(
            "/invoice/",
            json={
                "issued_by": user_id,
                "issued_to": user_id,
                "invoice_details": "Test invoice for services rendered",
                "invoice_amount": 1500.50,
                "due_date": "2024-06-23T19:11:07.570Z",
                "date_paid": "2024-06-24T19:11:07.570Z",
                "invoice_type": "general",
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
                    },
                ],
            },
        )
        assert response.status_code == 201, f"Failed with response: {response.text}"
        TestInvoice.default_invoice = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_invoices(self, client: AsyncClient):
        response = await client.get("/invoice/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        print(
            "Response is", response.json(), "response type is:", type(response.json())
        )
        assert isinstance(response.json(), list)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["TestInvoice::create_invoice"], name="get_invoice_by_id"
    )
    async def test_get_invoice_by_id(self, client: AsyncClient):
        print("Default invoice here", TestInvoice.default_invoice)
        invoice_number = TestInvoice.default_invoice["invoice_number"]

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
                "issued_by": self.default_user.get("user_id"),
                "issued_to": self.default_user.get("user_id"),
                "due_date": "2024-07-31T23:59:59",
                "status": "pending",
                "invoice_amount": 0,
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
            "Updated consulting services and utilities for the month of June 2024"
            in (
                response.json()["data"]["invoice_items"][0]["description"],
                response.json()["data"]["invoice_items"][1]["description"],
            )
        )

    # @pytest.mark.asyncio(loop_scope="session")
    # @pytest.mark.dependency(
    #     depends=["update_invoice_by_id"], name="delete_invoice_by_id"
    # )
    # async def test_delete_invoice(self, client: AsyncClient):
    #     invoice_number = self.default_invoice["invoice_number"]

    #     response = await client.delete(f"/invoice/{invoice_number}")
    #     assert response.status_code == 204

    #     # Verify the invoice is deleted
    #     response = await client.get(f"/invoice/{invoice_number}")
    #     assert response.status_code == 404
