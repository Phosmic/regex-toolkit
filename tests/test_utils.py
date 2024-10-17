import unittest
from collections.abc import Generator, Iterable

import pytest

import regex_toolkit


def is_sorted_by_length_and_alphabetically(
    texts: Iterable[str],
    reverse: bool = False,
) -> bool:
    prev_len, prev_text = None, None
    for text in texts:
        if prev_len is None:
            prev_len, prev_text = len(text), text
        if reverse:
            if len(text) < prev_len:
                return False
            elif (len(text) == prev_len) and (text > prev_text):
                return False
        else:
            if len(text) > prev_len:
                return False
            elif (len(text) == prev_len) and (text < prev_text):
                return False
        prev_len, prev_text = len(text), text
    return True


SORT_BY_LEN_TEXTS = [
    "apple",
    "orange",
    "banana",
    "grape",
    "blue",
    "apricot",
    "cherry",
    "plum",
    "blueberry",
    "strawberry",
    "blackberry",
]
SORT_BY_LEN_TEXTS_BY_TYPE = {
    set: set(SORT_BY_LEN_TEXTS),
    frozenset: frozenset(SORT_BY_LEN_TEXTS),
    tuple: tuple(SORT_BY_LEN_TEXTS),
    list: list(SORT_BY_LEN_TEXTS),
    dict: dict.fromkeys(SORT_BY_LEN_TEXTS, None),
}


@pytest.mark.parametrize("try_type, typed_texts", SORT_BY_LEN_TEXTS_BY_TYPE.items())
@pytest.mark.parametrize("reverse", (False, True))
def test_iter_sort_by_len_and_alpha(try_type, typed_texts, reverse):
    expected_tuple = tuple(
        sorted(
            typed_texts,
            key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY,
            reverse=reverse,
        )
    )
    assert is_sorted_by_length_and_alphabetically(expected_tuple, reverse=reverse)

    actual = regex_toolkit.utils.iter_sort_by_len_and_alpha(
        typed_texts, reverse=reverse
    )
    actual_tuple = tuple(actual)
    assert isinstance(actual, Generator) and (actual_tuple == expected_tuple), {
        "try_type": try_type,
        "typed_texts": typed_texts,
        "reverse": reverse,
        "actual_tuple": actual_tuple,
        "expected_tuple": expected_tuple,
    }


@pytest.mark.parametrize("try_type, typed_texts", SORT_BY_LEN_TEXTS_BY_TYPE.items())
@pytest.mark.parametrize("reverse", (False, True))
def test_sort_by_len_and_alpha(try_type, typed_texts, reverse):
    expected = tuple(
        sorted(
            typed_texts,
            key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY,
            reverse=reverse,
        )
    )
    assert is_sorted_by_length_and_alphabetically(expected, reverse=reverse)

    actual = regex_toolkit.utils.sort_by_len_and_alpha(typed_texts, reverse=reverse)
    assert isinstance(actual, tuple) and (actual == expected), {
        "try_type": try_type,
        "typed_texts": typed_texts,
        "reverse": reverse,
        "actual": actual,
        "expected": expected,
    }


@pytest.mark.parametrize(
    "ordinal, zfill, expected",
    [
        # ASCII, numeric hexadecimal, various zfill values
        (97, None, "61"),
        (97, 0, "61"),
        (97, 1, "61"),
        (97, 2, "61"),
        (97, 3, "061"),
        (97, 4, "0061"),
        (97, 5, "00061"),
        (97, 6, "000061"),
        (97, 7, "0000061"),
        (97, 8, "00000061"),
        # Non-ASCII, alphanumeric hexadecimal, various zfill values
        (128054, None, "1F436"),
        (128054, 0, "1F436"),
        (128054, 1, "1F436"),
        (128054, 2, "1F436"),
        (128054, 3, "1F436"),
        (128054, 4, "1F436"),
        (128054, 5, "1F436"),
        (128054, 6, "01F436"),
        (128054, 7, "001F436"),
        (128054, 8, "0001F436"),
    ],
)
def test_ord_to_cpoint(ordinal, zfill, expected):
    actual = regex_toolkit.ord_to_cpoint(ordinal, zfill=zfill)
    assert actual == expected, {
        "ordinal": ordinal,
        "zfill": zfill,
        "actual": actual,
        "expected": expected,
    }


@pytest.mark.parametrize(
    "codepoint, expected",
    [
        # ASCII, numeric hexadecimal
        ("61", 97),
        ("0061", 97),
        ("00000061", 97),
        # Non-ASCII, alphanumeric hexadecimal, various hexadecimal capitalization
        ("1F436", 128054),
        ("1f436", 128054),
        ("0001F436", 128054),
        ("0001f436", 128054),
    ],
)
def test_cpoint_to_ord(codepoint, expected):
    actual = regex_toolkit.cpoint_to_ord(codepoint)
    assert actual == expected, {
        "codepoint": codepoint,
        "actual": actual,
        "expected": expected,
    }


@pytest.mark.parametrize(
    "char, zfill, expected",
    [
        # ASCII, numeric hexadecimal
        ("a", None, "61"),
        ("a", 0, "61"),
        ("a", 1, "61"),
        ("a", 2, "61"),
        ("a", 3, "061"),
        ("a", 4, "0061"),
        ("a", 5, "00061"),
        ("a", 6, "000061"),
        ("a", 7, "0000061"),
        ("a", 8, "00000061"),
        # Non-ASCII, alphanumeric hexadecimal
        ("🐶", None, "1F436"),
        ("🐶", 0, "1F436"),
        ("🐶", 1, "1F436"),
        ("🐶", 2, "1F436"),
        ("🐶", 3, "1F436"),
        ("🐶", 4, "1F436"),
        ("🐶", 5, "1F436"),
        ("🐶", 6, "01F436"),
        ("🐶", 7, "001F436"),
        ("🐶", 8, "0001F436"),
    ],
)
def test_char_to_cpoint(char, zfill, expected):
    actual = regex_toolkit.char_to_cpoint(char, zfill=zfill)
    assert actual == expected, {
        "char": char,
        "actual": actual,
        "expected": expected,
    }


ITER_CHAR_RANGE_CASES = [
    # Single char
    (("a", "a"), ("a",)),
    # Basic range
    (("a", "d"), ("a", "b", "c", "d")),
    # Reverse range
    (("d", "a"), ("d", "c", "b", "a")),
    # Single char (non-ASCII)
    (("🐶", "🐶"), ("🐶",)),
    # Basic range (non-ASCII)
    (("🐶", "🐺"), ("🐶", "🐷", "🐸", "🐹", "🐺")),
    # Reverse range (non-ASCII)
    (("🐺", "🐶"), ("🐺", "🐹", "🐸", "🐷", "🐶")),
]


@pytest.mark.parametrize("char_range, expected", ITER_CHAR_RANGE_CASES)
def test_char_range(char_range, expected):
    actual = regex_toolkit.char_range(*char_range)
    assert isinstance(actual, tuple)
    assert actual == expected, {
        "char_range": char_range,
        "actual": actual,
        "expected": expected,
    }


@pytest.mark.parametrize("char_range, expected", ITER_CHAR_RANGE_CASES)
def test_iter_char_range(char_range, expected):
    actual = regex_toolkit.iter_char_range(*char_range)
    assert isinstance(actual, Generator)
    actual_tuple = tuple(actual)
    assert actual_tuple == expected, {
        "char_range": char_range,
        "actual_tuple": actual_tuple,
        "expected": expected,
    }


@pytest.mark.parametrize(
    "text, expected",
    (
        # Empty string
        ("", ""),
        # Already NFC
        ("a", "a"),
        # Already NFC (non-ASCII)
        ("🐶🐾", "🐶🐾"),
        # Basic combining char (acute accent)
        ("a\u0301", "á"),
        # Multiple combining chars (diaeresis and acute accent)
        ("o\u0308\u0301", "ö́"),
    ),
)
def test_to_nfc(text, expected):
    actual = regex_toolkit.to_nfc(text)
    assert isinstance(actual, str)
    assert actual == expected, {
        "text": text,
        "actual": actual,
        "expected": expected,
    }


class TestMasking(unittest.TestCase):
    def setUp(self):
        self.text = "This is an example"

    def test_insert_word(self):
        indexes = (8, 8)
        for try_type, typed_indexes in ((tuple, indexes), (list, list(indexes))):
            with self.subTest(try_type=try_type, indexes=indexes):
                self.assertEqual(
                    regex_toolkit.mask_span(self.text, typed_indexes, "not "),
                    "This is not an example",
                )

    def test_replace_word(self):
        indexes = (5, 7)
        for try_type, typed_indexes in ((tuple, indexes), (list, list(indexes))):
            with self.subTest(try_type=try_type, indexes=indexes):
                self.assertEqual(
                    regex_toolkit.mask_span(self.text, typed_indexes, "isn't"),
                    "This isn't an example",
                )
