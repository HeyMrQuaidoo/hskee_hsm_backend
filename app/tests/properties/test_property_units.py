import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestUnits:
    default_unit: Dict[str, Any] = {}
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
        TestUnits.default_utility = utility

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

        TestUnits.default_property = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_property"], name="create_unit")
    async def test_create_unit(self, client: AsyncClient):
        media_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="

        # get utilities
        response_utility = await client.get(
            "/utilities/", params={"limit": 10, "offset": 0}
        )
        utility = response_utility.json()["data"][0]

        response = await client.post(
            "/units/",
            json={
                "property_id": TestUnits.default_property["property_unit_assoc_id"],
                "property_unit_code": "string",
                "property_unit_floor_space": 0,
                "property_unit_amount": 0,
                "property_floor_id": 0,
                "property_unit_notes": "string",
                "property_status": "available",
                "property_unit_security_deposit": 0,
                "property_unit_commission": 0,
                "has_amenities": False,
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
                        "media": [],
                    }
                ],
                "utilities": [
                    {
                        "billable_id": utility.get("utility_id"),
                        "payment_type": "one_time",
                        "billable_amount": 200,
                        "apply_to_units": False,
                    }
                ],
            },
        )
        assert response.status_code == 200
        TestUnits.default_unit = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_units(self, client: AsyncClient):
        response = await client.get("/units/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_unit"], name="get_unit_by_id")
    async def test_get_unit_by_id(self, client: AsyncClient):
        unit_id = self.default_unit["property_unit_assoc_id"]

        response = await client.get(f"/units/{unit_id}")

        assert response.status_code == 200
        assert response.json()["data"]["property_unit_assoc_id"] == unit_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_unit_by_id"], name="update_unit_by_id")
    async def test_update_unit(self, client: AsyncClient):
        unit_id = self.default_unit["property_unit_assoc_id"]

        response = await client.put(
            f"/units/{unit_id}",
            json={
                "property_id": TestUnits.default_property["property_unit_assoc_id"],
                "property_unit_code": "updated_code",
                "property_unit_floor_space": 100,
                "property_unit_amount": 1000,
                "property_floor_id": 1,
                "property_unit_notes": "updated notes",
                "property_status": "available",
                "property_unit_security_deposit": 500,
                "property_unit_commission": 200,
                "property_unit_assoc_id": unit_id,
                "has_amenities": True,
                "media": [],
                "amenities": [],
                "utilities": [
                    {
                        "billable_id": TestUnits.default_utility.get("utility_id"),
                        "payment_type": "one_time",
                        "billable_amount": 200,
                        "apply_to_units": False,
                    }
                ],
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["property_unit_code"] == "updated_code"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["update_unit_by_id"], name="delete_unit_by_id")
    async def test_delete_unit(self, client: AsyncClient):
        unit_id = self.default_unit["property_unit_assoc_id"]

        response = await client.delete(f"/units/{unit_id}")
        assert response.status_code == 204

        # Verify the unit is deleted
        response = await client.get(f"/units/{unit_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["delete_unit_by_id"], name="delete_property_by_id")
    async def test_delete_property(self, client: AsyncClient):
        property_id = self.default_property["property_unit_assoc_id"]

        response = await client.delete(f"/property/{property_id}")
        assert response.status_code == 204

        # Verify the property is deleted
        response = await client.get(f"/property/{property_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
