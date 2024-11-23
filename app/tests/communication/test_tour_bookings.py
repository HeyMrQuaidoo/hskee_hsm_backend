import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.properties.test_property import TestProperties
from app.tests.users.test_users import TestUsers
from datetime import datetime, timedelta

class TestTourBookings:
    default_tour: Dict[str, Any] = {}
    tour_list: Dict[str, Any] = {}
    future_date = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["TestProperties::create_property", "TestUsers::create_user"],
        name="TestTourBookings::create_tour_booking",
    )
    async def test_create_tour_booking(self, client: AsyncClient):
        response = await client.post(
            "/tour/",
            json={
                "name": "John Doe",
                "email": "johndoe@example.com",
                "phone_number": "1234567890",
                "tour_type": "in_person",
                "status": "incoming",
                "tour_date": self.future_date,
                "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
                "user_id": TestUsers.default_user.get("user_id"),
            },
        )
        assert response.status_code == 201, f"Tour creation failed: {response.text}"
        TestTourBookings.default_tour = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestTourBookings::create_tour_booking"], name="TestTourBookings::create_additional_tours")
    async def test_create_additional_tours(self, client: AsyncClient):
        # Create additional tours for filtering tests
        tour_data_list = [
            {
                "name": "Jane Smith",
                "email": "janesmith@example.com",
                "phone_number": "0987654321",
                "tour_type": "virtual",
                "status": "confirmed",
                "tour_date": (datetime.now() + timedelta(days=1)).isoformat() + 'Z',
                "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
                "user_id": TestUsers.default_user.get("user_id"),
            },
            {
                "name": "Alice Johnson",
                "email": "alicejohnson@example.com",
                "phone_number": "5551234567",
                "tour_type": "in_person",
                "status": "completed",
                "tour_date": (datetime.now() - timedelta(days=1)).isoformat() + 'Z',
                "property_unit_assoc_id": TestProperties.default_property.get("property_unit_assoc_id"),
                "user_id": TestUsers.default_user.get("user_id"),
            },
        ]

        for tour_data in tour_data_list:
            response = await client.post("/tour/", json=tour_data)
            assert response.status_code == 201, f"Additional tour creation failed: {response.text}"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=
                            ["TestTourBookings::create_additional_tours"], 
                            name="TestTourBookings::get_all_tour_bookings")
    async def test_get_all_tour_bookings(self, client: AsyncClient):
        response = await client.get("/tour/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to fetch tours: {response.text}"
        print("Response: ", response)
        data = response.json()["data"]
        assert isinstance(data, list)
        assert len(data) >= 3, "Expected at least 3 tours"
        TestTourBookings.tour_list = data

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestTourBookings::create_tour_booking"], name="TestTourBookings::get_tour_booking_by_id")
    async def test_get_tour_booking_by_id(self, client: AsyncClient):
        tour_id = self.default_tour["tour_booking_id"]
        response = await client.get(f"/tour/{tour_id}")
        assert response.status_code == 200, f"Failed to get tour by ID: {response.text}"
        assert response.json()["data"]["tour_booking_id"] == tour_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestTourBookings::get_tour_booking_by_id"], name="TestTourBookings::update_tour_booking_by_id")
    async def test_update_tour_booking(self, client: AsyncClient):
        tour_id = self.default_tour["tour_booking_id"]
        new_date = (datetime.now() + timedelta(days=14)).isoformat() + 'Z'
        response = await client.put(
            f"/tour/{tour_id}",
            json={
                "status": "confirmed",
                "tour_date": new_date,
            },
        )
        assert response.status_code == 200, f"Tour update failed: {response.text}"
        assert response.json()["data"]["status"] == "confirmed"
        assert response.json()["data"]["tour_date"] == new_date

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestTourBookings::create_tour_booking"], name="TestTourBookings::filter_tours")
    async def test_filter_tours(self, client: AsyncClient):
        # Filter by status
        response = await client.get("/tour/", params={"status": "confirmed"})
        assert response.status_code == 200, f"Failed to filter tours by status: {response.text}"
        data = response.json()["data"]
        assert all(tour["status"] == "confirmed" for tour in data), "Filtering by status failed"

        # Filter by tour_type
        response = await client.get("/tour/", params={"tour_type": "virtual"})
        assert response.status_code == 200, f"Failed to filter tours by tour_type: {response.text}"
        data = response.json()["data"]
        assert all(tour["tour_type"] == "virtual" for tour in data), "Filtering by tour_type failed"

        # Filter by date range
        start_date = (datetime.now() - timedelta(days=2)).isoformat() + 'Z'
        end_date = (datetime.now() + timedelta(days=2)).isoformat() + 'Z'
        response = await client.get("/tour/", params={"date_gte": start_date, "date_lte": end_date})
        assert response.status_code == 200, f"Failed to filter tours by date range: {response.text}"
        data = response.json()["data"]
        assert len(data) > 0, "Expected at least one tour in the date range"

        # Filter by user_id
        user_id = TestUsers.default_user.get("user_id")
        response = await client.get("/tour/", params={"user_id": user_id})
        assert response.status_code == 200, f"Failed to filter tours by user_id: {response.text}"
        data = response.json()["data"]
        assert all(tour["user_id"] == user_id for tour in data), "Filtering by user_id failed"

        # Filter by email
        response = await client.get("/tour/", params={"email": "janesmith@example.com"})
        assert response.status_code == 200, f"Failed to filter tours by email: {response.text}"
        data = response.json()["data"]
        assert all("janesmith@example.com" in tour["email"] for tour in data), "Filtering by email failed"

        # Filter by name
        response = await client.get("/tour/", params={"name": "Alice"})
        assert response.status_code == 200, f"Failed to filter tours by name: {response.text}"
        data = response.json()["data"]
        assert all("Alice" in tour["name"] for tour in data), "Filtering by name failed"

        # Filter by phone_number
        response = await client.get("/tour/", params={"phone_number": "555"})
        assert response.status_code == 200, f"Failed to filter tours by phone_number: {response.text}"
        data = response.json()["data"]
        assert all("555" in tour["phone_number"] for tour in data), "Filtering by phone_number failed"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestTourBookings::update_tour_booking_by_id"], name="TestTourBookings::delete_tour_booking_by_id")
    async def test_delete_tour_booking(self, client: AsyncClient):
        tour_id = self.default_tour["tour_booking_id"]
        response = await client.delete(f"/tour/{tour_id}")
        assert response.status_code == 204, f"Tour deletion failed: {response.text}"

        # Verify that the tour booking is deleted
        response = await client.get(f"/tour/{tour_id}")
        assert response.status_code == 200, f"Failed to get tour by ID after deletion: {response.text}"
        assert response.json()["data"] == {}
