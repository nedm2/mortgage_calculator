from typing import Tuple

"""
e.g. 491750, 35 years 2.9%
e.g. 491750, 1 year 2.5%, 34 years 2.9%
e.g. 245875, 35 year 2.5%, 245875 2.9%
e.g. 491750, cashback 2% after 2 months, pay that off on variable, rest on fixed
e.g. 491750, pay off 50000 after 1 year, rest on fixed

paramaterization
[(principal, total_duration, [rate, duration]), ...]
"""

mortgage_scenarios = [
    [(491750, 35, [(0.025, 35)])]
  , [(491750, 35, [(0.029, 35)])]
  , [(491750, 35, [(0.035, 35)])]
  , [(491750, 30, [(0.025, 30)])]
  , [(491750, 30, [(0.029, 30)])]
  , [(491750, 30, [(0.035, 30)])]
]

def evaluate_step(
        rate : float,
        periods : int,
        principal : float,
        payment : float
    )-> Tuple[float, float]:
    """
    Evaluates the status of the loan following the passed number of periods.
    Returns the remaining loan value and the interest paid in this step.
    """
    interest_acc : float = 0
    for period in range(periods):
        interest = principal * rate
        interest_acc += interest
        principal = principal + interest - payment
    return (principal - payment*periods, interest_acc)


def pmt(rate, periods, present_value):
    payment: float = 1000
    while True:
        remaining = present_value
        for period in range(periods):
            interest = remaining * rate
            remaining = remaining + interest - payment
        if abs(remaining) < 0.1:
            return payment
        payment += remaining/periods

def evaluate_scenario(scenario):
    for (principal, duration_years, steps) in scenario:
        annual_interest_rate = steps[0][0]
        monthly_interest_rate = annual_interest_rate / 12.0
        duration_months = duration_years * 12

        monthly_payment = pmt(
            monthly_interest_rate, duration_months, principal)
        (remaining, interest) = evaluate_step(
                monthly_interest_rate, duration_months, principal, monthly_payment)
        print(f"{principal} for {duration_years} years at {annual_interest_rate*100:.2f}%:\
                {monthly_payment:.0f}/month costing {interest:.0f}")

if __name__ == "__main__":
    for scenario in mortgage_scenarios:
        evaluate_scenario(scenario)