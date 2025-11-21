import logging
from typing import Union

# Configure logging only in your main script, not in libraries
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


NumberLike = Union[int, float, str]


class InvalidInputError(Exception):
    def __init__(self, value: object) -> None:
        self.value = value
        message = f"{value!r} is not a number."
        super().__init__(message)


class DivisionByZeroError(Exception):
    def __init__(self, numerator: float, denominator: float) -> None:
        self.numerator = numerator
        self.denominator = denominator
        message = (
            f"Tried to divide {numerator} by {denominator}, "
            "but division by zero is not allowed."
        )
        super().__init__(message)


class InvalidOperatorError(Exception):
    def __init__(self, operator: str) -> None:
        self.operator = operator
        message = (
            f"Invalid operator {operator!r}. "
            "Only 'add', 'subtract', 'multiply', 'divide' are allowed."
        )
        super().__init__(message)


def to_float(value: NumberLike) -> float:
    """
    Convert int/float/str to float or raise InvalidInputError.
    """
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        # Wrap the low-level conversion error in a domain-specific error
        raise InvalidInputError(value) from exc


def calculator(number_a: NumberLike, number_b: NumberLike, operator: str) -> float:
    """
    Perform a simple calculation or raise a domain-specific error.
    """
    a = to_float(number_a)
    b = to_float(number_b)

    if operator not in ("add", "subtract", "multiply", "divide"):
        raise InvalidOperatorError(operator)

    match operator:
        case "add":
            return a + b
        case "subtract":
            return a - b
        case "multiply":
            return a * b
        case "divide":
            if b == 0:
                raise DivisionByZeroError(a, b)
            return a / b
        case _:
            # Should never be reached due to the earlier check,
            # but keeps mypy/pylance happy and is defensive.
            raise InvalidOperatorError(operator)


def main() -> None:
    try:
        result = calculator("10a", "0", "divide")
        print("Result:", result)
    except (InvalidInputError, InvalidOperatorError, DivisionByZeroError) as exc:
        # One place where we log, with full context if desired
        logger.error("Calculator failed: %s", exc, exc_info=True)


if __name__ == "__main__":
    main()
