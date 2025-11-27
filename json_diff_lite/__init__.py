"""A minimal library for comparing JSON objects with human-readable output."""

from .core import diff
from .colors import format_change

__version__ = "0.4.0"
__all__ = ["diff", "format_change"]
