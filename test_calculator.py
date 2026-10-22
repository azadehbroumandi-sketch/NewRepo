import subprocess
import sys
import unittest
from pathlib import Path

from calculator import add, calculate, divide, multiply, subtract


class CalculatorTests(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(subtract(7, 4), 3)
        self.assertEqual(multiply(6, 5), 30)
        self.assertEqual(divide(9, 3), 3)

    def test_fractional_division(self):
        self.assertAlmostEqual(divide(1, 4), 0.25)

    def test_calculate_accepts_symbolic_operations(self):
        self.assertEqual(calculate("+", 2, 8), 10)
        self.assertEqual(calculate("multiply", 3, 4), 12)
        self.assertEqual(calculate("ADD", 2, 8), 10)

    def test_invalid_values_raise_value_error_for_both_arguments(self):
        invalid_values = ("not a number", True, False, float("nan"), float("inf"), float("-inf"))
        for operation in (add, subtract, multiply, divide):
            for position in (0, 1):
                for value in invalid_values:
                    args = [1, 1]
                    args[position] = value
                    with self.subTest(operation=operation.__name__, position=position, value=value):
                        with self.assertRaises(ValueError):
                            operation(*args)

    def test_calculate_rejects_invalid_operations(self):
        with self.assertRaises(ValueError):
            calculate("modulo", 5, 2)
        with self.assertRaises(ValueError):
            calculate(123, 5, 2)

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_cli_operations_and_fractional_output(self):
        for operation, a, b, expected in (("+", "2", "3", "5.0"), ("-", "7", "4", "3.0"), ("*", "6", "5", "30.0"), ("/", "1", "4", "0.25")):
            with self.subTest(operation=operation):
                result = self.run_cli(operation, a, b)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stdout.strip(), expected)
                self.assertEqual(result.stderr, "")

    def test_cli_reports_division_by_zero(self):
        result = self.run_cli("/", "10", "0")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot divide by zero", result.stderr)

    def test_cli_reports_invalid_numbers(self):
        result = self.run_cli("+", "not-a-number", "2")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid float value", result.stderr)

        result = self.run_cli("+", "nan", "2")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be finite", result.stderr)

    @staticmethod
    def run_cli(*args):
        return subprocess.run(
            [sys.executable, str(Path(__file__).with_name("calculator.py")), *args],
            capture_output=True,
            text=True,
            check=False,
        )


if __name__ == "__main__":
    unittest.main()
