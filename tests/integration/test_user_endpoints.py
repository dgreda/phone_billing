from fastapi.testclient import TestClient


def test_user_not_found(client: TestClient) -> None:
    response = client.get("/user/123")
    assert response.status_code == 404


def test_create_and_get_user(client: TestClient) -> None:
    country_code = 1
    number = 123456789
    response = client.post(
        "/user", json={"country_code": country_code, "number": number}
    )
    data = response.json()

    assert response.status_code == 201
    assert data["country_code"] == country_code
    assert data["number"] == number
    assert data["id"] is not None

    user_id = data["id"]

    response = client.get(f"/user/{user_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["country_code"] == country_code
    assert data["number"] == number
