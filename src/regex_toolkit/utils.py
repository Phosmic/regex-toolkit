import unicodedata
from collections.abc import Generator, Iterable

__all__ = [
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
    """Character codepoint from character ordinal.

    Example:

        ```python
        # Output: '00000061'
        ord_to_cpoint(97)
        ```

    Args:
        ordinal (int): Character ordinal.

    Returns:
        str: Character codepoint.
    """
    return format(ordinal, "x").zfill(8)


def cpoint_to_ord(cpoint: str) -> int:
    """Character ordinal from character codepoint.

    Args:
        cpoint (str): Character codepoint.

    Returns:
        int: Character ordinal.
    """
    return int(cpoint, 16)


def char_to_cpoint(char: str) -> str:
    """Character codepoint from character.

    Example:

        ```python
        # Output: '00000061'
        char_to_cpoint("a")
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


def iter_char_range(first_cpoint: int, last_cpoint: int) -> Generator[str, None, None]:
    """Iterate all character within a range of codepoints (inclusive).

    Args:
        first_cpoint (int): Starting (first) codepoint.
        last_cpoint (int): Ending (last) codepoint.

    Yields:
        str: Character from within a range of codepoints.
    """
    for i in range(ord(first_cpoint), ord(last_cpoint) + 1):
        yield chr(i)


def char_range(first_cpoint: int, last_cpoint: int) -> tuple[str, ...]:
    """Tuple of all character within a range of codepoints (inclusive).

    Args:
        first_cpoint (int): Starting (first) codepoint.
        last_cpoint (int): Ending (last) codepoint.

    Returns:
        tuple[str, ...]: Characters within a range of codepoints.
    """
    return tuple(iter_char_range(first_cpoint, last_cpoint))


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

    Raises:
        ValueError: Invalid index positions for start and end.
    """
    if not 0 <= span[0] <= span[1] <= len(text):
        raise ValueError(f"Invalid index positions for start and end: {span}")
    if mask is None:
        # No mask
        return text[: span[0]] + text[span[1] :]
    else:
        # Use mask
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
        spans (Iterable[list[int] | tuple[int, int]]): Domains of index positions (x1, x2) to mask from the text.
        masks (Iterable[str], optional): Masks to insert when slicing. Defaults to None.

    Returns:
        str: String with all spans replaced with the mask text.

    Raises:
        ValueError: Invalid index positions for start and end.
    """
    try:
        if masks is None:
            # No masks
            for span in reversed(spans):
                text = mask_span(text, span, mask=None)
        else:
            # Has mask
            for span, mask in zip(reversed(spans), reversed(masks)):
                text = mask_span(text, span, mask=mask)
    except ValueError as err:
        raise err
    return text
