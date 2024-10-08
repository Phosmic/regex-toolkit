# import logging
from collections.abc import Iterable

from regex_toolkit.constants import ALWAYS_ESCAPE, ALWAYS_SAFE
from regex_toolkit.enums import ALL_REGEX_FLAVORS, RegexFlavor
from regex_toolkit.utils import char_to_cpoint, iter_sort_by_len_and_alpha

__all__ = [
    "default_flavor",
    "escape",
    "make_exp",
    "string_as_exp",
    "strings_as_exp",
    "resolve_flavor",
]

# logger: logging.Logger = logging.getLogger(__name__)

default_flavor: int | RegexFlavor | None = RegexFlavor.RE


def resolve_flavor(flavor: int | RegexFlavor | None) -> RegexFlavor:
    if flavor is not None:
        try:
            return RegexFlavor(flavor)
        except ValueError:
            raise ValueError(
                f"Invalid regex flavor: {flavor!r}. Valid flavors are: {[f.value for f in ALL_REGEX_FLAVORS]}."
            )
    elif default_flavor is not None:
        try:
            return RegexFlavor(default_flavor)
        except ValueError:
            raise ValueError(
                f"Invalid default regex flavor: {default_flavor!r}. Valid flavors are: {[f.value for f in ALL_REGEX_FLAVORS]}."
            )
    else:
        raise ValueError("No regex flavor provided and no default is set.")


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

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.escape("a")
    # Output: 'a'
    rtk.escape(".")
    # Output: '\\.'
    rtk.escape("/")
    # Output: '/'

    rtk.escape(".", flavor=2)
    # Output: '\\.'
    rtk.escape("a", flavor=2)
    # Output: 'a'
    rtk.escape("/", flavor=2)
    # Output: '\\x{002f}'
    ```

    Args:
        char (str): Character to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches the original character.

    Raises:
        ValueError: Invalid regex flavor.
        TypeError: Invalid type for `char`.
    """
    flavor = resolve_flavor(flavor)
    if not isinstance(char, str):
        raise TypeError(
            f"escape() expected string of length 1, but found {type(char).__name__}"
        )
    if len(char) != 1:
        raise TypeError(
            f"escape() expected string of length 1, but string of length {len(char)} found"
        )
    if flavor == RegexFlavor.RE:
        return _escape(char)
    else:
        return _escape2(char)


def _string_as_exp(text: str) -> str:
    return r"".join(map(_escape, text))


def _string_as_exp2(text: str) -> str:
    return r"".join(map(_escape2, text))


def string_as_exp(text: str, flavor: int | None = None) -> str:
    """Create a regex expression that exactly matches a string.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.string_as_exp("http://www.example.com")
    # Output: 'https\\:\\/\\/example\\.com'

    rtk.string_as_exp("http://www.example.com", flavor=2)
    # Output: 'https\\x{003a}\\x{002f}\\x{002f}example\\.com'
    ```

    Args:
        text (str): String to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches the original string.

    Raises:
        ValueError: Invalid regex flavor.
    """
    if resolve_flavor(flavor) == RegexFlavor.RE:
        return _string_as_exp(text)
    else:
        return _string_as_exp2(text)


def _strings_as_exp(texts: Iterable[str]) -> str:
    return r"|".join(map(_string_as_exp, iter_sort_by_len_and_alpha(texts)))


def _strings_as_exp2(texts: Iterable[str]) -> str:
    return r"|".join(map(_string_as_exp2, iter_sort_by_len_and_alpha(texts)))


def strings_as_exp(texts: Iterable[str], flavor: int | None = None) -> str:
    """Create a regex expression that exactly matches any one string.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.strings_as_exp(["apple", "banana", "cherry"])
    # Output: 'banana|cherry|apple'

    rtk.strings_as_exp(["apple", "banana", "cherry"], flavor=2)
    # Output: 'banana|cherry|apple'
    ```

    Args:
        texts (Iterable[str]): Strings to match.
        flavor (int | None, optional): Regex flavor (1 for RE, 2 for RE2). Defaults to None.

    Returns:
        str: Expression that exactly matches any one of the original strings.

    Raises:
        ValueError: Invalid regex flavor.
    """
    flavor = resolve_flavor(flavor)
    unique_texts = set(texts)
    # if all(map(lambda text: len(text) == 1, unique_texts)):
    #     logger.warning(
    #         "All strings are of length 1. Consider using make_exp() instead."
    #     )
    if flavor == RegexFlavor.RE:
        return _strings_as_exp(unique_texts)
    else:
        return _strings_as_exp2(unique_texts)


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
    import regex_toolkit as rtk

    "[" + rtk.make_exp(["a", "b", "c", "z", "y", "x"]) + "]"
    # Output: '[a-cx-z]'

    "[" + rtk.make_exp(["a", "b", "c", "z", "y", "x"], flavor=2) + "]"
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
    func = (
        _make_group_exp
        if resolve_flavor(flavor) == RegexFlavor.RE
        else _make_group_exp2
    )

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
            group.clear()
            group.append(char_ord)
    if group:
        # Make any remaining group
        exp += func(group)
    return exp
