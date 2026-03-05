"""A simple calculator module demonstrating stacked PRs with ghstack."""

import math


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exponent: float) -> float:
    return base**exponent


def sqrt(a: float) -> float:
    if a < 0:
        raise ValueError("Cannot compute square root of a negative number")
    return math.sqrt(a)


def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot compute modulo with zero divisor")
    return a % b
