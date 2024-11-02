# import pytest
# from typing import Any, Dict
# from httpx import AsyncClient

# class TestPropertyTours:
#     default_property_tour: Dict[str, Any] = {}

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(name="create_property_tour")
#     async def test_create_property_tour(self, client: AsyncClient):
#         response = await client.post(
#             "/tour_booking/",
#             json={
#                 "name": "John Doe",
#                 "email": "john@example.com",
#                 "phone_number": "123-456-7890",
#                 "tour_type": "in_person",
#                 "status": "incoming",
#                 "tour_date": "2024-07-21T21:28:44.207Z",
#                 "property_unit_assoc_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
#             },
#         )
#         assert response.status_code == 200

#         TestPropertyTours.default_property_tour = response.json()["data"]

#     @pytest.mark.asyncio(scope="session")
#     async def test_get_all_property_tours(self, client: AsyncClient):
#         response = await client.get("/tour_booking/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["create_property_tour"], name="get_property_tour_by_id")
#     async def test_get_property_tour_by_id(self, client: AsyncClient):
#         property_tour_id = self.default_property_tour["property_tour_id"]

#         response = await client.get(f"/tour_booking/{property_tour_id}")

#         assert response.status_code == 200
#         assert response.json()["data"]["property_tour_id"] == property_tour_id

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["get_property_tour_by_id"], name="update_property_tour_by_id")
#     async def test_update_property_tour(self, client: AsyncClient):
#         property_tour_id = self.default_property_tour["property_tour_id"]

#         response = await client.put(
#             f"/tour_booking/{property_tour_id}",
#             json={
#                 "name": "Jane Doe",
#                 "email": "jane@example.com",
#                 "phone_number": "987-654-3210",
#                 "tour_type": "virtual",
#                 "status": "completed",
#                 "tour_date": "2024-07-21T21:28:44.207Z",
#                 "property_unit_assoc_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#                 "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
#             },
#         )
#         assert response.status_code == 200
#         assert response.json()["data"]["name"] == "Jane Doe"

#     @pytest.mark.asyncio(scope="session")
#     @pytest.mark.dependency(depends=["update_property_tour_by_id"], name="delete_property_tour_by_id")
#     async def test_delete_property_tour(self, client: AsyncClient):
#         property_tour_id = self.default_property_tour["property_tour_id"]

#         response = await client.delete(f"/tour_booking/{property_tour_id}")
#         assert response.status_code == 204

#         # Verify the property tour is deleted
#         response = await client.get(f"/tour_booking/{property_tour_id}")
#         assert response.status_code == 404
