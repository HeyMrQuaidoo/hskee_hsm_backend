import pytest
from typing import Any, Dict
from httpx import AsyncClient

from app.tests.properties.test_property import TestProperties
from app.tests.payment_type.test_payment_type import TestPaymentType
from app.tests.billable.test_utilities import TestUtilities

class TestUnits:
    default_units: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=[ 
            "TestProperties::test_create_property",
            "TestPaymentType::test_create_payment_type",
            "TestUtilities::test_create_utility"], name="create_unit")
    async def test_create_unit(self, client: AsyncClient):
        media_image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="

        response = await client.post(
            "/unit/",
            json={
                "property_id": TestProperties.default_property.get(
                    "property_unit_assoc_id", ""
                ),
                "property_unit_code": "Unit 101",
                "property_unit_floor_space": 100,
                "property_unit_amount": 1000,
                "property_floor_id": 1,
                "property_unit_notes": "Test unit",
                "property_status": "available",
                "property_unit_security_deposit": 500,
                "property_unit_commission": 200,
                "has_amenities": False,
                "media": [
                    {
                        "media_name": "unit_image",
                        "media_type": "other",
                        "content_url": media_image,
                    }
                ],
                "amenities": [],
                "utilities": [
                    {
                        "billable_id": TestUtilities.default_utility.get(
                            "utility_id", ""
                        ),
                        "utility_id": TestUtilities.default_utility.get(
                            "utility_id", ""
                        ),
                        "apply_to_units": False,
                        "billable_amount": 7852,
                        "billable_type": "utilities",
                        "description": "Would attack fish financial early win budget. Western news threat life coach right.",
                        "end_period": "2024-11-19",
                        "name": "view",
                        "payment_type_id": TestPaymentType.default_payment_type.get("payment_type_id"),
                        "start_period": "2024-10-25",
                    }
                ],
            },
        )
        assert response.status_code == 201
        TestUnits.default_units["unit_data"] = response.json()[
            "data"
        ]  # Store unit data

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_units(self, client: AsyncClient):
        response = await client.get("/unit/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_unit"], name="get_unit_by_id")
    async def test_get_unit_by_id(self, client: AsyncClient):
        unit_id = TestUnits.default_units["unit_data"]["property_unit_assoc_id"]

        response = await client.get(f"/unit/{unit_id}")

        assert response.status_code == 200
        assert response.json()["data"]["property_unit_assoc_id"] == unit_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_unit_by_id"], name="update_unit_by_id")
    async def test_update_unit(self, client: AsyncClient):
        unit_id = TestUnits.default_units["unit_data"]["property_unit_assoc_id"]

        response = await client.put(
            f"/unit/{unit_id}",
            json={
                "property_id": TestUnits.default_units["property_data"].get(
                    "property_unit_assoc_id", ""
                ),
                "property_unit_code": "Updated Unit",
                "property_unit_floor_space": 120,
                "property_unit_amount": 1200,
                "property_floor_id": 2,
                "property_unit_notes": "Updated unit notes",
                "property_status": "unavailable",
                "property_unit_security_deposit": 600,
                "property_unit_commission": 250,
                "property_unit_assoc_id": unit_id,
                "has_amenities": True,
                "media": [],
                "amenities": [],
                "utilities": [
                    {
                        "billable_id": TestUnits.default_units["utility"].get(
                            "utility_id", ""
                        ),
                        "utility_id": TestUnits.default_units["utility"].get(
                            "utility_id", ""
                        ),
                        "payment_type": 10,
                        "billable_amount": 250,
                        "apply_to_units": False,
                    }
                ],
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["property_unit_code"] == "Updated Unit"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["update_unit_by_id"], name="delete_unit_by_id")
    async def test_delete_unit(self, client: AsyncClient):
        unit_id = TestUnits.default_units["unit_data"]["property_unit_assoc_id"]

        response = await client.delete(f"/unit/{unit_id}")
        assert response.status_code == 204

        # Verify the unit is deleted
        response = await client.get(f"/unit/{unit_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["delete_unit_by_id"], name="delete_property_by_id")
    async def test_delete_property(self, client: AsyncClient):
        property_id = TestUnits.default_units["property_data"]["property_unit_assoc_id"]

        response = await client.delete(f"/property/{property_id}")
        assert response.status_code == 204

        # Verify the property is deleted
        response = await client.get(f"/property/{property_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
