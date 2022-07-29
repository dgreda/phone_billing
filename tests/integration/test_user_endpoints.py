from fastapi.testclient import TestClient

from tests.integration.fixtures import create_user, get_user


def test_user_not_found(client: TestClient) -> None:
    response = client.get("/user/123")
    assert response.status_code == 404


def test_create_and_get_user(client: TestClient) -> None:
    country_code = 1
    number = 123456789
    response = create_user(client, country_code, number)
    data = response.json()

    assert data["country_code"] == country_code
    assert data["number"] == number

    user_id = data["id"]

    response = get_user(client, user_id)
    data = response.json()

    assert data["country_code"] == country_code
    assert data["number"] == number
