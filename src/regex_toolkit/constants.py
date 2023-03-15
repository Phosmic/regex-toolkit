"""Constant values.

This module contains constant values used throughout the project.
"""

from typing import Final

from regex_toolkit.enums import RegexFlavor

__all__ = [
    "ALWAYS_ESCAPE",
    "ALWAYS_SAFE",
    "ASCIILETTERS",
    "DIGITS",
]

DIGITS: Final[frozenset[str]] = frozenset(map(chr, b"0123456789"))
ASCIILETTERS: Final[frozenset[str]] = frozenset(
    map(chr, b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
)
ALWAYS_SAFE: Final[frozenset[str]] = DIGITS | ASCIILETTERS
ALWAYS_ESCAPE: Final[frozenset[str]] = frozenset(
    map(chr, b"()[]{}?*+-|^$\\.&~# \t\n\r\v\f")
)

REGEX_FLAVORS: Final[frozenset[RegexFlavor]] = frozenset(
    {RegexFlavor.RE, RegexFlavor.RE2}
)
