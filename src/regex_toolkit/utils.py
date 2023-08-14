import unicodedata
from collections.abc import Generator, Iterable
from functools import lru_cache
from typing import NoReturn

from regex_toolkit.enums import RegexFlavor

__all__ = [
    "validate_regex_flavor",
    "iter_sort_by_len",
    "sort_by_len",
    "ord_to_cpoint",
    "cpoint_to_ord",
    "char_to_cpoint",
    "to_utf8",
    "to_nfc",
    "iter_char_range",
    "char_range",
    "mask_span",
    "mask_spans",
]


@lru_cache(maxsize=2)
def validate_regex_flavor(flavor: int) -> None | NoReturn:
    """Validate a regex flavor.

    Args:
        flavor (int): Regex flavor (1 for RE, 2 for RE2).

    Raises:
        ValueError: Invalid regex flavor.
    """
    try:
        flavor = RegexFlavor(flavor)
    except ValueError:
        raise ValueError(f"Invalid regex flavor: {flavor}")


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

    Args:
        text (str): String to normalize.

    Returns:
        str: Normalized string.
    """
    return unicodedata.normalize("NFC", text)


def iter_char_range(first_char: str, last_char: str) -> Generator[str, None, None]:
    """Iterate all characters within a range of characters (inclusive).

    Args:
        first_char (str): Starting (first) character.
        last_char (str): Ending (last) character.

    Yields:
        str: Characters within a range of characters.
    """
    for i in range(ord(first_char), ord(last_char) + 1):
        yield chr(i)


def char_range(first_char: str, last_char: str) -> tuple[str, ...]:
    """Tuple of all characters within a range of characters (inclusive).

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
