from typing import Tuple, List
import argparse

"""
e.g. 491750, 35 years 2.9%
e.g. 491750, 1 year 2.5%, 34 years 2.9%
e.g. 245875, 35 year 2.5%, 245875 2.9%
e.g. 491750, cashback 2% after 2 months, pay that off on variable, rest on fixed
e.g. 491750, pay off 50000 after 1 year, rest on fixed

paramaterization
[(principal, total_duration, [rate, duration]), ...]
"""

class MortgageScenario:
    def __init__(
            self,
            principal : float,
            steps : List[Tuple[float, int, int]]
        ):
        """
        :param principal: Total principal of the mortgage
        :param steps: Steps of (rate, maturity, fixed_term)
        """
        self.principal = principal
        self.steps = steps


mortgage_scenarios : List[MortgageScenario] = [
    MortgageScenario(150000, [(0.023, 35, 5), (0.0195, 30, 30)]),
    MortgageScenario(300000, [(0.023, 35, 3), (0.0195, 32, 32)]),
    MortgageScenario(300000, [(0.023, 35, 35)]),
    MortgageScenario(400000, [(0.0195, 35, 35)]),
    MortgageScenario(400000, [(0.0195, 35, 5), (0.0195, 30, 30)]),
    MortgageScenario(500000, [(0.023, 35, 5), (0.0195, 30, 30)]),
    MortgageScenario(500000, [(0.023, 35, 3), (0.0195, 32, 32)]),
    MortgageScenario(500000, [(0.023, 35, 35)]),
    MortgageScenario(500000, [(0.0195, 35, 35)]),
    MortgageScenario(500000, [(0.0195, 35, 5), (0.0195, 30, 30)]),
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

def evaluate_scenario(scenario : MortgageScenario):
    """
    Evaluates a mortgage scenario and displays the principal, payment and
    interest after each step.
    :param scenario: List of steps to play out a particular scenario
    """
    assert (scenario.steps[-1][1] == scenario.steps[-1][2]), "Final step must have equal maturity and term"
    print("scenario:")
    total_interest_paid: float = 0
    remaining_principal: float = scenario.principal
    for (apr, maturity_years, fixed_term_years) in scenario.steps:
        monthly_rate = (1+apr)**(1.0/12) - 1
        maturity_months = maturity_years * 12
        fixed_term_months = fixed_term_years * 12

        monthly_payment = pmt(monthly_rate, maturity_months, remaining_principal)
        (remaining, interest) = step(
                monthly_rate, fixed_term_months, remaining_principal, monthly_payment)
        total_interest_paid += interest
        print(f"\t{remaining_principal:.2f} over {maturity_years} years for {fixed_term_years} years at {apr*100:.2f}%:\
                {monthly_payment:.0f}/month costing {interest:.0f}")
        remaining_principal = remaining
    print(f"\tTOTAL COST = {total_interest_paid:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate mortgage scenarios')
    parser.add_argument("--file", type=str, default="")
    args = parser.parse_args()

    for scenario in mortgage_scenarios:
        evaluate_scenario(scenario)
