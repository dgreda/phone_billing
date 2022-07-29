from unittest.mock import MagicMock

import pytest

from app.domain.entities import CreateInvoiceRequest
from app.domain.exceptions import InvoiceAlreadyExists
from app.domain.services import InvoiceService
from app.domain.services.billing import FlatRatePostpaidPlanStrategy
from tests.unit.fixtures import (
    create_call_entity,
    create_invoice_entity,
    create_user_entity,
)

TAX_RATE = 0.08
CHARGE_PER_MINUTE = 0.02


@pytest.fixture()
def invoice_service() -> InvoiceService:
    return InvoiceService(
        billing_strategy=FlatRatePostpaidPlanStrategy(
            tax_rate=TAX_RATE, charge_per_minute=CHARGE_PER_MINUTE
        ),
        call_repository=MagicMock(),
        invoice_repository=MagicMock(),
    )


def test_bill_and_create_invoice_raises_exception(
    invoice_service: InvoiceService,
) -> None:
    example_user = create_user_entity()
    example_invoice = create_invoice_entity(
        "abc-123",
        2022,
        7,
        123,
        12.34,
    )
    invoice_repo_mock = MagicMock()
    invoice_repo_mock.find_by_year_and_month.return_value = example_invoice

    invoice_service.invoice_repository = invoice_repo_mock

    with pytest.raises(
        InvoiceAlreadyExists, match="Invoice abc-123 for 7/2022 already exists!"
    ):
        invoice_service.bill_and_create_invoice(example_user, 2022, 7)


def test_bill_and_create_invoice(invoice_service: InvoiceService) -> None:
    minutes1 = 20
    minutes2 = 15
    expected_total_charges = (
        (minutes1 + minutes2) * CHARGE_PER_MINUTE * (1 + TAX_RATE)
    )
    example_user = create_user_entity()
    example_invoice = create_invoice_entity(
        "abc-123",
        2022,
        7,
        minutes1 + minutes2,
        expected_total_charges,
    )

    call1 = create_call_entity(minutes1)
    call2 = create_call_entity(minutes2)
    calls = [call1, call2]

    invoice_repo_mock = MagicMock()
    invoice_repo_mock.find_by_year_and_month.return_value = None
    invoice_repo_mock.persist_invoice.return_value = example_invoice

    invoice_service.invoice_repository = invoice_repo_mock

    call_repo_mock = MagicMock()
    call_repo_mock.find_not_invoiced_calls.return_value = calls

    invoice_service.call_repository = call_repo_mock

    invoice_service.bill_and_create_invoice(example_user, 2022, 7)

    invoice_repo_mock.persist_invoice.assert_called_once_with(
        request=CreateInvoiceRequest(
            billing_month=7,
            billing_year=2022,
            total_minutes=minutes1 + minutes2,
            total_charges=expected_total_charges,
        ),
        user=example_user,
    )

    call_repo_mock.persist_all.assert_called_once()
