import json
import shutil
from pathlib import Path

import pytest

from expenses.cli import main

SAMPLE = Path(__file__).resolve().parent.parent / "sample_data.json"


@pytest.fixture
def data_file(tmp_path):
    p = tmp_path / "data.json"
    shutil.copy(SAMPLE, p)
    return p


def test_ac1_add_then_summary(tmp_path, capsys):
    f = tmp_path / "new.json"
    main(["--file", str(f), "add", "2026-11-05", "food", "Coffee", "900"])
    main(["--file", str(f), "summary"])
    out = capsys.readouterr().out
    assert "Total: 900.0" in out
    assert json.loads(f.read_text())[0]["amount"] == 900.0


@pytest.mark.parametrize("fmt,first_line", [
    ("csv", "date,category,description,amount"),
    ("json", "["),
    ("text", "2026-11-01  food         Lunch at canteen             2500.00"),
])
def test_ac2_export_formats(data_file, capsys, fmt, first_line):
    main(["--file", str(data_file), "export", "--format", fmt])
    assert capsys.readouterr().out.splitlines()[0] == first_line


def test_ac2_export_to_file_adds_extension(data_file, tmp_path):
    out = tmp_path / "report"
    main(["--file", str(data_file), "export", "--format", "csv", "--out", str(out)])
    assert (tmp_path / "report.csv").exists()


def test_ac2_unknown_format_exits_1(data_file, capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--file", str(data_file), "export", "--format", "xml"])
    assert exc.value.code == 1
    assert "Unknown format" in capsys.readouterr().out


def test_ac3_read_only_commands_do_not_modify_data(data_file):
    before = data_file.read_bytes()
    main(["--file", str(data_file), "summary"])
    for fmt in ("text", "csv", "json"):
        main(["--file", str(data_file), "export", "--format", fmt])
    assert data_file.read_bytes() == before
