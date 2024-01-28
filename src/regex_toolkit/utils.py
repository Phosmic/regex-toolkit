from __future__ import annotations

import unicodedata
from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

import regex_toolkit.base
from regex_toolkit.enums import RegexFlavor

__all__ = [
    "char_range",
    "char_to_cpoint",
    "cpoint_to_ord",
    "iter_char_range",
    "iter_sort_by_len_and_alpha",
    "mask_span",
    "mask_spans",
    "ord_to_cpoint",
    "resolve_flavor",
    "sort_by_len_and_alpha",
    "to_nfc",
    "to_utf8",
]

SORT_BY_LEN_AND_ALPHA_KEY: Callable[[str], tuple[int, str]] = lambda x: (-len(x), x)


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


def iter_sort_by_len_and_alpha(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> Generator[str, None, None]:
    """Iterate strings sorted first by length (longest to shortest), then alphabetically.

    Example:

    ```python
    import regex_toolkit as rtk

    tuple(rtk.utils.iter_sort_by_len_and_alpha(["a", "aa", "aaa"]))
    # Output: ('aaa', 'aa', 'a')

    tuple(rtk.utils.iter_sort_by_len_and_alpha(["a", "b", "c"]))
    # Output: ('a', 'b', 'c')

    tuple(rtk.utils.iter_sort_by_len_and_alpha(["z", "a", "zz", "aa", "zzz", "aaa"]))
    # Output: ('aaa', 'zzz', 'aa', 'zz', 'a', 'z')
    ```

    Args:
        texts (Iterable[str]): Strings to sort.
        reverse (bool, optional): Sort in descending order (shortest to longest, then reverse alphabetically). Defaults to False.

    Yields:
        str: Strings sorted first by length, then alphabetically.
    """
    for text in sorted(texts, key=SORT_BY_LEN_AND_ALPHA_KEY, reverse=reverse):
        yield text


def sort_by_len_and_alpha(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> tuple[str, ...]:
    """Sort strings by first by length (longest to shortest), then alphabetically.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.utils.sort_by_len_and_alpha(["a", "aa", "aaa"])
    # Output: ('aaa', 'aa', 'a')

    rtk.utils.sort_by_len_and_alpha(["a", "b", "c"])
    # Output: ('a', 'b', 'c')

    rtk.utils.sort_by_len_and_alpha(["z", "a", "zz", "aa", "zzz", "aaa"])
    # Output: ('aaa', 'zzz', 'aa', 'zz', 'a', 'z')
    ```

    Args:
        texts (Iterable[str]): Strings to sort.
        reverse (bool, optional): Sort in descending order (shortest to longest, then reverse alphabetically). Defaults to False.

    Returns:
        tuple[str, ...]: Strings sorted first by length, then alphabetically.
    """
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

    rtk.cpoint_to_ord("1F436")
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

    rtk.to_nfc("e\\u0301")
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
    span: list[int] | tuple[int, int],
    mask: str | None = None,
) -> str:
    """Slice and mask a string using a single span.

    Example:

    ```python
    import regex_toolkit as rtk

    rtk.mask_span("This is a example", (10, 10), "insert ")
    # Output: 'This is a insert example'

    rtk.mask_span("This is a example", (5, 7), "replaces part of")
    # Output: 'This replaces part of a example'
    ```

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
