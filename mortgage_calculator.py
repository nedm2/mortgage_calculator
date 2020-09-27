from typing import Tuple, List

"""
e.g. 491750, 35 years 2.9%
e.g. 491750, 1 year 2.5%, 34 years 2.9%
e.g. 245875, 35 year 2.5%, 245875 2.9%
e.g. 491750, cashback 2% after 2 months, pay that off on variable, rest on fixed
e.g. 491750, pay off 50000 after 1 year, rest on fixed

paramaterization
[(principal, total_duration, [rate, duration]), ...]
"""

mortgage_scenarios : List[List[Tuple[int, int, List[Tuple[float, int]]]]] = [
    [(150000, 35, [(0.0195, 35)])]
  , [(150000, 35, [(0.022, 35)])]
  , [(150000, 35, [(0.023, 35)])]
  , [(150000, 35, [(0.025, 35)])]
  , [(300000, 35, [(0.0195, 35)])]
  , [(300000, 35, [(0.022, 35)])]
  , [(300000, 35, [(0.023, 35)])]
  , [(300000, 35, [(0.025, 35)])]
  , [(491750, 35, [(0.0195, 35)])]
  , [(491750, 35, [(0.022, 35)])]
  , [(491750, 35, [(0.023, 35)])]
  , [(491750, 35, [(0.025, 35)])]
  , [(491750, 35, [(0.029, 35)])]
  , [(491750, 35, [(0.035, 35)])]
  , [(491750, 30, [(0.025, 30)])]
  , [(491750, 30, [(0.029, 30)])]
  , [(491750, 30, [(0.035, 30)])]
]

def step_iter(
        rate : float,
        periods : int,
        principal : float,
        payment : float
    )-> Tuple[float, float]:
    """
    Evaluates the status of the loan following the passed number of periods.
    :param rate: Interest rate in this step
    :param periods: Number of periods covered in this step
    :param principal: Value of loan at start of this step
    :param payment: Amount paid off in each period of this step
    Returns (remaining loan value, interest paid in this step)
    """
    interest_acc : float = 0
    for period in range(periods):
        interest = principal * rate
        interest_acc += interest
        principal = principal + interest - payment
    return (principal, interest_acc)

def step(i : float, n : int, P : float, A : float) -> Tuple[float, float]:
    remaining_principal = P*(1+i)**n - A*((1+i)**n - 1)/i
    interest_paid = (P*i - A)*((1+i)**n - 1)/i + A*n
    return(remaining_principal, interest_paid)


def pmt(i : float, n : int, P :float):
    return P*(i*(i+1)**n)/((1+i)**n - 1)

def pmt_iter(rate, periods, present_value):
    payment: float = 1000
    while True:
        remaining = present_value
        for period in range(periods):
            interest = remaining * rate
            remaining = remaining + interest - payment
        if abs(remaining) < 0.1:
            return payment
        payment += remaining/periods

def evaluate_scenario(scenario : List):
    total_interest_paid: float = 0
    for (principal, duration_years, steps) in scenario:
        annual_interest_rate = steps[0][0]
        monthly_interest_rate = (1+annual_interest_rate)**(1.0/12) - 1
        duration_months = duration_years * 12

        monthly_payment = pmt(
            monthly_interest_rate, duration_months, principal)
        (remaining, interest) = step(
                monthly_interest_rate, duration_months, principal, monthly_payment)
        total_interest_paid += interest
        print(f"{principal} for {duration_years} years at {annual_interest_rate*100:.2f}%:\
                {monthly_payment:.0f}/month costing {interest:.0f}")

if __name__ == "__main__":
    for scenario in mortgage_scenarios:
        evaluate_scenario(scenario)
