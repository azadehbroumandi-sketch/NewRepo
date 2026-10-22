"""A small reusable calculator module with a command-line interface."""

from __future__ import annotations

import sys
from numbers import Real
from typing import Sequence


def add(first: Real, second: Real) -> Real:
    """Return the sum of two numbers."""
    return first + second


def subtract(first: Real, second: Real) -> Real:
    """Return the difference between two numbers."""
    return first - second


def multiply(first: Real, second: Real) -> Real:
    """Return the product of two numbers."""
    return first * second


def divide(first: Real, second: Real) -> float:
    """Return the quotient of two numbers.

    Raises:
        ZeroDivisionError: if ``second`` is zero.
    """
    if second == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return first / second


def calculate(first: Real, second: Real, operator: str) -> Real:
    """Apply ``operator`` to two numbers."""
    operations = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    try:
        operation = operations[operator]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"unknown operator: {operator!r}") from exc
    return operation(first, second)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line calculator and return a process status code."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 3:
        print("Usage: python calculator.py <number> <operator> <number>", file=sys.stderr)
        print("Operators: +, -, *, /", file=sys.stderr)
        return 2

    first_text, operator, second_text = arguments
    try:
        first = float(first_text)
        second = float(second_text)
        result = calculate(first, second, operator)
    except ValueError as exc:
        print(f"Error: invalid input ({exc})", file=sys.stderr)
        return 2
    except ZeroDivisionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
