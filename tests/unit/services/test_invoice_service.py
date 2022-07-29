from app.domain.services.billing import FlatRatePostpaidPlanStrategy
from tests.unit.fixtures import create_call


def test_calculate_total() -> None:
    charge_per_minute = 0.02
    tax_rate = 0.1
    call1 = create_call(20)
    call2 = create_call(15)

    strategy = FlatRatePostpaidPlanStrategy(
        tax_rate=tax_rate, charge_per_minute=charge_per_minute
    )

    total_charge = strategy.calculate_total(calls=[call1, call2])

    expected_charge = (
        (call1.duration_in_minutes + call2.duration_in_minutes)
        * charge_per_minute
    ) * (1 + tax_rate)

    assert total_charge == expected_charge
