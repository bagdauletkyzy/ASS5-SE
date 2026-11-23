# AGENTS.md — Expense Tracker

Instructions for AI coding agents (Claude Code, Codex, Cursor, Copilot) working in this repository.
Humans should read README.md first; this file adds the rules an agent must follow.

## 1. Purpose
A small command-line tool that records personal expenses (fictional data only) in a local JSON file
and prints summaries / exports (text, CSV, JSON). No network, no database, no login.

## 2. Architecture (read this before editing)
| Path | Responsibility |
|---|---|
| `expenses/models.py` | `Expense` dataclass, dict conversion, input validation |
| `expenses/storage.py` | Load/save the JSON data file (only module that touches the data file) |
| `expenses/report.py` | Pure functions: totals, per-category sums, export formatters (Strategy registry) |
| `expenses/cli.py` | argparse entry point; UI only — no business rules here |
| `tests/` | pytest unit tests; one file per module |
| `sample_data.json` | Fictional sample data. Never replace with real personal data |

Entry point: `python3 -m expenses.cli` (there is no `main.py`).

## 3. Setup
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```
Python 3.11+ is required (uses `X | Y` type syntax and `list[...]` generics).

## 4. Safe commands (allowed without asking)
```bash
python3 -m pytest -q                 # unit tests — must pass before you finish
ruff check .                         # lint (read-only; do NOT run with --fix on unrelated files)
mypy expenses                        # type check
python3 -m expenses.cli --file sample_data.json summary
python3 -m expenses.cli --file /tmp/scratch.json add 2026-11-01 food "Test" 100
git status / git diff / git log
```
Always pass `--file` pointing at `sample_data.json` or a file under `/tmp` when running the CLI,
so you never overwrite a user's `expenses.json`.

## 5. Coding conventions
- Python 3.11+, type hints on all new/changed functions; keep `mypy expenses` clean for touched files.
- Business rules (validation, totals, formatting) live in `models.py` / `report.py`, not in `cli.py`.
- New export format = add one formatter class to `FORMATTERS` in `report.py`; do not add new `if fmt == ...` chains.
- Small, focused diffs. One concern per commit. No drive-by refactoring of unrelated code.

## 6. Test expectations
- Every bug fix or behaviour change comes with a regression test in `tests/`.
- Do not delete, skip or weaken existing tests to make a change pass.
- Report the exact command and the pass/fail totals. Never claim a test passed that you did not run.

## 7. Acceptance criteria that must stay true
- AC1 `add` stores a valid expense and `summary` shows the correct total and per-category sums.
- AC2 `export` supports `text`, `csv`, `json`; an unknown format exits with code 1 and a clear message.
- AC3 Existing stored data is never modified by `summary` or `export` (read-only commands).
- AC4 Invalid input (non-positive / non-numeric amount, impossible date) is rejected with a clear error, exit code 2, and nothing is saved.
- AC5 `python3 -m pytest -q` passes.

## 8. Forbidden actions (never do these)
- Never add, print, commit or request secrets, tokens, passwords or real personal/financial data.
- Never deploy, publish to PyPI, push to `main`, force-push, or rewrite git history.
- Never run destructive commands (`rm -rf`, `git reset --hard`, `git clean -fdx`) or delete user data files.
- Never add, remove or upgrade dependencies (`pip install <new>`, editing `requirements.txt`) without explicit human approval.
- Never make network calls or add code that does.
- Never disable tests, linters or type checks to get a green result.

## 9. Review gates
- Work on a feature branch (`agent/<topic>`); a human reviews the diff and the test output before merge.
- Your final message must contain: summary of change, files touched, commands run with results, open risks.
- Changes to `storage.py` (data file handling) or `AGENTS.md` itself always need explicit human approval.
