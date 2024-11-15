import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.properties.test_property import TestProperties
from app.tests.users.test_users import TestUsers


class TestPropertyAssignment:
    default_property_assignment: Dict[str, Any] = {}
    default_property: Dict[str, Any] = TestProperties.default_property
    default_utility: Dict[str, Any] = TestProperties.default_utility
    default_user: Dict[str, Any] = TestUsers.default_user

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["TestProperties::test_create_property", "TestUsers::test_create_user"],
        name="create_property_assignment",
    )
    async def test_create_property_assignment(self, client: AsyncClient):
        # Using the property created by TestProperties and user created by TestUsers
        response = await client.post(
            "/assign-properties/",
            json={
                "property_unit_assoc_id": self.default_property[
                    "property_unit_assoc_id"
                ],
                "user_id": self.default_user["user_id"],  # Fetching from TestUsers
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
            "/assign-properties/", params={"limit": 10, "offset": 0}
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

        response = await client.get(f"/assign-properties/{property_assignment_id}")
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
            f"/assign-properties/{property_assignment_id}",
            json={
                "property_unit_assoc_id": self.default_property[
                    "property_unit_assoc_id"
                ],
                "user_id": self.default_user["user_id"],  # Fetching from TestUsers
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

        response = await client.delete(f"/assign-properties/{property_assignment_id}")
        assert response.status_code == 204

        # Verify the property assignment is deleted
        response = await client.get(f"/assign-properties/{property_assignment_id}")
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
