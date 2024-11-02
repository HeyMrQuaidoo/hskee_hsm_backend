# import pytest
# from httpx import AsyncClient

# @pytest.mark.asyncio(scope="session")
# async def test_user_login(client: AsyncClient):
#     response = await client.post("/auth/", json={"username": "admin@housekee.com", "password": "tester"})
#     assert response.status_code == 200
#     assert "access_token" in response.json()

# # @pytest.mark.asyncio(scope="session")
# # async def test_reset_password(client: AsyncClient):
# #     response = await client.post("/auth/reset-password", json={"email": "daniel.quaidoo@gmail.com"})
# #     assert response.status_code == 200

# # @pytest.mark.asyncio(scope="session")
# # async def test_verify_email(client: AsyncClient):
# #     response = await client.get("/auth/verify-email", params={"email": "testuser@example.com", "token": "sometoken"})
# #     assert response.status_code == 200
