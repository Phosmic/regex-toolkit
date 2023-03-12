"""Constant values.

This module contains constant values used throughout the project.
"""

from typing import Final

__all__ = [
    "ALWAYS_SAFE",
    "ALWAYS_ESCAPED",
    "ASCIILETTERS",
    "DIGITS",
]
DIGITS: Final[frozenset[str]] = frozenset("0123456789")
ASCIILETTERS: Final[frozenset[str]] = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
)
ALWAYS_SAFE: Final[frozenset[str]] = frozenset() | DIGITS | ASCIILETTERS
ALWAYS_ESCAPED: Final[frozenset[str]] = frozenset(
    map(chr, b"()[]{}?*+-|^$\\.&~# \t\n\r\v\f")
)
