from typing import Tuple, List
import unittest

from mortgage_calculator import pmt, pmt_iter, step, step_iter

class TestMortgageCalculator(unittest.TestCase):
    def test_pmt(self):
        tests : List[Tuple[float, int, float]] = [
                (0.004, 50, 100000),
                (0.002, 30, 200000),
                ]
        for test in tests:
            self.assertAlmostEqual(pmt(*test), pmt_iter(*test), places=2)
            A = pmt(*test)
            step_result = step(*test, A)
            step_iter_result = step_iter(*test, A)
            self.assertAlmostEqual(step_result[0], step_iter_result[0], places=2)
            self.assertAlmostEqual(step_result[1], step_iter_result[1], places=2)

if __name__ == '__main__':
    unittest.main()
