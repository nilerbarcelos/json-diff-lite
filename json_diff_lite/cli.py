"""Command-line interface for json-diff-lite."""

import argparse
import json
import sys

from .core import diff


def main():
    """Main entry point for the CLI."""
    # Handle --version before argparse to avoid requiring positional args
    if "-v" in sys.argv or "--version" in sys.argv:
        from . import __version__
        print(f"json-diff-lite {__version__}")
        return 0

    parser = argparse.ArgumentParser(
        prog="json-diff-lite",
        description="Compare two JSON files and show differences",
    )
    parser.add_argument("file1", help="First JSON file (original)")
    parser.add_argument("file2", help="Second JSON file (new)")
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Exit with code 1 if differences found, without output",
    )

    args = parser.parse_args()

    try:
        with open(args.file1, "r", encoding="utf-8") as f:
            data1 = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file1}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.file1}: {e}", file=sys.stderr)
        return 2

    try:
        with open(args.file2, "r", encoding="utf-8") as f:
            data2 = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file2}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.file2}: {e}", file=sys.stderr)
        return 2

    changes = diff(data1, data2)

    if args.quiet:
        return 1 if changes else 0

    if not changes:
        print("No differences found.")
        return 0

    for change in changes:
        print(change)

    return 1


if __name__ == "__main__":
    sys.exit(main())
