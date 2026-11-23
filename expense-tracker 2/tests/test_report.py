import csv

import pytest

from expenses.models import Expense
from expenses.report import by_category, export, total


def sample():
    return [
        Expense("2026-11-01", "food", "Lunch at canteen", 2500),
        Expense("2026-11-02", "transport", "Bus card top-up", 1000),
        Expense("2026-11-03", "food", "Groceries", 7400),
    ]


def test_total():
    assert total(sample()) == 10900


def test_by_category():
    assert by_category(sample()) == {"food": 9900, "transport": 1000}


def test_export_csv_has_header():
    out = export(sample(), "csv")
    assert out.splitlines()[0] == "date,category,description,amount"


def test_unknown_format_raises_value_error():

    with pytest.raises(ValueError):
        export(sample(), "xml")


@pytest.mark.parametrize("payload", [
    '=HYPERLINK("http://example.invalid","click")',
    "+1+1", "-2+3", "@SUM(A1:A2)", "\t=1+1", "\r=1+1",
])
def test_r2_csv_export_neutralises_formula_cells(payload):
    rows = [Expense("2026-11-04", "misc", payload, 100)]
    line = export(rows, "csv").splitlines()[1]
    desc_cell = next(csv.reader([line]))[2]
    assert desc_cell.startswith("'"), desc_cell


def test_r2_csv_export_keeps_normal_text_and_amounts():
    out = export(sample(), "csv").splitlines()
    assert out[1] == "2026-11-01,food,Lunch at canteen,2500"
