import csv
import io
import json
from typing import Protocol

from expenses.models import Expense, expense_to_dict


def total(expenses: list[Expense]) -> float:
    return sum((e.amount for e in expenses), 0.0)


def by_category(expenses: list[Expense]) -> dict[str, float]:
    result: dict[str, float] = {}
    for e in expenses:
        result[e.category] = result.get(e.category, 0.0) + e.amount
    return result


# --- Export strategies -------------------------------------------------------
# Each format is one small class with the same interface. Adding a format means
# adding one class and one registry entry; no if/elif chains in report or CLI.

class Formatter(Protocol):
    extension: str

    def render(self, expenses: list[Expense]) -> str: ...


_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _safe_cell(value: str) -> str:
    """Neutralise spreadsheet formula injection (OWASP CSV Injection)."""
    return "'" + value if value.startswith(_FORMULA_PREFIXES) else value


class CsvFormatter:
    extension = ".csv"

    def render(self, expenses: list[Expense]) -> str:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["date", "category", "description", "amount"])
        for e in expenses:
            writer.writerow([
                _safe_cell(e.date), _safe_cell(e.category),
                _safe_cell(e.description), e.amount,
            ])
        return buf.getvalue()


class JsonFormatter:
    extension = ".json"

    def render(self, expenses: list[Expense]) -> str:
        return json.dumps([expense_to_dict(e) for e in expenses], indent=2)


class TextFormatter:
    extension = ".txt"

    def render(self, expenses: list[Expense]) -> str:
        lines = [
            f"{e.date}  {e.category:<12} {e.description:<25} {e.amount:>10.2f}"
            for e in expenses
        ]
        lines.append(f"TOTAL{'':>40}{total(expenses):>10.2f}")
        return "\n".join(lines)


FORMATTERS: dict[str, Formatter] = {
    "csv": CsvFormatter(),
    "json": JsonFormatter(),
    "text": TextFormatter(),
}


def get_formatter(fmt: str) -> Formatter:
    try:
        return FORMATTERS[fmt]
    except KeyError:
        raise ValueError(f"unknown format: {fmt}") from None


def export(expenses: list[Expense], fmt: str) -> str:
    return get_formatter(fmt).render(expenses)
