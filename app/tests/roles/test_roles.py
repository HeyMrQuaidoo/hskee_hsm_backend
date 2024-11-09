import pytest
from typing import Any, Dict
from httpx import AsyncClient
from faker import Faker  # Import Faker

faker = Faker()  # Initialize a Faker instance

class TestRoles:
    role_data: Dict[str, Any] = {}  # Use a class variable to store role data

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_role")
    async def test_create_role(self, client: AsyncClient):
        unique_role_name = faker.unique.name()  # Generate a unique role name using Faker
        response = await client.post(
            "/roles/",
            json={
                "name": unique_role_name,
                "alias": f"{unique_role_name}_alias",
                "description": "A new role with a unique name",
            },
        )
        assert response.status_code == 201
        TestRoles.role_data = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_roles(self, client: AsyncClient):
        response = await client.get("/roles/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_role"], name="get_role_by_id")
    async def test_get_role_by_id(self, client: AsyncClient):
        # Retrieve role data
        role_id = self.role_data["role_id"]
        response = await client.get(f"/roles/{role_id}")
        assert response.status_code == 200
        assert response.json()["data"]["role_id"] == role_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["get_role_by_id"], name="update_role_by_id")
    async def test_update_role(self, client: AsyncClient):
        # Retrieve role data
        role_id = self.role_data["role_id"]
        updated_name = faker.unique.name()  # Generate a new unique role name using Faker
        response = await client.put(
            f"/roles/{role_id}",
            json={
                "name": updated_name,
                "alias": f"{updated_name}_alias",
                "description": "An updated role with a unique name",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == updated_name
        assert response.json()["data"]["alias"] == f"{updated_name}_alias"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["update_role_by_id"], name="delete_role_by_id")
    async def test_delete_role(self, client: AsyncClient):
        # Retrieve role data
        role_id = self.role_data["role_id"]
        response = await client.delete(f"/roles/{role_id}")
        assert response.status_code == 204

        # Verify the role is deleted
        response = await client.get(f"/roles/{role_id}")
        assert response.status_code == 404
