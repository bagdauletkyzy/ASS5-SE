import json
import os

from expenses.models import Expense, expense_from_dict, expense_to_dict

DEFAULT_FILE = "expenses.json"


def load_expenses(path=DEFAULT_FILE):
    if not os.path.exists(path):
        return []
    with open(path) as f:
        raw = json.load(f)
    return [expense_from_dict(item) for item in raw]


def save_expenses(expenses, path=DEFAULT_FILE):
    with open(path, "w") as f:
        json.dump([expense_to_dict(e) for e in expenses], f, indent=2)
