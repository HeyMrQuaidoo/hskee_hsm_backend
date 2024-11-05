# import pytest
# from typing import Any, Dict
# from httpx import AsyncClient


# class TestMessages:
#     default_message: Dict[str, Any] = {}

#     @pytest.mark.asyncio(loop_scope="session")
#     @pytest.mark.dependency(name="create_message")
#     async def test_create_message(self, client: AsyncClient):
#         response = await client.post(
#             "/messages/",
#             json={
#                 "subject": "Test Subject",
#                 "message_body": "This is a test message body.",
#                 "sender_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
#                 "is_draft": False,
#                 "is_scheduled": False,
#                 "recipient_ids": [
#                     "4dbc3019-1884-4a0d-a2e6-feb12d83186e"
#                 ],
#                 "recipient_groups": []
#             },
#         )
#         assert response.status_code == 200

#         TestMessages.default_message = response.json()["data"]

#     @pytest.mark.asyncio(loop_scope="session")
#     async def test_get_all_messages(self, client: AsyncClient):
#         response = await client.get("/messages/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200
#         assert isinstance(response.json(), dict)

#     @pytest.mark.asyncio(loop_scope="session")
#     @pytest.mark.dependency(depends=["create_message"], name="get_message_by_id")
#     async def test_get_message_by_id(self, client: AsyncClient):
#         message_id = self.default_message["message_id"]

#         response = await client.get(f"/messages/{message_id}")

#         assert response.status_code == 200
#         assert response.json()["data"]["message_id"] == message_id

#     @pytest.mark.asyncio(loop_scope="session")
#     @pytest.mark.dependency(depends=["get_message_by_id"], name="update_message_by_id")
#     async def test_update_message(self, client: AsyncClient):
#         message_id = self.default_message["message_id"]

#         response = await client.put(
#             f"/messages/{message_id}",
#             json={
#                 "subject": "Updated Subject",
#                 "message_body": "This is an updated test message body.",
#                 "sender_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
#                 "is_draft": False,
#                 "is_scheduled": False,
#                 "recipient_ids": [
#                     "4dbc3019-1884-4a0d-a2e6-feb12d83186e"
#                 ],
#                 "recipient_groups": []
#             },
#         )
#         assert response.status_code == 200
#         assert response.json()["data"]["subject"] == "Updated Subject"

#     @pytest.mark.asyncio(loop_scope="session")
#     @pytest.mark.dependency(depends=["update_message_by_id"], name="delete_message_by_id")
#     async def test_delete_message(self, client: AsyncClient):
#         message_id = self.default_message["message_id"]

#         response = await client.delete(f"/messages/{message_id}")
#         assert response.status_code == 204

#         # Verify the message is deleted
#         response = await client.get(f"/messages/{message_id}")
#         assert response.status_code == 200
#         assert response.json()["data"] == {}
