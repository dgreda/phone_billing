from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.domain.exceptions import InvoiceAlreadyExists
from tests.integration.fixtures import create_call, create_user, get_call, get_invoice


def test_invoice_not_found(client: TestClient) -> None:
    response = client.get("/invoice/456")
    assert response.status_code == 404


def test_invoice_creation_end_to_end(client: TestClient) -> None:
    # first create a user (customer)
    response = create_user(client)
    data = response.json()
    user_id = data["id"]

    # next, create some phone calls
    call1 = create_call(
        client=client,
        user_id=user_id,
        duration=30,
        start_datetime=datetime(2022, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
    ).json()

    call2 = create_call(
        client=client,
        user_id=user_id,
        duration=45,
        start_datetime=datetime(2022, 7, 31, 17, 59, 0, tzinfo=timezone.utc),
    ).json()

    # request invoice generation for 7/2022
    response = client.post(f"user/{user_id}/invoice/2022/7")
    assert response.status_code == 201

    invoice = response.json()

    assert invoice["id"] is not None
    assert invoice["identifier"] is not None
    assert invoice["billing_month"] == 7
    assert invoice["billing_year"] == 2022
    assert invoice["total_minutes"] == 75
    assert invoice["total_charges"] == 75 * 0.02 * 1.08

    # reload invoice data
    invoice = get_invoice(client, invoice["id"]).json()

    # check that individual call entries have their invoice_id updated now
    read_call1 = get_call(client, call1["id"]).json()
    read_call2 = get_call(client, call2["id"]).json()

    assert read_call1["invoice_id"] == invoice["id"]
    assert read_call2["invoice_id"] == invoice["id"]

    # verify that it's not possible to create invoice for the same user and billing cycle again
    response = client.post(f"user/{user_id}/invoice/2022/7")
    data = response.json()

    assert response.status_code == 409
    assert (
        data["error"]
        == f"Invoice {invoice['identifier']} for 7/2022 already exists!"
    )
