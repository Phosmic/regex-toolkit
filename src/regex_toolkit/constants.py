"""Constant values.

This module contains constant values used throughout the project.
"""

from typing import Final

__all__ = [
    "SAFE_CHARS",
    "ESCAPE_CHARS",
]

SAFE_CHARS: Final[frozenset[str]] = frozenset(
    map(chr, b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
)
ESCAPE_CHARS: Final[frozenset[str]] = frozenset(
    map(chr, b"()[]{}?*+-|^$\\.&~# \t\n\r\v\f")
)
