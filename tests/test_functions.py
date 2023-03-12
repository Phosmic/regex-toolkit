import re
import unittest
from collections.abc import Iterable  # Generator
from itertools import combinations_with_replacement  # product

import regex_toolkit
from regex_toolkit.constants import ESCAPE_CHARS, SAFE_CHARS
from regex_toolkit.enums import RegexFlavor


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


class TestRegexFlavor(unittest.TestCase):
    def test_flavor(self):
        for flavor in RegexFlavor:
            with self.subTest(flavor=flavor):
                self.assertIsInstance(flavor, RegexFlavor)
                self.assertIsInstance(flavor.name, str)
                self.assertIsInstance(flavor.value, int)


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        self.texts = {
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
        }
        self.texts_by_type = (
            (set, self.texts),
            (frozenset, frozenset(self.texts)),
            (tuple, tuple(self.texts)),
            (list, list(self.texts)),
            (dict, dict.fromkeys(self.texts, None)),
        )

    def test_iter_sort_by_len(self):
        for try_type, typed_texts in self.texts_by_type:
            for reverse in (False, True):
                with self.subTest(
                    try_type=try_type, typed_texts=typed_texts, reverse=reverse
                ):
                    result = regex_toolkit.iter_sort_by_len(
                        typed_texts, reverse=reverse
                    )
                    self.assertIsInstance(result, Iterable)
                    result_tuple = tuple(result)
                    self.assertTrue(is_sorted_by_len(result_tuple, reverse=reverse))
                    self.assertEqual(len(result_tuple), len(typed_texts))

    def test_sort_by_len(self):
        for try_type, typed_texts in self.texts_by_type:
            for reverse in (False, True):
                with self.subTest(
                    try_type=try_type, typed_texts=typed_texts, reverse=reverse
                ):
                    result = regex_toolkit.sort_by_len(typed_texts, reverse=reverse)
                    self.assertIsInstance(result, tuple)
                    self.assertTrue(is_sorted_by_len(result, reverse=reverse))
                    self.assertEqual(len(result), len(typed_texts))

    def test_iter_char_range(self):
        result = regex_toolkit.iter_char_range("a", "z")
        self.assertIsInstance(result, Iterable)
        self.assertTupleEqual(tuple(result), tuple("abcdefghijklmnopqrstuvwxyz"))

    def test_char_range(self):
        self.assertEqual(
            regex_toolkit.char_range("a", "z"), tuple("abcdefghijklmnopqrstuvwxyz")
        )


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


class TestEscapeRE(unittest.TestCase):
    def test_only_safe(self):
        for char in SAFE_CHARS:
            with self.subTest(char=char):
                self.assertEqual(regex_toolkit.escape(char, RegexFlavor.RE), char)

    def test_only_escapable_chars(self):
        for char in ESCAPE_CHARS:
            with self.subTest(char=char):
                char_exp = regex_toolkit.escape(char, RegexFlavor.RE)
                self.assertEqual(char_exp, f"\\{char}")
                # Compile and test the expression.
                char_regex = re.compile(char_exp)
                self.assertTrue(char_regex.match(char))

    def test_only_unknown_chars(self):
        # TODO: Include additional characters to test.
        for char in "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅":
            with self.subTest(char=char):
                expression = regex_toolkit.escape(char, RegexFlavor.RE)
                self.assertEqual(expression, f"\\{char}")
                # Compile and match the expression.
                regex = re.compile(r"^" + expression + r"$")
                self.assertTrue(regex.match(char))


class TestEscapeRE2(unittest.TestCase):
    def test_only_safe(self):
        for char in SAFE_CHARS:
            with self.subTest(char=char):
                self.assertEqual(regex_toolkit.escape(char, RegexFlavor.RE), char)

    def test_only_escapable_chars(self):
        for char in ESCAPE_CHARS:
            with self.subTest(char=char):
                self.assertEqual(
                    regex_toolkit.escape(char, RegexFlavor.RE2),
                    f"\\{char}",
                )

    def test_only_unknown_chars(self):
        # TODO: Include additional characters to test.
        for char, expected_exp in (
            # Length 1
            ("🅰", r"\x{0001f170}"),
            ("🅱", r"\x{0001f171}"),
            ("🅾", r"\x{0001f17e}"),
            ("🅿", r"\x{0001f17f}"),
            ("🆎", r"\x{0001f18e}"),
            ("🆑", r"\x{0001f191}"),
            ("🆒", r"\x{0001f192}"),
            ("🆓", r"\x{0001f193}"),
            ("🆔", r"\x{0001f194}"),
            ("🆕", r"\x{0001f195}"),
            ("🆖", r"\x{0001f196}"),
            ("🆗", r"\x{0001f197}"),
            ("🆘", r"\x{0001f198}"),
            ("🆙", r"\x{0001f199}"),
            ("🆚", r"\x{0001f19a}"),
            ("🇦", r"\x{0001f1e6}"),
            ("🇧", r"\x{0001f1e7}"),
            ("🇨", r"\x{0001f1e8}"),
            ("🈁", r"\x{0001f201}"),
            ("🈂", r"\x{0001f202}"),
            ("🈚", r"\x{0001f21a}"),
            ("🈯", r"\x{0001f22f}"),
            ("🈲", r"\x{0001f232}"),
            ("🈳", r"\x{0001f233}"),
            ("🈴", r"\x{0001f234}"),
            ("🈵", r"\x{0001f235}"),
            ("🈶", r"\x{0001f236}"),
            ("🈷", r"\x{0001f237}"),
            ("🈸", r"\x{0001f238}"),
            ("🈹", r"\x{0001f239}"),
            ("🈺", r"\x{0001f23a}"),
            ("🉐", r"\x{0001f250}"),
            ("🉑", r"\x{0001f251}"),
            ("🌀", r"\x{0001f300}"),
            ("🌁", r"\x{0001f301}"),
            ("🌂", r"\x{0001f302}"),
            ("🌃", r"\x{0001f303}"),
            ("🌄", r"\x{0001f304}"),
            # Length 2
            ("🌅", r"\x{0001f305}"),
        ):
            with self.subTest(char=char, expected_exp=expected_exp):
                self.assertEqual(
                    regex_toolkit.escape(char, RegexFlavor.RE2),
                    expected_exp,
                )


class TestStringAsExpressionRE(unittest.TestCase):
    # TODO: Add tests for mix of characters.
    def test_safe(self):
        text = "".join(SAFE_CHARS)
        self.assertEqual(regex_toolkit.string_as_exp(text, RegexFlavor.RE), text)

    def test_escapable(self):
        text = "".join(ESCAPE_CHARS)
        self.assertEqual(
            regex_toolkit.string_as_exp(text, RegexFlavor.RE),
            "".join(f"\\{char}" for char in ESCAPE_CHARS),
        )

    def test_unknown(self):
        text = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"
        self.assertEqual(
            regex_toolkit.string_as_exp(text, RegexFlavor.RE),
            "".join(f"\\{char}" for char in text),
        )


class TestStringAsExpressionRE2(unittest.TestCase):
    # TODO: Add tests for mix of characters.
    def test_only_safe(self):
        text = "".join(SAFE_CHARS)
        self.assertEqual(
            regex_toolkit.string_as_exp(text, RegexFlavor.RE2),
            "".join(SAFE_CHARS),
        )

    def test_only_escapable_chars(self):
        text = "".join(ESCAPE_CHARS)
        self.assertEqual(
            regex_toolkit.string_as_exp(text, RegexFlavor.RE2),
            "".join(f"\\{char}" for char in ESCAPE_CHARS),
        )

    def test_only_unknown_chars(self):
        text = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"
        self.assertEqual(
            regex_toolkit.string_as_exp(text, RegexFlavor.RE2),
            r"".join(
                (
                    r"\x{0001f170}",
                    r"\x{0001f171}",
                    r"\x{0001f17e}",
                    r"\x{0001f17f}",
                    r"\x{0001f18e}",
                    r"\x{0001f191}",
                    r"\x{0001f192}",
                    r"\x{0001f193}",
                    r"\x{0001f194}",
                    r"\x{0001f195}",
                    r"\x{0001f196}",
                    r"\x{0001f197}",
                    r"\x{0001f198}",
                    r"\x{0001f199}",
                    r"\x{0001f19a}",
                    r"\x{0001f1e6}",
                    r"\x{0001f1e7}",
                    r"\x{0001f1e8}",
                    r"\x{0001f201}",
                    r"\x{0001f202}",
                    r"\x{0001f21a}",
                    r"\x{0001f22f}",
                    r"\x{0001f232}",
                    r"\x{0001f233}",
                    r"\x{0001f234}",
                    r"\x{0001f235}",
                    r"\x{0001f236}",
                    r"\x{0001f237}",
                    r"\x{0001f238}",
                    r"\x{0001f239}",
                    r"\x{0001f23a}",
                    r"\x{0001f250}",
                    r"\x{0001f251}",
                    r"\x{0001f300}",
                    r"\x{0001f301}",
                    r"\x{0001f302}",
                    r"\x{0001f303}",
                    r"\x{0001f304}",
                    # Length 2
                    r"\x{0001f305}",
                )
            ),
        )


class StringsAsExpressionRE(unittest.TestCase):
    def test_only_safe(self):
        # Unique combinations of SAFE_CHARS using various lengths (1-4).
        # elements = tuple(SAFE_CHARS)
        elements = SAFE_CHARS
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE),
                        "|".join(texts),
                    )

    def test_only_escapable_chars(self):
        # Unique combinations of ESCAPE_CHARS using various lengths (1-4).
        # elements = tuple(ESCAPE_CHARS)
        elements = ESCAPE_CHARS
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE),
                        "|".join(f"\\{text}" for text in texts),
                    )

    def test_reserved_only(self):
        # Unique combinations of reserved expressions using various lengths (1-4).
        elements = (
            r"\A",
            r"\b",
            r"\B",
            r"\d",
            r"\D",
            r"\s",
            r"\S",
            r"\w",
            r"\W",
            r"\Z",
            r"\1",
        )
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE),
                        "|".join(f"\\{text}" for text in texts),
                    )

    def test_unsafe_only(self):
        # TODO: Include text/chars such as punctuation, etc.
        # Unique combinations of UNSAFE_CHARS using various lengths (1-4).
        # elements = tuple(UNSAFE_CHARS)
        elements = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE),
                        "|".join(f"\\{text}" for text in texts),
                    )


######################
###################### # Multiple unsafe char
###################### self.assertEqual(
######################     regex_toolkit.strings_as_exp([".", "!", "?"], RegexFlavor.RE),
######################     "\\.|\\!|\\?",
###################### )
######################
###################### for texts, expected_exp in [
######################     (["🅰"], "\\🅰"),
######################     (["🅰", "🅱"], "\\🅰|\\🅱"),
######################     (["alpha", "beta"], "alpha|beta"),
######################     (["🅰lpha", "🅱eta"], "\\🅰lpha|\\🅱eta"),
######################     (["🅰lpha", "Beta"], "\\🅰lpha|Beta"),
###################### ]:
######################     self.assertEqual(
######################         regex_toolkit.strings_as_exp(texts, RegexFlavor.RE),
######################         expected_exp,
######################     )


class StringsAsExpressionRE2(unittest.TestCase):
    def test_only_safe(self):
        # Unique combinations of SAFE_CHARS using various lengths (1-4).
        # elements = tuple(SAFE_CHARS)
        elements = SAFE_CHARS
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE),
                        "|".join(texts),
                    )

    def test_only_escapable_chars(self):
        # Unique combinations of ESCAPE_CHARS using various lengths (1-4).
        # elements = tuple(ESCAPE_CHARS)
        elements = ESCAPE_CHARS
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2),
                        "|".join(f"\\{text}" for text in texts),
                    )

    def test_reserved_only(self):
        # Unique combinations of reserved expressions using various lengths (1-4).
        elements = (
            r"\A",
            r"\b",
            r"\B",
            r"\d",
            r"\D",
            r"\s",
            r"\S",
            r"\w",
            r"\W",
            r"\Z",
            r"\1",
        )
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2),
                        "|".join(f"\\{text}" for text in texts),
                    )

    def test_unsafe_only(self):
        # TODO: Include text/chars such as punctuation, etc.
        # Unique combinations of UNSAFE_CHARS using various lengths (1-4).
        # elements = tuple(UNSAFE_CHARS)
        elements_map = {
            # Length 1
            "🅰": r"\x{0001f170}",
            "🅱": r"\x{0001f171}",
            "🅾": r"\x{0001f17e}",
            "🅿": r"\x{0001f17f}",
            "🆎": r"\x{0001f18e}",
            "🆑": r"\x{0001f191}",
            "🆒": r"\x{0001f192}",
            "🆓": r"\x{0001f193}",
            "🆔": r"\x{0001f194}",
            "🆕": r"\x{0001f195}",
            "🆖": r"\x{0001f196}",
            "🆗": r"\x{0001f197}",
            "🆘": r"\x{0001f198}",
            "🆙": r"\x{0001f199}",
            "🆚": r"\x{0001f19a}",
            "🇦": r"\x{0001f1e6}",
            "🇧": r"\x{0001f1e7}",
            "🇨": r"\x{0001f1e8}",
            "🈁": r"\x{0001f201}",
            "🈂": r"\x{0001f202}",
            "🈚": r"\x{0001f21a}",
            "🈯": r"\x{0001f22f}",
            "🈲": r"\x{0001f232}",
            "🈳": r"\x{0001f233}",
            "🈴": r"\x{0001f234}",
            "🈵": r"\x{0001f235}",
            "🈶": r"\x{0001f236}",
            "🈷": r"\x{0001f237}",
            "🈸": r"\x{0001f238}",
            "🈹": r"\x{0001f239}",
            "🈺": r"\x{0001f23a}",
            "🉐": r"\x{0001f250}",
            "🉑": r"\x{0001f251}",
            "🌀": r"\x{0001f300}",
            "🌁": r"\x{0001f301}",
            "🌂": r"\x{0001f302}",
            "🌃": r"\x{0001f303}",
            "🌄": r"\x{0001f304}",
            # Length 2
            "🌅": r"\x{0001f305}",
        }
        elements = tuple(elements_map)
        for i in range(1, 5):
            for texts in combinations_with_replacement(elements, i):
                with self.subTest(texts=texts):
                    self.assertEqual(
                        regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2),
                        "|".join(elements_map[text] for text in texts),
                    )


##############################3        # Exact matches that equate to reserved spaces
##############################3        # E.g. Should match '\\' + 'd', not r'\d'
##############################3        for text in (r"\w", r"\W", r"\d", r"\D", r"\s", r"\S", r"\1"):
##############################3            texts = [text]
##############################3            with self.subTest(texts=texts):
##############################3                self.assertEqual(
##############################3                    regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2),
##############################3                    f"\\{text}",
##############################3                )
##############################3
##############################3        # Single whitespace char
##############################3        for texts in (["\n"], ["\v"], ["\t"], ["\r"], ["\f"], ["\v"]):
##############################3            with self.subTest(texts=texts):
##############################3                self.assertEqual(regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2), texts[0])
##############################3
##############################3        # Single unsafe char
##############################3        for texts, expected_exp in [
##############################3            (["."], "\\."),
##############################3            (["!"], "\\!"),
##############################3            (["?"], "\\?"),
##############################3        ]:
##############################3            with self.subTest(texts=texts, expected_exp=expected_exp):
##############################3                self.assertEqual(
##############################3                    regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2),
##############################3                    expected_exp,
##############################3                )
##############################3
##############################3        # Multiple unsafe char
##############################3        texts = [".", "!", "?"]
##############################3        self.assertEqual(regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2), "\\.|\\!|\\?")
##############################3
##############################3        for texts, expected_exp in [
##############################3            (["🅰"], "\\x{0001f170}"),
##############################3            (["🅰", "🅱"], "\\x{0001f170}|\\x{0001f171}"),
##############################3            (["alpha", "beta"], "alpha|beta"),
##############################3            (["🅰lpha", "🅱eta"], "\\x{0001f170}lpha|\\x{0001f171}eta"),
##############################3            (["🅰lpha", "Beta"], "\\x{0001f170}lpha|Beta"),
##############################3        ]:
##############################3            with self.subTest(texts=texts, expected_exp=expected_exp):
##############################3                self.assertEqual(
##############################3                    regex_toolkit.strings_as_exp(texts, RegexFlavor.RE2),
##############################3                    expected_exp,
##############################3                )

# TODO: Add tests for actually compiling the e.
