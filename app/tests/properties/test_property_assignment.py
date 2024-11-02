import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestPropertyAssignment:
    default_property_assignment: Dict[str, Any] = {}
    default_property: Dict[str, Any] = {}
    default_utility: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_property")
    async def test_create_property(self, client: AsyncClient):
        media_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="

        response_utility = await client.get(
            "/utilities/", params={"limit": 10, "offset": 0}
        )
        utility = response_utility.json()["data"][0]
        TestPropertyAssignment.default_utility = utility

        response = await client.post(
            "/property/",
            json={
                "name": "Baeta Heights 2",
                "property_type": "residential",
                "amount": 90800,
                "security_deposit": 6600,
                "commission": 5555,
                "floor_space": 224,
                "num_units": 4,
                "num_bathrooms": 5,
                "num_garages": True,
                "has_balconies": False,
                "has_parking_space": False,
                "pets_allowed": True,
                "description": "description",
                "property_status": "available",
                "address": {
                    "address_type": "billing",
                    "primary": True,
                    "address_1": "line 1",
                    "address_2": "line 2",
                    "city": "Tema",
                    "region": "Greater Accra",
                    "country": "Ghana",
                    "address_postalcode": "",
                },
                "media": [
                    {
                        "media_name": "property_image",
                        "media_type": "png",
                        "content_url": media_image,
                    }
                ],
                "amenities": [
                    {
                        "amenity_name": "Air Conditioning",
                        "amenity_short_name": "Air Conditioning",
                        "amenity_value_type": "boolean",
                        "description": "no notes needed",
                        "media": [
                            {
                                "media_name": "ammenity_image",
                                "media_type": "png",
                                "content_url": media_image,
                            }
                        ],
                    }
                ],
                "utilities": [
                    {
                        "payment_type": "one_time",
                        "billable_amount": "100",
                        "apply_to_units": False,
                        "billable_id": utility.get("utility_id"),
                    }
                ],
            },
        )
        assert response.status_code == 200

        TestPropertyAssignment.default_property = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_property"], name="create_property_assignment"
    )
    async def test_create_property_assignment(self, client: AsyncClient):
        response = await client.post(
            "/property_assignment/",
            json={
                "property_unit_assoc_id": self.default_property[
                    "property_unit_assoc_id"
                ],
                "user_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "assignment_type": "landlord",
                "date_from": "2024-07-21T21:28:08.506",
                "date_to": "2024-07-21T21:28:08.506",
                "notes": "assign new user",
            },
        )
        assert response.status_code == 200

        TestPropertyAssignment.default_property_assignment = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_property_assignments(self, client: AsyncClient):
        response = await client.get(
            "/property_assignment/", params={"limit": 10, "offset": 0}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_property_assignment"], name="get_property_assignment_by_id"
    )
    async def test_get_property_assignment_by_id(self, client: AsyncClient):
        property_assignment_id = self.default_property_assignment[
            "property_assignment_id"
        ]

        response = await client.get(f"/property_assignment/{property_assignment_id}")

        assert response.status_code == 200
        assert (
            response.json()["data"]["property_assignment_id"] == property_assignment_id
        )

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_property_assignment_by_id"],
        name="update_property_assignment_by_id",
    )
    async def test_update_property_assignment(self, client: AsyncClient):
        property_assignment_id = self.default_property_assignment[
            "property_assignment_id"
        ]

        response = await client.put(
            f"/property_assignment/{property_assignment_id}",
            json={
                "property_unit_assoc_id": self.default_property[
                    "property_unit_assoc_id"
                ],
                "user_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
                "assignment_type": "handler",
                "date_from": "2024-07-21T21:28:08.506",
                "date_to": "2024-07-21T21:28:08.506",
                "notes": "updated notes",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["assignment_type"] == "handler"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_property_assignment_by_id"],
        name="delete_property_assignment_by_id",
    )
    async def test_delete_property_assignment(self, client: AsyncClient):
        property_assignment_id = self.default_property_assignment[
            "property_assignment_id"
        ]

        response = await client.delete(f"/property_assignment/{property_assignment_id}")
        assert response.status_code == 204

        # Verify the property assignment is deleted
        response = await client.get(f"/property_assignment/{property_assignment_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["delete_property_assignment_by_id"], name="delete_property_by_id"
    )
    async def test_delete_property(self, client: AsyncClient):
        property_id = self.default_property["property_unit_assoc_id"]

        response = await client.delete(f"/property/{property_id}")
        assert response.status_code == 204

        # Verify the property is deleted
        response = await client.get(f"/property/{property_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
