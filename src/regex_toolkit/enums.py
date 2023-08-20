"""Enums."""

from enum import Enum

__all__ = [
    "ALL_REGEX_FLAVORS",
    "RegexFlavor",
]


class RegexFlavor(int, Enum):
    """Regex flavors.

    Attributes:
        RE (int): Standard Python regex flavor.
        RE2 (int): Google RE2 regex flavor.
    """

    RE = 1
    RE2 = 2


ALL_REGEX_FLAVORS: list[RegexFlavor] = [RegexFlavor.RE, RegexFlavor.RE2]
