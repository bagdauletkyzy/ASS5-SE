import argparse
import sys

from expenses.models import make_expense
from expenses.report import by_category, get_formatter, total
from expenses.storage import DEFAULT_FILE, load_expenses, save_expenses


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expenses")
    parser.add_argument("--file", default=DEFAULT_FILE)
    sub = parser.add_subparsers(dest="cmd")

    add = sub.add_parser("add")
    add.add_argument("date")
    add.add_argument("category")
    add.add_argument("description")
    add.add_argument("amount")

    sub.add_parser("summary")

    exp = sub.add_parser("export")
    exp.add_argument("--format", default="text")
    exp.add_argument("--out")

    args = parser.parse_args(argv)
    expenses = load_expenses(args.file)

    if args.cmd == "add":
        try:
            e = make_expense(args.date, args.category, args.description, args.amount)
        except ValueError as err:
            print("Error:", err, file=sys.stderr)
            sys.exit(2)
        expenses.append(e)
        save_expenses(expenses, args.file)
        print("Added:", e.description, e.amount)
    elif args.cmd == "summary":
        print("Total:", total(expenses))
        for cat, amt in by_category(expenses).items():
            print(" ", cat, amt)
    elif args.cmd == "export":
        try:
            formatter = get_formatter(args.format)
        except ValueError:
            print("Unknown format", args.format)
            sys.exit(1)
        ext = formatter.extension
        data = formatter.render(expenses)
        if args.out:
            out = args.out if args.out.endswith(ext) else args.out + ext
            with open(out, "w") as f:
                f.write(data)
            print("Exported to", out)
        else:
            print(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
