"""Constant values.

This module contains constant values used throughout the project.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

__all__ = [
    "ALWAYS_ESCAPE",
    "ALWAYS_SAFE",
    "ASCIILETTERS",
    "DIGITS",
    "RESERVED_EXPRESSIONS",
]

DIGITS: Final[frozenset[str]] = frozenset(map(chr, b"0123456789"))
ASCIILETTERS: Final[frozenset[str]] = frozenset(
    map(chr, b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
)
ALWAYS_SAFE: Final[frozenset[str]] = DIGITS | ASCIILETTERS
ALWAYS_ESCAPE: Final[frozenset[str]] = frozenset(
    map(chr, b"()[]{}?*+-|^$\\.&~# \t\n\r\v\f")
)
RESERVED_EXPRESSIONS: Final[frozenset[str]] = frozenset(
    {"\\A", "\\b", "\\B", "\\d", "\\D", "\\s", "\\S", "\\w", "\\W", "\\Z", "\\1"}
)
