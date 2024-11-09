import pytest
from typing import Any, Dict
from httpx import AsyncClient

class TestPermissions:
    default_permission: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_permission")
    async def test_create_permission(self, client: AsyncClient):
        # Check if permission already exists and delete it if necessary to avoid duplicates
        existing_permissions_response = await client.get(
            "/permissions/", params={"name": "Administrator"}
        )
        if existing_permissions_response.status_code == 200:
            existing_permissions = existing_permissions_response.json().get("data", [])
            for permission in existing_permissions:
                if permission["name"] == "Administrator":
                    permission_id = permission["permission_id"]
                    delete_response = await client.delete(f"/permissions/{permission_id}")
                    assert delete_response.status_code in [200, 204], f"Failed to delete existing permission: {delete_response.text}"

        # Proceed to create a new permission
        response = await client.post(
            "/permissions/",
            json={
                "name": "Administrator",
                "alias": "admin",
                "description": "Has full access to all settings.",
            },
        )
        assert response.status_code == 201, f"Failed to create permission: {response.text}"
        TestPermissions.default_permission = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_permissions(self, client: AsyncClient):
        response = await client.get("/permissions/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to fetch all permissions: {response.text}"
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["create_permission"], name="get_permission_by_id")
    async def test_get_permission_by_id(self, client: AsyncClient):
        print("Default permission", self.default_permission)
        permission_id = self.default_permission["permission_id"]

        response = await client.get(f"/permissions/{permission_id}")
        assert response.status_code == 200, f"Failed to fetch permission by ID: {response.text}"
        assert response.json()["data"]["permission_id"] == permission_id

    @pytest.mark.asyncio(loop_scope="session")
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
        assert response.status_code == 200, f"Failed to update permission: {response.text}"
        assert response.json()["data"]["name"] == "write"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_permission_by_id"], name="delete_permission_by_id"
    )
    async def test_delete_permission(self, client: AsyncClient):
        permission_id = self.default_permission["permission_id"]

        response = await client.delete(f"/permissions/{permission_id}")
        assert response.status_code == 204, f"Failed to delete permission: {response.text}"

        # Verify the permission is deleted
        response = await client.get(f"/permissions/{permission_id}")
        assert response.status_code == 404, f"Permission was not properly deleted: {response.text}"
