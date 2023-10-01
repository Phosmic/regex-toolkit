import unittest
from collections.abc import Generator, Iterable
from unittest import mock

import pytest

import regex_toolkit
from regex_toolkit.enums import RegexFlavor


@pytest.mark.parametrize(
    "potential_flavor, expected",
    [
        (1, RegexFlavor.RE),
        (2, RegexFlavor.RE2),
        (RegexFlavor.RE, RegexFlavor.RE),
        (RegexFlavor.RE2, RegexFlavor.RE2),
        (RegexFlavor(1), RegexFlavor.RE),
        (RegexFlavor(2), RegexFlavor.RE2),
    ],
)
def test_resolve_flavor_with_valid(potential_flavor, expected):
    assert regex_toolkit.base.resolve_flavor(potential_flavor) == expected


@mock.patch("regex_toolkit.base.default_flavor", None)
def test_resolve_flavor_with_invalid_and_with_no_default_raises_value_error():
    with pytest.raises(ValueError, match=r"^Invalid regex flavor: None$"):
        regex_toolkit.base.resolve_flavor(None)


@pytest.mark.parametrize("potential_flavor", [None, 0, 3, "1", "2"])
@mock.patch("regex_toolkit.base.default_flavor", RegexFlavor.RE)
def test_resolve_flavor_falls_back_to_default(potential_flavor):
    regex_toolkit.base.resolve_flavor(potential_flavor) == RegexFlavor.RE


@pytest.mark.parametrize("potential_flavor", [None, 0, 3, "1", "2"])
@mock.patch("regex_toolkit.base.default_flavor", None)
def test_resolve_flavor_invalid_int_without_default_raises(potential_flavor):
    with pytest.raises(ValueError, match=r"^Invalid regex flavor: (None|'?\d'?)$"):
        regex_toolkit.base.resolve_flavor(potential_flavor)


@mock.patch("regex_toolkit.base.default_flavor", None)
def test_default_flavor_can_be_set():
    regex_toolkit.base.default_flavor = 2
    assert regex_toolkit.base.resolve_flavor(None) == RegexFlavor.RE2


def is_sorted_by_len(texts: Iterable[str], reverse: bool = False) -> bool:
    prev_len = None
    for text in texts:
        if prev_len is None:
            prev_len = len(text)
        if reverse:
            if len(text) > prev_len:
                return False
        else:
            if len(text) < prev_len:
                return False
        prev_len = len(text)
    return True


SORT_BY_LEN_TEXTS = [
    "apple",
    "orange",
    "banana",
    "grape",
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
def test_iter_sort_by_len(try_type, typed_texts, reverse):
    expected_tuple = tuple(sorted(typed_texts, key=len, reverse=reverse))
    assert is_sorted_by_len(expected_tuple, reverse=reverse)

    actual = regex_toolkit.iter_sort_by_len(typed_texts, reverse=reverse)
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
def test_sort_by_len(try_type, typed_texts, reverse):
    expected = tuple(sorted(typed_texts, key=len, reverse=reverse))
    assert is_sorted_by_len(expected, reverse=reverse)

    actual = regex_toolkit.sort_by_len(typed_texts, reverse=reverse)
    assert isinstance(actual, tuple) and (actual == expected), {
        "try_type": try_type,
        "typed_texts": typed_texts,
        "reverse": reverse,
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
    (("🐶", "🐺"), ("🐶", "🐷", "🐸", "🐹", "🐺")),
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
