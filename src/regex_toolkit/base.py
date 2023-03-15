__all__ = [
    "escape",
    "string_as_exp",
    "strings_as_exp",
]
from collections.abc import Iterable

from regex_toolkit.constants import ALWAYS_ESCAPE, ALWAYS_SAFE
from regex_toolkit.enums import RegexFlavor
from regex_toolkit.utils import char_to_cpoint, iter_sort_by_len


def escape(char: str, flavor: int = 1) -> str:
    """Create a regex expression that exactly matches a character.

    Args:
        char (str): Character to match.
        flavor (int, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to 1.

    Returns:
        str: Expression that exactly matches the original character.

    Raises:
        ValueError: Invalid regex flavor.
    """
    try:
        flavor = RegexFlavor(flavor)
    except ValueError:
        raise ValueError(f"Invalid regex flavor: {flavor}")

    if flavor == RegexFlavor.RE:
        return _escape(char)
    # elif flavor == RegexFlavor.RE2:
    else:
        return _escape2(char)


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
        return "\\x{" + char_to_cpoint(char) + "}"


def string_as_exp(text: str, flavor: int = 1) -> str:
    """Create a regex expression that exactly matches a string.

    Args:
        text (str): String to match.
        flavor (int, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to 1.

    Returns:
        str: Expression that exactly matches the original string.

    Raises:
        ValueError: Invalid regex flavor.
    """
    try:
        flavor = RegexFlavor(flavor)
    except ValueError:
        raise ValueError(f"Invalid regex flavor: {flavor}")

    if flavor == RegexFlavor.RE:
        return _string_as_exp(text)
    # elif flavor == RegexFlavor.RE2:
    else:
        return _string_as_exp2(text)


def _string_as_exp(text: str) -> str:
    return r"".join(map(_escape, text))


def _string_as_exp2(text: str) -> str:
    return r"".join(map(_escape2, text))


def strings_as_exp(texts: Iterable[str], flavor: int = 1) -> str:
    """Create a regex expression that exactly matches any one string.

    Args:
        texts (Iterable[str]): Strings to match.
        flavor (int, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to 1.

    Returns:
        str: Expression that exactly matches any one of the original strings.

    Raises:
        ValueError: Invalid regex flavor.
    """
    try:
        flavor = RegexFlavor(flavor)
    except ValueError:
        raise ValueError(f"Invalid regex flavor: {flavor}")

    if flavor == RegexFlavor.RE:
        return _strings_as_exp(texts)
    # elif flavor == RegexFlavor.RE2:
    else:
        return _strings_as_exp2(texts)


def _strings_as_exp(texts: Iterable[str]) -> str:
    return r"|".join(map(_string_as_exp, iter_sort_by_len(texts, reverse=True)))


def _strings_as_exp2(texts: Iterable[str]) -> str:
    return r"|".join(map(_string_as_exp2, iter_sort_by_len(texts, reverse=True)))
