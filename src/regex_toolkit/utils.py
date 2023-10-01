import unicodedata
from collections.abc import Generator, Iterable

import regex_toolkit.base
from regex_toolkit.enums import RegexFlavor

__all__ = [
    "char_range",
    "char_to_cpoint",
    "cpoint_to_ord",
    "iter_char_range",
    "iter_sort_by_len",
    "mask_span",
    "mask_spans",
    "ord_to_cpoint",
    "resolve_flavor",
    "sort_by_len",
    "to_nfc",
    "to_utf8",
]


def resolve_flavor(potential_flavor: int | RegexFlavor | None) -> RegexFlavor:
    """Resolve a regex flavor.

    If the flavor is an integer, it is validated and returned.
    If the flavor is a RegexFlavor, it is returned.
    If the flavor is None, the default flavor is returned. To change the default flavor, set `default_flavor`.

    ```python
    import regex_toolkit as rtk

    rtk.base.default_flavor = 2
    assert rtk.utils.resolve_flavor(None) == rtk.enums.RegexFlavor.RE2
    ```

    Args:
        potential_flavor (int | RegexFlavor | None): Potential regex flavor.

    Returns:
        RegexFlavor: Resolved regex flavor.

    Raises:
        ValueError: Invalid regex flavor.
    """
    try:
        return RegexFlavor(potential_flavor)
    except ValueError as err:
        if regex_toolkit.base.default_flavor is not None:
            try:
                return RegexFlavor(regex_toolkit.base.default_flavor)
            except ValueError as err:
                raise ValueError(f"Invalid regex flavor: {potential_flavor}") from err
        else:
            raise ValueError(f"Invalid regex flavor: {potential_flavor}") from err


def iter_sort_by_len(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> Generator[str, None, None]:
    """Iterate strings sorted by length.

    Args:
        texts (Iterable[str]): Strings to sort.
        reverse (bool, optional): Sort in descending order (longest to shortest). Defaults to False.

    Yields:
        str: Strings sorted by length.
    """
    for text in sorted(texts, key=len, reverse=reverse):
        yield text


def sort_by_len(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> tuple[str, ...]:
    """Sort strings by length.

    Args:
        texts (Iterable[str]): Strings to sort.
        reverse (bool, optional): Sort in descending order (longest to shortest). Defaults to False.

    Returns:
        tuple[str, ...]: Strings sorted by length.
    """
    return tuple(iter_sort_by_len(texts, reverse=reverse))


def ord_to_cpoint(ordinal: int) -> str:
    """Character ordinal to character codepoint.

    The codepoint is always 8 characters long (zero-padded).

    Example:

    ```python
    ord_to_cpoint(97)
    # Output: '00000061'
    ```

    Args:
        ordinal (int): Character ordinal.

    Returns:
        str: Character codepoint.
    """
    return format(ordinal, "x").zfill(8)


def cpoint_to_ord(cpoint: str) -> int:
    """Character codepoint to character ordinal.

    Args:
        cpoint (str): Character codepoint.

    Returns:
        int: Character ordinal.
    """
    return int(cpoint, 16)


def char_to_cpoint(char: str) -> str:
    """Character to character codepoint.

    Example:

    ```python
    char_to_cpoint("a")
    # Output: '00000061'
    ```

    Args:
        char (str): Character.

    Returns:
        str: Character codepoint.
    """
    return ord_to_cpoint(ord(char))


def to_utf8(text):
    return text.encode("utf-8").decode("utf-8")


def to_nfc(text: str) -> str:
    """Normalize a Unicode string to NFC form C.

    Form C favors the use of a fully combined character.

    Example:

    ```python
    to_nfc("e\\u0301") == "é"
    # Output: True
    ```

    Args:
        text (str): String to normalize.

    Returns:
        str: Normalized string.
    """
    return unicodedata.normalize("NFC", text)


def iter_char_range(first_char: str, last_char: str) -> Generator[str, None, None]:
    """Iterate all characters within a range of characters (inclusive).

    Example:

    ```python
    char_range("a", "c")
    # Output: ('a', 'b', 'c')

    char_range("c", "a")
    # Output: ('c', 'b', 'a')
    ```

    Args:
        first_char (str): Starting (first) character.
        last_char (str): Ending (last) character.

    Yields:
        str: Characters within a range of characters.
    """
    first_ord = ord(first_char)
    last_ord = ord(last_char)
    if first_ord > last_ord:
        ord_range = range(first_ord, last_ord - 1, -1)
    else:
        ord_range = range(first_ord, last_ord + 1)
    for ordinal in ord_range:
        yield chr(ordinal)


def char_range(first_char: str, last_char: str) -> tuple[str, ...]:
    """Tuple of all characters within a range of characters (inclusive).

    Example:

    ```python
    char_range("a", "d")
    # Output: ('a', 'b', 'c', 'd')

    char_range("d", "a")
    # Output: ('d', 'c', 'b', 'a')
    ```

    Args:
        first_char (str): Starting (first) character.
        last_char (str): Ending (last) character.

    Returns:
        tuple[str, ...]: Characters within a range of characters.
    """
    return tuple(iter_char_range(first_char, last_char))


def mask_span(
    text: str,
    span: list[int] | tuple[int, int],
    mask: str | None = None,
) -> str:
    """Slice and mask a string using a single span.

    Args:
        text (str): String to slice.
        span (list[int] | tuple[int, int]): Domain of index positions (start, end) to mask.
        mask (str, optional): Mask to insert after slicing. Defaults to None.

    Returns:
        str: String with span replaced with the mask text.
    """
    if mask is None:
        # No mask
        return text[: span[0]] + text[span[1] :]
    else:
        # Has mask
        return text[: span[0]] + mask + text[span[1] :]


def mask_spans(
    text: str,
    spans: Iterable[list[int] | tuple[int, int]],
    masks: Iterable[str] | None = None,
) -> str:
    """Slice and mask a string using multiple spans.

    Todo: Add support for overlapping (and unordered?) spans.

    Args:
        text (str): String to slice.
        spans (Iterable[list[int] | tuple[int, int]]): Domains of index positions (x1, x2) to mask within the text.
        masks (Iterable[str], optional): Masks to insert when slicing. Defaults to None.

    Returns:
        str: String with all spans replaced with the mask text.
    """
    if masks is None:
        # No masks
        for span in reversed(spans):
            text = mask_span(text, span, mask=None)
    else:
        # Has masks
        for span, mask in zip(reversed(spans), reversed(masks)):
            text = mask_span(text, span, mask=mask)
    return text
