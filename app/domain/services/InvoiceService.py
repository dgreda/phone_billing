from app.domain.contracts import BillingPlanStrategyInterface
from app.domain.entities import CreateInvoiceRequest, Invoice, User
from app.domain.exceptions import InvoiceAlreadyExists
from app.domain.repositories import CallRepository, InvoiceRepository
from app.domain.services.DateService import DateService


class InvoiceService:
    def __init__(
        self,
        billing_strategy: BillingPlanStrategyInterface,
        call_repository: CallRepository,
        invoice_repository: InvoiceRepository,
    ):
        self.billing_strategy = billing_strategy
        self.call_repository = call_repository
        self.invoice_repository = invoice_repository

    def bill_and_create_invoice(
        self, user: User, billing_year: int, billing_month: int
    ) -> Invoice:
        existing_invoice = self.invoice_repository.find_by_year_and_month(
            year=billing_year, month=billing_month
        )

        if existing_invoice is not None:
            raise InvoiceAlreadyExists(
                year=billing_year,
                month=billing_month,
                identifier=existing_invoice.identifier,
            )

        start_datetime = DateService.get_month_start_utc_timestamp(
            year=billing_year,
            month=billing_month,
        )
        end_datetime = DateService.get_month_end_utc_timestamp(
            year=billing_year,
            month=billing_month,
        )

        calls = self.call_repository.find_not_invoiced_calls(
            user, start_datetime, end_datetime
        )

        request = CreateInvoiceRequest(
            billing_month=billing_month,
            billing_year=billing_year,
            total_minutes=self.billing_strategy.get_total_billable_minutes(
                calls
            ),
            total_charges=self.billing_strategy.calculate_total(calls),
        )

        invoice = self.invoice_repository.persist_invoice(
            request=request, user=user
        )

        for call in calls:
            call.invoice_id = invoice.id

        self.call_repository.persist_all(calls)

        return invoice
