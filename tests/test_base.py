# import random
import re
from collections.abc import Iterable
from itertools import product
from unittest import mock

import pytest
import re2

import regex_toolkit
from regex_toolkit.constants import (
    ALWAYS_ESCAPE,
    ALWAYS_SAFE,
    RESERVED_EXPRESSIONS,
)
from regex_toolkit.enums import ALL_REGEX_FLAVORS, RegexFlavor

NON_ASCII_CHARS = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"


def _check_exp_match(exp: str, text: str, flavor: int, *, should_match: bool) -> bool:
    if flavor == 1:
        found = bool(re.fullmatch(exp, text))
        return found if should_match else not found
    if flavor == 2:
        found = bool(re2.fullmatch(exp, text))
        return found if should_match else not found
    raise ValueError(f"Invalid regex flavor: {flavor!r}")


def assert_exp_match(exp: str, text: str, flavor: int, *, should_match: bool) -> bool:
    assert _check_exp_match(exp, text, flavor, should_match=should_match), (
        f"RE{flavor} Pattern: {exp!r} should match {text!r}"
        if should_match
        else f"RE{flavor} Pattern: {exp!r} should not match {text!r}"
    )


def assert_exp_match_all(
    exp: str,
    texts: Iterable[str],
    flavor: int,
    *,
    should_match: bool,
) -> bool:
    for text in texts:
        assert_exp_match(exp, text, flavor, should_match=should_match)


# RE and RE2 - Escape


@pytest.mark.parametrize("char, expected", [(char, char) for char in ALWAYS_SAFE])
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_escape_and_escape2_safe(char, expected, flavor):
    actual = regex_toolkit.escape(char, flavor)
    assert actual == expected
    assert_exp_match(actual, char, flavor, should_match=True)


@pytest.mark.parametrize(
    "char, expected_exp", [(char, f"\\{char}") for char in ALWAYS_ESCAPE]
)
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_escape_and_escape2_escapable(char, expected_exp, flavor):
    actual = regex_toolkit.escape(char, flavor)
    assert actual == expected_exp
    assert_exp_match(actual, char, flavor, should_match=True)


@mock.patch("regex_toolkit.base._escape")
@mock.patch("regex_toolkit.base._escape2")
def test_escape_calls_expected_inner_func(mock__escape, mock__escape2):
    char = "a"

    flavor = RegexFlavor.RE
    mock__escape.return_value = regex_toolkit.escape(char, flavor)
    mock__escape2.return_value = regex_toolkit.escape(char, flavor)
    regex_toolkit.escape(char, flavor)
    assert mock__escape.called_once_with(char)
    assert mock__escape2.not_called()

    mock__escape.reset_mock()
    mock__escape2.reset_mock()

    flavor = RegexFlavor.RE2
    mock__escape.return_value = regex_toolkit.escape(char, flavor)
    mock__escape2.return_value = regex_toolkit.escape(char, flavor)
    regex_toolkit.escape(char, flavor)
    assert mock__escape.not_called()
    assert mock__escape2.called_once_with(char)


# RE - Escape


@pytest.mark.parametrize(
    "char, expected_exp",
    [(char, f"\\{char}") for char in NON_ASCII_CHARS],
)
def test_escape_unknown(char, expected_exp):
    actual = regex_toolkit.escape(char, RegexFlavor.RE)
    assert actual == expected_exp
    assert_exp_match(actual, char, RegexFlavor.RE, should_match=True)


# RE2 - Escape


@pytest.mark.parametrize(
    "char, expected",
    [
        (char, "\\x{" + format(ord(char), "x").zfill(8).removeprefix("0000") + "}")
        for char in NON_ASCII_CHARS
    ],
)
def test_escape2_unknown(char, expected):
    actual = regex_toolkit.escape(char, RegexFlavor.RE2)
    assert actual == expected
    assert_exp_match(actual, char, RegexFlavor.RE2, should_match=True)


def test_escape2_trimmed():
    text = "°"
    expected = "\\x{00b0}"
    actual = regex_toolkit.escape(text, RegexFlavor.RE2)
    assert actual == expected
    assert_exp_match(actual, text, RegexFlavor.RE2, should_match=True)


def test_escape2_untrimmed():
    text = "🅰"
    expected = "\\x{0001f170}"
    actual = regex_toolkit.escape(text, RegexFlavor.RE2)
    assert actual == expected
    assert_exp_match(actual, text, RegexFlavor.RE2, should_match=True)


# RE and RE2 - String as expression


@pytest.mark.parametrize("text, expected", [(text, text) for text in ALWAYS_SAFE])
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_string_as_exp_and_exp2_safe_individual_char(text, expected, flavor):
    actual = regex_toolkit.string_as_exp(text, flavor)
    assert actual == expected
    assert_exp_match(actual, text, flavor, should_match=True)


@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_string_as_exp_and_exp2_safe_joined_as_one(flavor):
    text = "".join(ALWAYS_SAFE)
    expected = "".join(ALWAYS_SAFE)
    actual = regex_toolkit.string_as_exp(text, flavor)
    assert actual == expected
    assert_exp_match(actual, text, flavor, should_match=True)


@pytest.mark.parametrize(
    "text, expected", [(char, f"\\{char}") for char in ALWAYS_ESCAPE]
)
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_string_as_exp_escapable_individual_char(text, expected, flavor):
    actual = regex_toolkit.string_as_exp(text, flavor)
    assert actual == expected
    assert_exp_match(actual, text, flavor, should_match=True)


@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_string_as_exp_escapable_joined_as_one(flavor):
    text = "".join(ALWAYS_ESCAPE)
    expected = "".join(f"\\{char}" for char in ALWAYS_ESCAPE)
    actual = regex_toolkit.string_as_exp(text, flavor)
    assert actual == expected
    assert_exp_match(actual, text, flavor, should_match=True)


@mock.patch("regex_toolkit.base._string_as_exp")
@mock.patch("regex_toolkit.base._string_as_exp2")
def test_string_as_exp_calls_expected_inner_func(
    mock__string_as_exp, mock__string_as_exp2
):
    text = "foo"

    flavor = RegexFlavor.RE
    mock__string_as_exp.return_value = regex_toolkit.string_as_exp(text, flavor)
    mock__string_as_exp2.return_value = regex_toolkit.string_as_exp(text, flavor)
    regex_toolkit.string_as_exp(text, flavor)
    assert mock__string_as_exp.called_once_with(text)
    assert mock__string_as_exp2.not_called()

    mock__string_as_exp.reset_mock()
    mock__string_as_exp2.reset_mock()

    flavor = RegexFlavor.RE2
    mock__string_as_exp.return_value = regex_toolkit.string_as_exp(text, flavor)
    mock__string_as_exp2.return_value = regex_toolkit.string_as_exp(text, flavor)
    regex_toolkit.string_as_exp(text, flavor)
    assert mock__string_as_exp.not_called()
    assert mock__string_as_exp2.called_once_with(text)


# RE - String as expression


@pytest.mark.parametrize(
    "text, expected",
    [(text, f"\\{text}") for text in NON_ASCII_CHARS],
)
def test_string_as_exp_unsafe_individual_char(text, expected):
    actual = regex_toolkit.string_as_exp(text, RegexFlavor.RE)
    assert actual == expected
    assert_exp_match(actual, text, RegexFlavor.RE, should_match=True)


def test_string_as_exp_unsafe_joined_as_one():
    text = "".join(NON_ASCII_CHARS)
    expected = "".join(f"\\{char}" for char in text)
    actual = regex_toolkit.string_as_exp(text, RegexFlavor.RE)
    assert actual == expected
    assert_exp_match(actual, text, RegexFlavor.RE, should_match=True)


# RE2 - String as expression


@pytest.mark.parametrize(
    "text, expected",
    [
        (char, "\\x{" + format(ord(char), "x").zfill(8).removeprefix("0000") + "}")
        for char in NON_ASCII_CHARS
    ],
)
def test_string_as_exp2_unknown_individual_char(text, expected):
    actual = regex_toolkit.string_as_exp(text, RegexFlavor.RE2)
    assert actual == expected
    assert_exp_match(actual, text, RegexFlavor.RE2, should_match=True)


def test_string_as_exp2_unknown_joined_as_one():
    text = "".join(NON_ASCII_CHARS)
    expected = "".join(
        "\\x{" + format(ord(char), "x").zfill(8).removeprefix("0000") + "}"
        for char in text
    )
    actual = regex_toolkit.string_as_exp(text, RegexFlavor.RE2)
    assert actual == expected
    assert_exp_match(actual, text, RegexFlavor.RE2, should_match=True)


# RE and RE2 - Strings as expression


@pytest.mark.parametrize(
    "texts, expected",
    [
        (
            texts,
            r"|".join(sorted(texts, key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY)),
        )
        for texts in product(ALWAYS_SAFE, repeat=2)
    ],
)
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_strings_as_exp_and_exp2_safe_of_various_lengths(texts, expected, flavor):
    actual = regex_toolkit.strings_as_exp(texts, flavor)
    assert actual == expected
    assert_exp_match_all(actual, texts, flavor, should_match=True)


@pytest.mark.parametrize(
    "texts, expected",
    [
        (
            texts,
            r"|".join(
                f"\\{text}"
                for text in sorted(
                    texts, key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY
                )
            ),
        )
        for texts in product(ALWAYS_ESCAPE, repeat=2)
    ],
)
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_strings_as_exp_and_exp2_escapable_of_various_lengths(texts, expected, flavor):
    actual = regex_toolkit.strings_as_exp(texts, flavor)
    assert actual == expected
    assert_exp_match_all(actual, texts, flavor, should_match=True)


@pytest.mark.parametrize(
    "texts, expected",
    [
        (
            texts,
            r"|".join(
                f"\\{text}"
                for text in sorted(
                    texts, key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY
                )
            ),
        )
        for texts in product(RESERVED_EXPRESSIONS, repeat=2)
    ],
)
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_strings_as_exp_and_exp2_reserved_of_various_lengths(texts, expected, flavor):
    actual = regex_toolkit.strings_as_exp(texts, flavor)
    assert actual == expected
    assert_exp_match_all(actual, texts, flavor, should_match=True)


@pytest.mark.parametrize(
    "texts, expected",
    [
        (
            texts,
            r"|".join(
                text if text in ALWAYS_SAFE else f"\\{text}"
                for text in sorted(
                    texts, key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY
                )
            ),
        )
        for texts in product(ALWAYS_SAFE | ALWAYS_ESCAPE, repeat=2)
    ],
)
@pytest.mark.parametrize("flavor", ALL_REGEX_FLAVORS)
def test_strings_as_exp_and_exp2_safe_and_escapable_of_various_lengths(
    texts, expected, flavor
):
    actual = regex_toolkit.strings_as_exp(texts, flavor)
    assert actual == expected
    assert_exp_match_all(actual, texts, flavor, should_match=True)


@mock.patch("regex_toolkit.base._strings_as_exp")
@mock.patch("regex_toolkit.base._strings_as_exp2")
def test_strings_as_exp_calls_expected_inner_func(
    mock__strings_as_exp, mock__strings_as_exp2
):
    texts = ["foo", "bar"]

    flavor = RegexFlavor.RE
    mock__strings_as_exp.return_value = regex_toolkit.strings_as_exp(texts, flavor)
    mock__strings_as_exp2.return_value = regex_toolkit.strings_as_exp(texts, flavor)
    regex_toolkit.strings_as_exp(texts, flavor)
    assert mock__strings_as_exp.called_once_with(texts)
    assert mock__strings_as_exp2.not_called()

    mock__strings_as_exp.reset_mock()
    mock__strings_as_exp2.reset_mock()

    flavor = RegexFlavor.RE2
    mock__strings_as_exp.return_value = regex_toolkit.strings_as_exp(texts, flavor)
    mock__strings_as_exp2.return_value = regex_toolkit.strings_as_exp(texts, flavor)
    regex_toolkit.strings_as_exp(texts, flavor)
    assert mock__strings_as_exp.not_called()
    assert mock__strings_as_exp2.called_once_with(texts)


# RE - Strings as expression


@pytest.mark.parametrize(
    "texts, expected",
    [
        (
            texts,
            r"|".join(
                f"\\{text}"
                for text in sorted(
                    texts, key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY
                )
            ),
        )
        for texts in product(NON_ASCII_CHARS, repeat=2)
    ],
)
def test_strings_as_exp_unsafe_of_various_lengths(texts, expected):
    actual = regex_toolkit.strings_as_exp(texts, RegexFlavor.RE)
    assert actual == expected
    assert_exp_match_all(actual, texts, RegexFlavor.RE, should_match=True)


# RE2 - Strings as expression


@pytest.mark.parametrize(
    "texts, expected",
    [
        (
            texts,
            r"|".join(
                "\\x{" + format(ord(char), "x").zfill(8).removeprefix("0000") + "}"
                for char in sorted(
                    texts, key=regex_toolkit.utils.SORT_BY_LEN_AND_ALPHA_KEY
                )
            ),
        )
        for texts in product(*NON_ASCII_CHARS, repeat=2)
    ],
)
def test_strings_as_exp2_unsafe_of_various_lengths(texts, expected):
    actual = regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2)
    assert actual == expected
    assert_exp_match_all(actual, texts, RegexFlavor.RE2, should_match=True)


# Make expression


@pytest.mark.parametrize(
    "chars, expected",
    (
        # 1 char does not make a range
        (["a"], "a"),
        # 2 chars should not make a range
        (["a", "b"], "ab"),
        # 3+ sequential chars make a range
        (["a", "b", "c"], "a-c"),
        # 3+ non-sequential chars should not make a range
        (["a", "c", "e"], "ace"),
        # 3+ sequential chars with extra out of range char
        (["a", "b", "c", "z"], "a-cz"),
        # Chars should always be ordered by ordinal
        (["b", "a"], "ab"),
        # Chars should always be ordered by ordinal
        (["e", "c", "a"], "ace"),
        # Chars should always be ordered by ordinal
        (["z", "c", "b", "a"], "a-cz"),
        # Duplicates should be removed
        (["d", "a", "b", "c", "a"], "a-d"),
    ),
)
def test_make_exp(chars, expected):
    assert regex_toolkit.make_exp(chars, RegexFlavor.RE) == expected
