import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestRoles:
    default_role: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_role")
    async def test_create_role(self, client: AsyncClient):
        response = await client.post(
            "/roles/",
            json={
                "name": "newrole",
                "alias": "newrolealias",
                "description": "A new role",
            },
        )
        assert response.status_code == 200

        TestRoles.default_role = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_roles(self, client: AsyncClient):
        response = await client.get("/roles/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_role"], name="get_role_by_id")
    async def test_get_role_by_id(self, client: AsyncClient):
        # get role information
        role_id = self.default_role["role_id"]

        response = await client.get(f"/roles/{role_id}")

        assert response.status_code == 200
        assert response.json()["data"]["role_id"] == role_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["get_role_by_id"], name="update_role_by_id")
    async def test_update_role(self, client: AsyncClient):
        # get role information
        role_id = self.default_role["role_id"]

        response = await client.put(
            f"/roles/{role_id}",
            json={
                "name": "updatedrole",
                "alias": "updatedrolealias",
                "description": "An updated role",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "updatedrole"
        assert response.json()["data"]["alias"] == "updatedrolealias"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["update_role_by_id"], name="delete_role_by_id")
    async def test_delete_role(self, client: AsyncClient):
        # get role information
        role_id = self.default_role["role_id"]

        response = await client.delete(f"/roles/{role_id}")
        assert response.status_code == 204

        # verify the role is deleted
        response = await client.get(f"/roles/{role_id}")
        assert response.status_code == 404
