"""A small calculator supporting the four basic arithmetic operations."""

from __future__ import annotations

import argparse
import math
from numbers import Real
from typing import Callable


def _validate_number(value: object, name: str) -> float | int:
    """Validate and return a finite real number."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a real number")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def add(a: object, b: object) -> float | int:
    """Return the sum of *a* and *b*."""
    return _validate_number(a, "a") + _validate_number(b, "b")


def subtract(a: object, b: object) -> float | int:
    """Return *a* minus *b*."""
    return _validate_number(a, "a") - _validate_number(b, "b")


def multiply(a: object, b: object) -> float | int:
    """Return the product of *a* and *b*."""
    return _validate_number(a, "a") * _validate_number(b, "b")


def divide(a: object, b: object) -> float | int:
    """Return *a* divided by *b*.

    Raises:
        ZeroDivisionError: if *b* is zero.
        ValueError: if either argument is not a finite real number.
    """
    left = _validate_number(a, "a")
    right = _validate_number(b, "b")
    if right == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return left / right


_OPERATIONS: dict[str, Callable[[object, object], float | int]] = {
    "+": add,
    "add": add,
    "-": subtract,
    "subtract": subtract,
    "*": multiply,
    "multiply": multiply,
    "/": divide,
    "divide": divide,
}


def calculate(operation: str, a: object, b: object) -> float | int:
    """Perform a named or symbolic basic arithmetic operation."""
    if not isinstance(operation, str) or operation.lower() not in _OPERATIONS:
        raise ValueError(f"unsupported operation: {operation!r}")
    return _OPERATIONS[operation.lower()](a, b)


def main() -> None:
    parser = argparse.ArgumentParser(description="Perform basic arithmetic")
    parser.add_argument("operation", choices=("+", "-", "*", "/"))
    parser.add_argument("a", type=float)
    parser.add_argument("b", type=float)
    args = parser.parse_args()
    try:
        print(calculate(args.operation, args.a, args.b))
    except (ValueError, ZeroDivisionError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
