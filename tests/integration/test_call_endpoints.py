from datetime import datetime, timedelta

from dateutil import parser
from fastapi.testclient import TestClient


def test_call_not_found(client: TestClient) -> None:
    response = client.get("/call/123")
    assert response.status_code == 404


def test_create_and_get_call(client: TestClient):
    country_code = 1
    number = 123456789
    response = client.post(
        "/user", json={"country_code": country_code, "number": number}
    )
    data = response.json()
    assert response.status_code == 201
    user_id = data["id"]

    recipient_country_code = 48
    recipient_number = 987123654
    duration = 12
    now = datetime.now()
    start_datetime = now - timedelta(minutes=duration)
    end_datetime = now

    response = client.post(
        f"/user/{user_id}/phone_call",
        json={
            "recipient_country_code": recipient_country_code,
            "recipient_number": recipient_number,
            "duration_in_minutes": duration,
            "start_datetime_iso_8601": start_datetime.isoformat(),
            "end_datetime_iso_8601": end_datetime.isoformat(),
        },
    )
    data = response.json()

    assert response.status_code == 201
    assert data["recipient_country_code"] == recipient_country_code
    assert data["recipient_number"] == recipient_number
    assert data["duration_in_minutes"] == duration
    assert parser.parse(data["start_datetime_iso_8601"]) == start_datetime
    assert parser.parse(data["end_datetime_iso_8601"]) == end_datetime
    assert data["duration_in_minutes"] == duration
    assert data["id"] is not None
    assert data["user_id"] == user_id
    assert data["invoice_id"] is None

    response = client.get(f"/user/{user_id}/phone_call?offset=0&limit=1")
    data = response.json()

    assert response.status_code == 200
    assert type(data) == list
    assert len(data) == 1

    call = data[0]

    assert call["id"] is not None
    call_id = call["id"]

    response = client.get(f"/call/{call_id}")
    data = response.json()

    assert data["recipient_country_code"] == recipient_country_code
    assert data["recipient_number"] == recipient_number
    assert data["duration_in_minutes"] == duration
