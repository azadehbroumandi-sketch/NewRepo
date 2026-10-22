import contextlib
import io
import unittest

import calculator


class CalculatorOperationsTest(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calculator.add(2, 3), 5)
        self.assertEqual(calculator.subtract(7, 4), 3)
        self.assertEqual(calculator.multiply(6, 5), 30)
        self.assertEqual(calculator.divide(9, 3), 3)

    def test_calculate_dispatches_operators(self):
        self.assertEqual(calculator.calculate(2, 3, "+"), 5)
        self.assertEqual(calculator.calculate(8, 2, "/"), 4)

    def test_division_by_zero_raises_clear_error(self):
        with self.assertRaisesRegex(ZeroDivisionError, "cannot divide by zero"):
            calculator.divide(1, 0)


class CalculatorInputTest(unittest.TestCase):
    def test_unknown_operator_is_invalid(self):
        with self.assertRaisesRegex(ValueError, "unknown operator"):
            calculator.calculate(1, 2, "%")

    def test_cli_rejects_non_numeric_input(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            status = calculator.main(["not-a-number", "+", "2"])

        self.assertEqual(status, 2)
        self.assertIn("invalid input", error.getvalue())

    def test_cli_rejects_division_by_zero(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            status = calculator.main(["10", "/", "0"])

        self.assertEqual(status, 2)
        self.assertIn("cannot divide by zero", error.getvalue())


if __name__ == "__main__":
    unittest.main()
