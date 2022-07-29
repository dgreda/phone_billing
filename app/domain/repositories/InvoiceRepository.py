import uuid
from typing import Optional

from sqlmodel import select

from app.domain.entities.CreateInvoiceRequest import CreateInvoiceRequest
from app.domain.entities.Invoice import Invoice
from app.domain.entities.User import User
from app.domain.exceptions import InvoiceNotFound

from .AbstractRepository import AbstractRepository


class InvoiceRepository(AbstractRepository):
    def find_or_fail(self, id: int) -> Invoice:
        invoice = self.session.get(Invoice, id)
        if invoice is None:
            raise InvoiceNotFound(id)

        return invoice

    def find_by_year_and_month(
        self, year: int, month: int
    ) -> Optional[Invoice]:
        return self.session.exec(
            select(Invoice)
            .where(Invoice.billing_month == month)
            .where(Invoice.billing_year == year)
        ).one_or_none()

    def persist_invoice(
        self, request: CreateInvoiceRequest, user: User
    ) -> Invoice:
        invoice = Invoice(
            identifier=str(uuid.uuid1()),
            billing_month=request.billing_month,
            billing_year=request.billing_year,
            total_minutes=request.total_minutes,
            total_charges=request.total_charges,
            user_id=user.id,
        )
        invoice = self.persist(invoice)

        return invoice
