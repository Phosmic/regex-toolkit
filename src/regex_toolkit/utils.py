from __future__ import annotations

import unicodedata
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import (
        Callable,
        Generator,
        Iterable,
        Sequence,
    )


__all__ = [
    "char_range",
    "char_to_cpoint",
    "cpoint_to_ord",
    "iter_char_range",
    "iter_sort_by_len_and_alpha",
    "mask_span",
    "mask_spans",
    "ord_to_cpoint",
    "sort_by_len_and_alpha",
    "to_nfc",
    "to_utf8",
]

SORT_BY_LEN_AND_ALPHA_KEY: Callable[[str], tuple[int, str]] = lambda x: (-len(x), x)


def iter_sort_by_len_and_alpha(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> Generator[str, None, None]:
    for text in sorted(texts, key=SORT_BY_LEN_AND_ALPHA_KEY, reverse=reverse):
        yield text


def sort_by_len_and_alpha(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> tuple[str, ...]:
    return tuple(iter_sort_by_len_and_alpha(texts, reverse=reverse))


def ord_to_cpoint(ordinal: int, *, zfill: int | None = 8) -> str:
    """Character ordinal to character codepoint.

    Produces a hexadecimal (`[0-9A-F]`) representation of the ordinal.
    The default zero-padding is 8 characters, which is the maximum amount of characters in a codepoint.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.ord_to_cpoint(128054)
    # Output: '0001F436'

    # Disable zero-padding by setting `zfill` to `0` or `None`.
    rtk.ord_to_cpoint(128054, zfill=0)
    # Output: '1F436'
    ```

    Args:
        ordinal (int): Character ordinal.
        zfill (int | None, optional): Amount of characters to zero-pad the codepoint to. Defaults to 8.

    Returns:
        str: Character codepoint.
    """
    nonpadded_cpoint = format(ordinal, "x").upper()
    return nonpadded_cpoint.zfill(zfill) if zfill else nonpadded_cpoint


def cpoint_to_ord(cpoint: str) -> int:
    """Character codepoint to character ordinal.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.cpoint_to_ord("0001F436")
    # Output: 128054

    rtk.cpoint_to_ord("1f436")
    # Output: 128054
    ```

    Args:
        cpoint (str): Character codepoint.

    Returns:
        int: Character ordinal.
    """
    return int(cpoint, 16)


def char_to_cpoint(char: str, *, zfill: int | None = 8) -> str:
    """Character to character codepoint.

    Produces a hexadecimal (`[0-9A-F]`) representation of the character.
    The default zero-padding is 8 characters, which is the maximum amount of characters in a codepoint.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.char_to_cpoint("🐶")
    # Output: '0001F436'

    # Disable zero-padding by setting `zfill` to `0` or `None`.
    rtk.char_to_cpoint("🐶", zfill=0)
    # Output: '1F436'
    ```

    Args:
        char (str): Character.
        zfill (int | None, optional): Amount of characters to zero-pad the codepoint to. Defaults to 8.

    Returns:
        str: Character codepoint.
    """
    return ord_to_cpoint(ord(char), zfill=zfill)


def to_utf8(text):
    return text.encode("utf-8").decode("utf-8")


def to_nfc(text: str) -> str:
    """Normalize a Unicode string to NFC form C.

    Form C favors the use of a fully combined character.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.to_nfc("e\u0301")
    # Output: 'é'
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
    import regex_toolkit as rtk

    tuple(rtk.iter_char_range("a", "c"))
    # Output: ('a', 'b', 'c')

    tuple(rtk.iter_char_range("c", "a"))
    # Output: ('c', 'b', 'a')

    tuple(rtk.iter_char_range("🐶", "🐺"))
    # Output: ("🐶", "🐷", "🐸", "🐹", "🐺")
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
    """Get all characters within a range of characters (inclusive).

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.char_range("a", "d")
    # Output: ('a', 'b', 'c', 'd')

    rtk.char_range("d", "a")
    # Output: ('d', 'c', 'b', 'a')

    rtk.char_range("🐶", "🐺")
    # Output: ("🐶", "🐷", "🐸", "🐹", "🐺")
    ```

    Args:
        first_char (str): First character (inclusive).
        last_char (str): Last character (inclusive).

    Returns:
        tuple[str, ...]: Characters within a range of characters.
    """
    return tuple(iter_char_range(first_char, last_char))


def mask_span(
    text: str,
    span: Sequence[int],
    mask: str | None = None,
) -> str:
    """Slice and mask a string using a single span.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.mask_span("example", (0, 2))
    # Output: 'ample'

    rtk.mask_span("This is a example", (10, 10), "insert ")
    # Output: 'This is a insert example'

    rtk.mask_span("This is a example", (5, 7), "replaces part of")
    # Output: 'This replaces part of a example'
    ```

    Todo:

    * Consider alternate behavior for a span that is out of bounds.

    Args:
        text (str): String to slice.
        span (Sequence[int]): Span to slice (start is inclusive, end is exclusive).
        mask (str, optional): String to replace the span with. Defaults to None.

    Returns:
        str: String with span replaced with the mask text.
    """
    if mask is None:
        return text[: span[0]] + text[span[1] :]
    else:
        return text[: span[0]] + mask + text[span[1] :]


def mask_spans(
    text: str,
    spans: Sequence[Sequence[int]],
    masks: Sequence[str] | None = None,
) -> str:
    """Slice and mask a string using multiple spans.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.mask_spans(
        text="This is a example",
        masks=["replaces part of", "insert "],
        spans=[(5, 7), (10, 10)],
    )
    # Output: 'This replaces part of a insert example'
    ```

    Todo:

    * Consider alternate behavior for spans that overlap.
    * Consider alternate behavior for spans that are out of order.
    * Consider alternate behavior for spans that are out of bounds.

    Args:
        text (str): String to slice.
        spans (Sequence[Sequence[int]]): Spans to slice (start is inclusive, end is exclusive).
        masks (Sequence[str], optional): Strings to replace the spans with. Defaults to None.

    Returns:
        str: String with all spans replaced with the mask text.
    """
    for idx in range(len(spans) - 1, -1, -1):
        text = mask_span(text, spans[idx], mask=masks[idx] if masks else None)
    return text
