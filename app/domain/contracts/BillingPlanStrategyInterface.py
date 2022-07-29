from abc import ABC, abstractmethod
from typing import List

from app.domain.entities import Call


class BillingPlanStrategyInterface(ABC):
    def __init__(self, tax_rate: float):
        self.tax_rate = tax_rate

    @staticmethod
    def get_total_billable_minutes(calls: List[Call]) -> int:
        return sum(call.duration_in_minutes for call in calls)

    @abstractmethod
    def calculate_total(self, calls: List[Call]) -> float:
        """
        Interface method that individual billing plan strategies must implement.
        Example billing plans might be prepaid, postpaid, fixed_amount, etc.
        :param calls: List of Call entities, for which the strategy has to calculate total amount to charge
        :return float: The total charge (including taxes)
        """
