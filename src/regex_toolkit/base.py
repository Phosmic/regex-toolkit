__all__ = [
    "default_flavor",
    "escape",
    "string_as_exp",
    "strings_as_exp",
    "make_exp",
]
from collections.abc import Iterable

from regex_toolkit.constants import ALWAYS_ESCAPE, ALWAYS_SAFE
from regex_toolkit.enums import RegexFlavor
from regex_toolkit.utils import (
    char_to_cpoint,
    iter_sort_by_len,
    resolve_flavor,
)

default_flavor: int | RegexFlavor | None = RegexFlavor.RE


def _escape(char: str) -> str:
    if char in ALWAYS_SAFE:
        # Safe as-is
        return char
    else:
        # Safe to escape with backslash
        return f"\\{char}"


def _escape2(char: str) -> str:
    if char in ALWAYS_SAFE:
        # Safe as-is
        return char
    elif char in ALWAYS_ESCAPE:
        # Safe to escape with backslash
        return f"\\{char}"
    else:
        # Otherwise escape using the codepoint
        return "\\x{" + char_to_cpoint(char).removeprefix("0000") + "}"


def escape(char: str, flavor: int | None = None) -> str:
    """Create a regex expression that exactly matches a character.

    Args:
        char (str): Character to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches the original character.

    Raises:
        ValueError: Invalid regex flavor.
    """
    if (flavor := resolve_flavor(flavor)) == RegexFlavor.RE:
        return _escape(char)
    return _escape2(char)


def _string_as_exp(text: str) -> str:
    return r"".join(map(_escape, text))


def _string_as_exp2(text: str) -> str:
    return r"".join(map(_escape2, text))


def string_as_exp(text: str, flavor: int | None = None) -> str:
    """Create a regex expression that exactly matches a string.

    Args:
        text (str): String to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches the original string.

    Raises:
        ValueError: Invalid regex flavor.
    """
    if (flavor := resolve_flavor(flavor)) == RegexFlavor.RE:
        return _string_as_exp(text)
    return _string_as_exp2(text)


def _strings_as_exp(texts: Iterable[str]) -> str:
    return r"|".join(map(_string_as_exp, iter_sort_by_len(texts, reverse=True)))


def _strings_as_exp2(texts: Iterable[str]) -> str:
    return r"|".join(map(_string_as_exp2, iter_sort_by_len(texts, reverse=True)))


def strings_as_exp(texts: Iterable[str], flavor: int | None = None) -> str:
    """Create a regex expression that exactly matches any one string.

    Args:
        texts (Iterable[str]): Strings to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches any one of the original strings.

    Raises:
        ValueError: Invalid regex flavor.
    """
    if (flavor := resolve_flavor(flavor)) == RegexFlavor.RE:
        return _strings_as_exp(texts)
    return _strings_as_exp2(texts)


def _make_group_exp(group: list[int]) -> str:
    if len(group) > 2:
        # Represent as a character range
        return _escape(chr(group[0])) + "-" + _escape(chr(group[-1]))
    else:
        # Represent as individual characters
        return "".join((_escape(chr(char_ord)) for char_ord in group))


def _make_group_exp2(group: list[int]) -> str:
    if len(group) > 2:
        # Represent as a character range
        return _escape2(chr(group[0])) + "-" + _escape2(chr(group[-1]))
    else:
        # Represent as individual characters
        return "".join((_escape2(chr(char_ord)) for char_ord in group))


def make_exp(chars: Iterable[str], flavor: int | None = None) -> str:
    """Create a regex expression that exactly matches a list of characters.

    The characters are sorted and grouped into ranges where possible.
    The expression is not anchored, so it can be used as part of a larger expression.

    Example:

    ```python
    exp = "[" + make_exp(["a", "b", "c", "z", "y", "x"]) + "]"
    # Output: '[a-cx-z]'
    ```

    Args:
        chars (Iterable[str]): Characters to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches the original characters.

    Raises:
        ValueError: Invalid regex flavor.
    """
    if (flavor := resolve_flavor(flavor)) == RegexFlavor.RE:
        func = _make_group_exp
    func = _make_group_exp2

    exp = ""
    group = []
    for char_ord in sorted(set(map(ord, chars))):
        if not group:
            # Start first group
            group.append(char_ord)
        elif char_ord == group[-1] + 1:
            # Add to current group
            group.append(char_ord)
        else:
            # Make the group and start a new one
            exp += func(group)
            group = [char_ord]
    if group:
        # Make any remaining group
        exp += func(group)
    return exp
