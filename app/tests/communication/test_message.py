# test_messages.py

import pytest
from typing import Any, Dict
from httpx import AsyncClient
from app.tests.users.test_users import TestUsers
from faker import Faker

class TestMessages:
    default_message: Dict[str, Any] = {}
    default_reply: Dict[str, Any] = {}
    default_draft: Dict[str, Any] = {}
    default_scheduled: Dict[str, Any] = {}
    default_notification: Dict[str, Any] = {}
    recipient_user: Dict[str, Any] = {}
    faker = Faker()

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["TestUsers::create_user"],
        name="TestMessages::create_recipient_user",
    )
    async def test_create_recipient_user(self, client: AsyncClient):
        # Create a recipient user
        response = await client.post(
            "/users/",
            json={
                "date_of_birth": "1992-02-02",
                "first_name": "Recipient",
                "last_name": "User",
                "email": self.faker.unique.email(),
                "phone_number": self.faker.phone_number(),
                "identification_number": str(self.faker.random_number(digits=6, fix_len=True)),
                "photo_url": "",
                "gender": "female",
                "address": [
                    {
                        "address_type": "billing",
                        "primary": True,
                        "address_1": self.faker.street_address(),
                        "address_2": self.faker.secondary_address(),
                        "city": self.faker.city(),
                        "region": self.faker.state_abbr(),
                        "country": "USA",
                        "address_postalcode": self.faker.postcode(),
                    }
                ],
                "user_auth_info": {
                    "password": "password123",
                    "login_provider": "local",
                    "reset_token": self.faker.uuid4(),
                    "verification_token": self.faker.uuid4(),
                    "is_subscribed_token": self.faker.uuid4(),
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "current_login_time": "2024-07-21T20:52:37.078064",
                    "last_login_time": "2024-07-21T21:21:38.279Z",
                },
                "user_emergency_info": {
                    "emergency_contact_name": "John Doe",
                    "emergency_contact_email": self.faker.unique.email(),
                    "emergency_contact_relation": "Brother",
                    "emergency_contact_number": self.faker.phone_number(),
                },
                "user_employer_info": {
                    "employer_name": self.faker.company(),
                    "occupation_status": "Employed",
                    "occupation_location": self.faker.city(),
                },
                "role": "user",
            },
        )
        assert response.status_code == 201, f"Recipient user creation failed: {response.text}"
        TestMessages.recipient_user = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["TestMessages::create_recipient_user"],
        name="TestMessages::create_message",
    )
    async def test_create_message(self, client: AsyncClient):
        response = await client.post(
            "/message/",
            json={
                "subject": "Test Message",
                "message_body": "This is a test message.",
                "sender_id": TestUsers.default_user.get("user_id"),
                "recipient_ids": [TestMessages.recipient_user.get("user_id")],
                "recipient_groups": [],
                "is_draft": False,
                "is_scheduled": False,
                "is_notification": False,
            },
        )
        assert response.status_code == 201, f"Message creation failed: {response.text}"
        TestMessages.default_message = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::create_draft_message")
    async def test_create_draft_message(self, client: AsyncClient):
        # Create a draft message
        response = await client.post(
            "/message/",
            json={
                "subject": "Draft Message",
                "message_body": "This is a draft message.",
                "sender_id": TestUsers.default_user.get("user_id"),
                "recipient_ids": [],
                "recipient_groups": [],
                "is_draft": True,
                "is_scheduled": False,
                "is_notification": False,
            },
        )
        assert response.status_code == 201, f"Draft message creation failed: {response.text}"
        TestMessages.default_draft = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::create_scheduled_message")
    async def test_create_scheduled_message(self, client: AsyncClient):
        # Create a scheduled message
        response = await client.post(
            "/message/",
            json={
                "subject": "Scheduled Message",
                "message_body": "This is a scheduled message.",
                "sender_id": TestUsers.default_user.get("user_id"),
                "recipient_ids": [TestMessages.recipient_user.get("user_id")],
                "recipient_groups": [],
                "is_draft": False,
                "is_scheduled": True,
                "is_notification": False,
            },
        )
        assert response.status_code == 201, f"Scheduled message creation failed: {response.text}"
        TestMessages.default_scheduled = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::create_notification_message")
    async def test_create_notification_message(self, client: AsyncClient):
        # Create a notification message
        response = await client.post(
            "/message/",
            json={
                "subject": "Notification Message",
                "message_body": "This is a notification message.",
                "sender_id": TestUsers.default_user.get("user_id"),
                "recipient_ids": [TestMessages.recipient_user.get("user_id")],
                "recipient_groups": [],
                "is_draft": False,
                "is_scheduled": False,
                "is_notification": True,
            },
        )
        assert response.status_code == 201, f"Notification message creation failed: {response.text}"
        TestMessages.default_notification = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_messages(self, client: AsyncClient):
        response = await client.get("/message/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to fetch messages: {response.text}"
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::get_message_by_id")
    async def test_get_message_by_id(self, client: AsyncClient):
        print("Response is:", self.default_message)
        message_id = self.default_message['data']["message_id"]
        response = await client.get(f"/message/{message_id}")
        assert response.status_code == 200, f"Failed to get message by ID: {response.text}"
        assert response.json()["data"]["message_id"] == message_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::reply_to_message")
    async def test_reply_to_message(self, client: AsyncClient):
        message_id = self.default_message["data"]["message_id"]
        print("Message ID:", message_id)
        response = await client.post(
            "/message/reply/",
            json={
                "parent_message_id": message_id,
                "message_body": "This is a reply to the test message.",
                "sender_id": TestMessages.recipient_user.get("user_id"),
                "recipient_ids": [TestUsers.default_user.get("user_id")],
                "recipient_groups": [],
            },
        )
        assert response.status_code == 200, f"Reply to message failed: {response.text}"
        TestMessages.default_reply = response.json()["data"]
        assert TestMessages.default_reply["parent_message_id"] == message_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_draft_message"], name="TestMessages::get_user_drafts")
    async def test_get_user_drafts(self, client: AsyncClient):
        user_id = TestUsers.default_user.get("user_id")
        response = await client.get(f"/message/users/{user_id}/drafts", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to get user drafts: {response.text}"
        messages = response.json()["data"]
        assert any(m["message_id"] == self.default_draft["data"]["message_id"] for m in messages), "Draft message not found in drafts"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_scheduled_message"], name="TestMessages::get_user_scheduled")
    async def test_get_user_scheduled(self, client: AsyncClient):
        user_id = TestUsers.default_user.get("user_id")
        response = await client.get(f"/message/users/{user_id}/scheduled", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to get user scheduled messages: {response.text}"
        messages = response.json()["data"]
        assert any(m["message_id"] == self.default_scheduled["data"]["message_id"] for m in messages), "Scheduled message not found"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::get_user_outbox")
    async def test_get_user_outbox(self, client: AsyncClient):
        user_id = TestUsers.default_user.get("user_id")
        response = await client.get(f"/message/users/{user_id}/outbox", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to get user outbox: {response.text}"
        messages = response.json()["data"]
        assert any(m["message_id"] == self.default_message["data"]["message_id"] for m in messages), "Message not found in outbox"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[
            "TestMessages::reply_to_message"],
        name="TestMessages::get_user_inbox"
    )
    async def test_get_user_inbox(self, client: AsyncClient):
        user_id = TestUsers.default_user.get("user_id")
        response = await client.get(f"/message/users/{user_id}/inbox", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to get user inbox: {response.text}"
        messages = response.json()["data"]
        # Check if the reply message is in the inbox
        assert any(m["message_id"] == self.default_reply["message_id"] for m in messages), "Reply not found in inbox"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=[
            "TestMessages::create_notification_message"],
        name="TestMessages::get_user_notifications"
    )
    async def test_get_user_notifications(self, client: AsyncClient):
        user_id = TestMessages.recipient_user.get("user_id")
        response = await client.get(f"/message/users/{user_id}/notifications", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, f"Failed to get user notifications: {response.text}"
        messages = response.json()["data"]
        assert any(m["message_id"] == self.default_notification["data"]["message_id"] for m in messages), "Notification message not found"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::update_message_by_id")
    async def test_update_message(self, client: AsyncClient):
        message_id = self.default_message["data"]["message_id"]
        response = await client.put(
            f"/message/{message_id}",
            json={
                "subject": "Updated Test Message",
                "message_body": "This is an updated test message.",
            },
        )
        assert response.status_code == 200, f"Message update failed: {response.text}"
        assert response.json()["data"]["subject"] == "Updated Test Message"

    # @pytest.mark.asyncio(loop_scope="session")
    # @pytest.mark.dependency(depends=["TestMessages::create_message"], name="TestMessages::delete_message_by_id")
    # async def test_delete_message(self, client: AsyncClient):
    #     message_id = self.default_message["data"]["message_id"]
    #     response = await client.delete(f"/message/{message_id}")
    #     assert response.status_code == 204, f"Message deletion failed: {response.text}"

    #     # Verify that the message is deleted
    #     response = await client.get(f"/message/{message_id}")
    #     assert response.status_code == 200, f"Failed to get message by ID after deletion: {response.text}"
    #     assert response.json()["data"] == {}
