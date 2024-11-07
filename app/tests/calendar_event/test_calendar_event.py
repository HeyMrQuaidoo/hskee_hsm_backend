import pytest
from typing import Any, Dict
from httpx import AsyncClient

class TestCalendarEvent:
    default_calendar_event: Dict[str, Any] = {}

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(name="create_calendar_event")
    async def test_create_calendar_event(self, client: AsyncClient):
        response = await client.post(
            "/calendar-event/",
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
        assert response.status_code == 201, response.text

        TestCalendarEvent.default_calendar_event = response.json().get("data", {})

    @pytest.mark.asyncio(scope="session")
    async def test_get_all_calendar_events(self, client: AsyncClient):
        response = await client.get("/calendar-event/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200, response.text
        assert isinstance(response.json(), dict), response.text

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["create_calendar_event"], name="get_calendar_event_by_id"
    )
    async def test_get_calendar_event_by_id(self, client: AsyncClient):
        calendar_event_id = self.default_calendar_event["event_id"]
        response = await client.get(f"/calendar-event/{calendar_event_id}")
        assert response.status_code == 200, response.text
        assert response.json().get("data", {}).get("event_id") == calendar_event_id

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["get_calendar_event_by_id"], name="update_calendar_event_by_id"
    )
    async def test_update_calendar_event(self, client: AsyncClient):
        calendar_event_id = self.default_calendar_event["event_id"]
        response = await client.put(
            f"/calendar-event/{calendar_event_id}",
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
        assert response.status_code == 200, response.text
        assert response.json().get("data", {}).get("title") == "Updated Meeting"

    @pytest.mark.asyncio(scope="session")
    @pytest.mark.dependency(
        depends=["update_calendar_event_by_id"], name="delete_calendar_event_by_id"
    )
    async def test_delete_calendar_event(self, client: AsyncClient):
        calendar_event_id = self.default_calendar_event["event_id"]
        response = await client.delete(f"/calendar-event/{calendar_event_id}")
        assert response.status_code == 204, response.text

        # Verify the calendar event is deleted
        response = await client.get(f"/calendar-event/{calendar_event_id}")
        assert response.status_code == 404, response.text
