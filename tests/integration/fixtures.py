from datetime import datetime, timedelta
from random import randint
from typing import Optional

import requests
from fastapi.testclient import TestClient


def create_user(
    client: TestClient,
    country_code: Optional[int] = randint(1, 100),
    number: Optional[int] = randint(101_100_100, 959_000_1000),
) -> requests.Response:
    response = client.post(
        "/user", json={"country_code": country_code, "number": number}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["id"] is not None

    return response


def get_user(client: TestClient, id: int) -> requests.Response:
    response = client.get(f"/user/{id}")

    assert response.status_code == 200

    return response


def create_call(
    client: TestClient,
    user_id: int,
    duration: int,
    start_datetime: datetime,
    recipient_country_code: Optional[int] = randint(1, 100),
    recipient_number: Optional[int] = randint(101_100_100, 959_000_1000),
) -> requests.Response:
    end_datetime = start_datetime + timedelta(minutes=duration)

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
    assert data["id"] is not None

    return response


def get_call(client: TestClient, id: int) -> requests.Response:
    response = client.get(f"/call/{id}")

    assert response.status_code == 200

    return response


def get_invoice(client: TestClient, id: int) -> requests.Response:
    response = client.get(f"/invoice/{id}")

    assert response.status_code == 200

    return response
