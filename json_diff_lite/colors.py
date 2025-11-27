"""ANSI color support for terminal output."""

import sys


class Colors:
    """ANSI color codes."""

    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"


def supports_color():
    """Check if the terminal supports colors."""
    if not hasattr(sys.stdout, "isatty"):
        return False
    if not sys.stdout.isatty():
        return False
    return True


def colorize(text, color):
    """Apply color to text if supported."""
    if not supports_color():
        return text
    return f"{color}{text}{Colors.RESET}"


def format_change(change, use_color=True):
    """Format a change line with optional color.

    Args:
        change: The change string (e.g., "+ key: value")
        use_color: Whether to apply colors

    Returns:
        Formatted string with or without ANSI colors
    """
    if not use_color or not supports_color():
        return change

    if change.startswith("+"):
        return colorize(change, Colors.GREEN)
    elif change.startswith("-"):
        return colorize(change, Colors.RED)
    elif change.startswith("~"):
        return colorize(change, Colors.YELLOW)

    return change
