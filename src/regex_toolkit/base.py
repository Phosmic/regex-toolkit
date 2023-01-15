__all__ = [
    "iter_sort_by_len",
    "sort_by_len",
    "ord_to_codepoint",
    "codepoint_to_ord",
    "char_to_codepoint",
    "char_as_exp",
    "char_as_exp2",
    "string_as_exp",
    "string_as_exp2",
    "strings_as_exp",
    "strings_as_exp2",
    "iter_char_range",
    "mask_span",
    "mask_spans",
    "to_utf8",
    "to_nfc",
]
import string
import unicodedata

from collections.abc import Iterable

_ALPHA_CHARS: set[str] = set(string.ascii_letters)
_DIGIT_CHARTS: set[str] = set(string.digits)
_SAFE_CHARS: set[str] = _ALPHA_CHARS.union(_DIGIT_CHARTS).union(set(string.whitespace))
_RE2_ESCAPABLE_CHARS: set[str] = set(string.punctuation)


def iter_sort_by_len(
    texts: Iterable[str],
    *,
    reverse: bool = False,
) -> Iterable[str]:
    """Iterate Texts Sorted by Length

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
    """Strings Sorted by Length

    Args:
        texts (Iterable[str]): Strings to sort.
        reverse (bool, optional): Sort in descending order (longest to shortest). Defaults to False.

    Returns:
        tuple[str]: Strings sorted by length.
    """
    return tuple(iter_sort_by_len(texts, reverse=reverse))


def ord_to_codepoint(ordinal: int) -> str:
    """Character Codepoint from Character Ordinal

    Args:
        ordinal (int): Character ordinal.

    Returns:
        str: Character codepoint.
    """
    return format(ordinal, "x").zfill(8)


def codepoint_to_ord(codepoint: str) -> int:
    """Character Ordinal from Character Codepoint

    Args:
        codepoint (str): Character codepoint.

    Returns:
        int: Character ordinal.
    """
    return int(codepoint, 16)


def char_to_codepoint(char: str) -> str:
    """Character Codepoint from Character

    Args:
        char (str): Character.

    Returns:
        str: Character codepoint.
    """
    return ord_to_codepoint(ord(char))


def char_as_exp(char: str) -> str:
    """Create a RE Regex Expression that Exactly Matches a Character

    Escape to avoid reserved character classes (i.e. \s, \S, \d, \D, \1, etc.).

    Args:
        char (str): Character to match.

    Returns:
        str: RE expression that exactly matches the original character.
    """
    if char in _SAFE_CHARS:
        # Safe as-is
        return char
    else:
        # Safe to escape with backslash
        return f"\\{char}"


def char_as_exp2(char: str) -> str:
    """Create a RE2 Regex Expression that Exactly Matches a Character

    Args:
        char (str): Character to match.

    Returns:
        str: RE2 expression that exactly matches the original character.
    """
    if char in _SAFE_CHARS:
        # Safe as-is
        return char
    elif char in _RE2_ESCAPABLE_CHARS:
        # Safe to escape with backslash
        return f"\\{char}"
    else:
        # Otherwise escape using the codepoint
        return "\\x{" + char_to_codepoint(char) + "}"


def string_as_exp(text: str) -> str:
    """Create a RE Regex Expression that Exactly Matches a String

    Args:
        text (str): String to match.

    Returns:
        str: RE expression that exactly matches the original string.
    """
    return r"".join(map(char_as_exp, text))


def string_as_exp2(text: str) -> str:
    """Create a RE2 Regex Expression that Exactly Matches a String

    Args:
        text (str): String to match.

    Returns:
        str: RE2 expression that exactly matches the original string.
    """
    return r"".join(map(char_as_exp2, text))


def strings_as_exp(texts: Iterable[str]) -> str:
    """Create a RE Regex expression that Exactly Matches Any One String

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
    """Create a RE2 Regex expression that Exactly Matches Any One String

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
    """Iterate All Characters within a Range of Codepoints (Inclusive)

    Args:
        first_codepoint (int): Starting (first) codepoint.
        last_codepoint (int): Ending (last) codepoint.

    Yields:
        str: Character from within a range of codepoints.
    """
    for i in range(ord(first_codepoint), ord(last_codepoint) + 1):
        yield chr(i)


def char_range(first_codepoint: int, last_codepoint: int) -> tuple[str, ...]:
    """Tuple of All Characters within a Range of Codepoints (Inclusive)

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
    """Slice and Mask a String using a Span

    Args:
        text (str): Text to slice.
        span (list[int] | tuple[int, int]): Domain of index positions (start, end) to mask.
        mask (str, optional): Mask to insert after slicing. Defaults to None.

    Returns:
        str: Text with span replaced with the mask text.
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
    """Slice and Mask a String using Multiple Spans

    Args:
        text (str): Text to slice.
        spans (Iterable[list[int] | tuple[int, int]]): Domains of index positions (x1, x2) to mask from the text.
        masks (Iterable[str], optional): Masks to insert when slicing. Defaults to None.

    Returns:
        str: Text with all spans replaced with the mask text.
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
    """Normalize a Unicode String to NFC Form C

    Form C favors the use of a fully combined character.

    Args:
        text (str): String to normalize.

    Returns:
        str: Normalized string.
    """
    return unicodedata.normalize("NFC", text)
