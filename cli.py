"""Command-line interface for the calculator."""

import argparse
import sys

from calculator import add, subtract, multiply, divide, power, sqrt, modulo

OPERATIONS = {
    "add": (add, 2),
    "sub": (subtract, 2),
    "mul": (multiply, 2),
    "div": (divide, 2),
    "pow": (power, 2),
    "sqrt": (sqrt, 1),
    "mod": (modulo, 2),
}


def main():
    parser = argparse.ArgumentParser(description="Calculator CLI")
    parser.add_argument("operation", choices=OPERATIONS.keys(), help="Operation to perform")
    parser.add_argument("operands", nargs="+", type=float, help="Operands for the operation")
    args = parser.parse_args()

    func, expected_args = OPERATIONS[args.operation]
    if len(args.operands) != expected_args:
        print(f"Error: '{args.operation}' requires {expected_args} operand(s), got {len(args.operands)}")
        sys.exit(1)

    try:
        result = func(*args.operands)
        print(f"{result}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
