"""Constant values.

This module contains constant values used throughout the project.
"""

import string
from typing import Final

__all__ = [
    "ALPHA_CHARS",
    "DIGIT_CHARTS",
    "SAFE_CHARS",
    "RE2_ESCAPABLE_CHARS",
]

ALPHA_CHARS: Final[set[str]] = set(string.ascii_letters)
DIGIT_CHARTS: Final[set[str]] = set(string.digits)
SAFE_CHARS: Final[set[str]] = ALPHA_CHARS.union(DIGIT_CHARTS).union(
    set(string.whitespace)
)
RE2_ESCAPABLE_CHARS: Final[set[str]] = set(string.punctuation)
