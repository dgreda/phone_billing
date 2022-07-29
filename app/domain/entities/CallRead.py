from typing import Optional

from app.domain.entities.CallBase import CallBase


class CallRead(CallBase):
    id: int
    user_id: int
    invoice_id: Optional[int]
