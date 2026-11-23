import json

import pytest

from expenses.cli import main


@pytest.mark.parametrize("date,amount", [
    ("2026-11-01", "-5000"),     # negative
    ("2026-11-01", "0"),         # zero
    ("2026-11-01", "nan"),       # not a number
    ("2026-11-01", "inf"),       # infinite
    ("2026-11-01", "abc"),       # non-numeric
    ("2026-02-30", "100"),       # impossible date
    ("not-a-date", "100"),       # malformed date
])
def test_ac4_invalid_input_rejected_and_not_saved(tmp_path, capsys, date, amount):
    f = tmp_path / "data.json"
    with pytest.raises(SystemExit) as exc:
        main(["--file", str(f), "add", date, "food", "Bad", "--", amount]
             if amount.startswith("-") else
             ["--file", str(f), "add", date, "food", "Bad", amount])
    assert exc.value.code == 2
    assert "Error:" in capsys.readouterr().err
    assert not f.exists()


def test_ac4_valid_input_still_accepted(tmp_path):
    f = tmp_path / "data.json"
    main(["--file", str(f), "add", "2026-11-01", "food", "Ok", "1250.50"])
    assert json.loads(f.read_text())[0]["amount"] == 1250.50
