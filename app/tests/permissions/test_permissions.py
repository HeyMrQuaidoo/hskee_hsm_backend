import pytest
from typing import Any, Dict
from httpx import AsyncClient


class TestPermissions:
    default_permission: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_permission")
    async def test_create_permission(self, client: AsyncClient):
        response = await client.post(
            "/permissions/",
            json={
                "name": "read",
                "alias": "read_permission",
                "description": "Allows reading of resources",
            },
        )
        assert response.status_code == 200

        TestPermissions.default_permission = response.json()["data"]

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_permissions(self, client: AsyncClient):
        response = await client.get("/permissions/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(depends=["create_permission"], name="get_permission_by_id")
    async def test_get_permission_by_id(self, client: AsyncClient):
        permission_id = self.default_permission["permission_id"]

        response = await client.get(f"/permissions/{permission_id}")

        assert response.status_code == 200
        assert response.json()["data"]["permission_id"] == permission_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["get_permission_by_id"], name="update_permission_by_id"
    )
    async def test_update_permission(self, client: AsyncClient):
        permission_id = self.default_permission["permission_id"]

        response = await client.put(
            f"/permissions/{permission_id}",
            json={
                "name": "write",
                "alias": "write_permission",
                "description": "Allows writing of resources",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "write"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["update_permission_by_id"], name="delete_permission_by_id"
    )
    async def test_delete_permission(self, client: AsyncClient):
        permission_id = self.default_permission["permission_id"]

        response = await client.delete(f"/permissions/{permission_id}")
        assert response.status_code == 204

        # verify the permission is deleted
        response = await client.get(f"/permissions/{permission_id}")
        assert response.status_code == 404
