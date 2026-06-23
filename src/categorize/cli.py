"""Command-line interface for categorize."""

import argparse
import sys

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="categorize",
        description="A CLI tool to categorize things.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "items",
        nargs="*",
        help="Items to categorize.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.items:
        parser.print_help()
        return 0

    for item in args.items:
        print(f"categorizing: {item}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
