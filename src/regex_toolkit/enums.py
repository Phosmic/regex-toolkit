"""Enums."""

from enum import Enum


class RegexFlavor(int, Enum):
    """Regex flavors.

    Attributes:
        RE (int): Standard Python regex flavor.
        RE2 (int): Google RE2 regex flavor.
    """

    RE = 1
    RE2 = 2
