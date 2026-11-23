# Expense Tracker

Small command-line tool to track personal expenses in a local JSON file.
Use fictional data only. Amounts are in KZT.

## Requirements
Python 3.11+

## Install
    python3 -m venv .venv && . .venv/bin/activate
    pip install -r requirements.txt

## Usage
    python3 -m expenses.cli --file sample_data.json summary
    python3 -m expenses.cli add 2026-11-01 food "Lunch" 2500
    python3 -m expenses.cli export --format csv --out report

`--file` defaults to `expenses.json` in the current directory.
Export formats: `text` (default), `csv`, `json`.

Data is stored in a JSON file (no database).

## Checks
    python3 -m pytest -q
    ruff check .
    mypy expenses

## For AI agents
See [AGENTS.md](AGENTS.md) for architecture, safe commands and forbidden actions.
