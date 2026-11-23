import math
from dataclasses import dataclass
from datetime import date as _date


@dataclass
class Expense:
    date: str          # ISO format YYYY-MM-DD
    category: str
    description: str
    amount: float      # in KZT


def make_expense(date: str, category: str, description: str, amount: str) -> Expense:
    """Build an Expense from user input, rejecting invalid values (ValueError)."""
    try:
        _date.fromisoformat(date)
    except ValueError:
        raise ValueError(f"invalid date {date!r}, expected a real date YYYY-MM-DD") from None
    try:
        value = float(amount)
    except ValueError:
        raise ValueError(f"amount {amount!r} is not a number") from None
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"amount must be a positive finite number, got {amount!r}")
    return Expense(date, category, description, value)


def expense_from_dict(data: dict) -> Expense:
    return Expense(
        date=data["date"],
        category=data["category"],
        description=data["description"],
        amount=float(data["amount"]),
    )


def expense_to_dict(e: Expense) -> dict:
    return {
        "date": e.date,
        "category": e.category,
        "description": e.description,
        "amount": e.amount,
    }
