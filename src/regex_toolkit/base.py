__all__ = [
    "char_as_exp",
    "char_as_exp2",
    "char_range",
    "char_to_codepoint",
    "codepoint_to_ord",
    "iter_char_range",
    "iter_sort_by_len",
    "mask_span",
    "mask_spans",
    "ord_to_codepoint",
    "sort_by_len",
    "string_as_exp",
    "string_as_exp2",
    "strings_as_exp",
    "strings_as_exp2",
    "to_nfc",
    "to_utf8",
]
import unicodedata
from collections.abc import Iterable

from regex_toolkit.constants import RE2_ESCAPABLE_CHARS, SAFE_CHARS


def iter_sort_by_len(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> Iterable[str]:
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
        tuple[str]: Strings sorted by length.
    """
    return tuple(iter_sort_by_len(texts, reverse=reverse))


def ord_to_codepoint(ordinal: int) -> str:
    """Character codepoint from character ordinal.

    Args:
        ordinal (int): Character ordinal.

    Returns:
        str: Character codepoint.
    """
    return format(ordinal, "x").zfill(8)


def codepoint_to_ord(codepoint: str) -> int:
    """Character ordinal from character codepoint.

    Args:
        codepoint (str): Character codepoint.

    Returns:
        int: Character ordinal.
    """
    return int(codepoint, 16)


def char_to_codepoint(char: str) -> str:
    """Character codepoint from character.

    Args:
        char (str): Character.

    Returns:
        str: Character codepoint.
    """
    return ord_to_codepoint(ord(char))


def char_as_exp(char: str) -> str:
    """Create a RE regex expression that exactly matches a character.

    Escape to avoid reserved character classes (i.e. \\s, \\S, \\d, \\D, \\1, etc.).

    Args:
        char (str): Character to match.

    Returns:
        str: RE expression that exactly matches the original character.
    """
    if char in SAFE_CHARS:
        # Safe as-is
        return char
    else:
        # Safe to escape with backslash
        return f"\\{char}"


def char_as_exp2(char: str) -> str:
    """Create a RE2 regex expression that exactly matches a character.

    Args:
        char (str): Character to match.

    Returns:
        str: RE2 expression that exactly matches the original character.
    """
    if char in SAFE_CHARS:
        # Safe as-is
        return char
    elif char in RE2_ESCAPABLE_CHARS:
        # Safe to escape with backslash
        return f"\\{char}"
    else:
        # Otherwise escape using the codepoint
        return "\\x{" + char_to_codepoint(char) + "}"


def string_as_exp(text: str) -> str:
    """Create a RE regex expression that exactly matches a string.

    Args:
        text (str): String to match.

    Returns:
        str: RE expression that exactly matches the original string.
    """
    return r"".join(map(char_as_exp, text))


def string_as_exp2(text: str) -> str:
    """Create a RE2 regex expression that exactly matches a string.

    Args:
        text (str): String to match.

    Returns:
        str: RE2 expression that exactly matches the original string.
    """
    return r"".join(map(char_as_exp2, text))


def strings_as_exp(texts: Iterable[str]) -> str:
    """Create a RE regex expression that exactly matches any one string.

    Args:
        texts (Iterable[str]): Strings to match.

    Returns:
        str: RE expression that exactly matches any one of the original strings.
    """
    return r"|".join(
        map(
            string_as_exp,
            iter_sort_by_len(texts, reverse=True),
        )
    )


def strings_as_exp2(texts: Iterable[str]) -> str:
    """Create a RE2 regex expression that exactly matches any one string.

    Args:
        texts (Iterable[str]): Strings to match.

    Returns:
        str: RE2 expression that exactly matches any one of the original strings.
    """
    return r"|".join(
        map(
            string_as_exp2,
            iter_sort_by_len(texts, reverse=True),
        )
    )


def iter_char_range(first_codepoint: int, last_codepoint: int) -> Iterable[str]:
    """Iterate all character within a range of codepoints (inclusive).

    Args:
        first_codepoint (int): Starting (first) codepoint.
        last_codepoint (int): Ending (last) codepoint.

    Yields:
        str: Character from within a range of codepoints.
    """
    for i in range(ord(first_codepoint), ord(last_codepoint) + 1):
        yield chr(i)


def char_range(first_codepoint: int, last_codepoint: int) -> tuple[str, ...]:
    """Tuple of all character within a range of codepoints (inclusive).

    Args:
        first_codepoint (int): Starting (first) codepoint.
        last_codepoint (int): Ending (last) codepoint.

    Returns:
        tuple[str, ...]: Characters within a range of codepoints.
    """
    return tuple(iter_char_range(first_codepoint, last_codepoint))


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

    Args:
        text (str): String to slice.
        spans (Iterable[list[int] | tuple[int, int]]): Domains of index positions (x1, x2) to mask from the text.
        masks (Iterable[str], optional): Masks to insert when slicing. Defaults to None.

    Returns:
        str: String with all spans replaced with the mask text.
    """
    if masks is None:
        # No masks
        for span in reversed(spans):
            text = mask_span(text, span, mask=None)
    else:
        # Has mask
        for span, mask in zip(reversed(spans), reversed(masks)):
            text = mask_span(text, span, mask=mask)

    return text


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
