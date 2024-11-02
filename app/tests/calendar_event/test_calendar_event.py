import pytest
from typing import Any, Dict
from httpx import AsyncClient


# TODO:
# - PUT, DELETE, GET[id] should be the same
class TestCalendarEvent:
    default_calendar_event: Dict[str, Any] = {}

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(name="create_calendar_event")
    async def test_create_calendar_event(self, client: AsyncClient):
        response = await client.post(
            "/calendar_event/",
            json={
                "title": "Meeting",
                "description": "Team meeting",
                "status": "pending",
                "event_type": "other",
                "event_start_date": "2024-07-21T21:28:35.074Z",
                "event_end_date": "2024-07-21T21:28:35.074Z",
                "completed_date": "2024-07-21T21:28:35.074Z",
                "organizer_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
            },
        )
        assert response.status_code == 200

        TestCalendarEvent.default_calendar_event = response.json()["data"]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_all_calendar_events(self, client: AsyncClient):
        response = await client.get(
            "/calendar_event/", params={"limit": 10, "offset": 0}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["create_calendar_event"], name="get_calendar_event_by_id"
    )
    async def test_get_calendar_event_by_id(self, client: AsyncClient):
        calendar_event_id = self.default_calendar_event["event_id"]

        response = await client.get(f"/calendar_event/{calendar_event_id}")

        assert response.status_code == 200
        assert response.json()["data"]["event_id"] == calendar_event_id

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["get_calendar_event_by_id"], name="update_calendar_event_by_id"
    )
    async def test_update_calendar_event(self, client: AsyncClient):
        calendar_event_id = self.default_calendar_event["event_id"]

        response = await client.put(
            f"/calendar_event/{calendar_event_id}",
            json={
                "title": "Updated Meeting",
                "description": "Updated team meeting",
                "status": "pending",
                "event_type": "other",
                "event_start_date": "2024-07-21T21:28:35.074Z",
                "event_end_date": "2024-07-21T21:28:35.074Z",
                "completed_date": "2024-07-21T21:28:35.074Z",
                "organizer_id": "0d5340d2-046b-42d9-9ef5-0233b79b6642",
            },
        )
        assert response.status_code == 200
        assert response.json()["data"]["title"] == "Updated Meeting"

    @pytest.mark.asyncio(loop_scope="session")
    @pytest.mark.dependency(
        depends=["update_calendar_event_by_id"], name="delete_calendar_event_by_id"
    )
    async def test_delete_calendar_event(self, client: AsyncClient):
        calendar_event_get_id = self.default_calendar_event["event_id"]
        # calendar_event_id = self.default_calendar_event["id"]

        response = await client.delete(f"/calendar_event/{calendar_event_get_id}")
        assert response.status_code == 204

        # Verify the calendar event is deleted
        response = await client.get(f"/calendar_event/{calendar_event_get_id}")
        assert response.status_code == 200
        assert response.json()["data"] == {}
