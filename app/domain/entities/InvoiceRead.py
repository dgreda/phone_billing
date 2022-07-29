from app.domain.entities.InvoiceBase import InvoiceBase


class InvoiceRead(InvoiceBase):
    id: int
    user_id: int
    identifier: str
