from typing import List

from app.domain.contracts import BillingPlanStrategyInterface
from app.domain.entities import Call


class FlatRatePostpaidPlanStrategy(BillingPlanStrategyInterface):
    def __init__(self, tax_rate: float, charge_per_minute: float):
        super().__init__(tax_rate)
        self.charge_per_minute = charge_per_minute

    def calculate_total(self, calls: List[Call]) -> float:
        total_minutes = self.get_total_billable_minutes(calls)
        total_net_charge = total_minutes * self.charge_per_minute

        return total_net_charge * (1 + self.tax_rate)
