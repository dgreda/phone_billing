from sqlmodel import SQLModel


class InvoiceBase(SQLModel):
    billing_month: int
    billing_year: int
    total_minutes: int
    total_charges: float
