import re
import unittest
from itertools import product

import pytest
import re2

import regex_toolkit
from regex_toolkit.constants import ALWAYS_ESCAPE, ALWAYS_SAFE
from regex_toolkit.enums import RegexFlavor


class TestEscapeRE(unittest.TestCase):
    def setUp(self):
        self._flavor = RegexFlavor.RE
        self._re_compile = re.compile

    def test_safe(self):
        for char in ALWAYS_SAFE:
            with self.subTest(char=char):
                expected_exp = char
                actual_exp = regex_toolkit.escape(char, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the character.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(char))

    def test_escapable(self):
        for char in ALWAYS_ESCAPE:
            with self.subTest(char=char):
                expected_exp = f"\\{char}"
                actual_exp = regex_toolkit.escape(char, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the character.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(char))

    def test_unknown(self):
        # TODO: Include additional characters to test.
        for char in "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅":
            with self.subTest(char=char):
                expected_exp = f"\\{char}"
                actual_exp = regex_toolkit.escape(char, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the character.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(char))


class TestEscapeRE2(unittest.TestCase):
    def setUp(self):
        self._flavor = RegexFlavor.RE2
        self._re_compile = re2.compile

    def test_safe(self):
        for char in ALWAYS_SAFE:
            with self.subTest(char=char):
                expected_exp = char
                actual_exp = regex_toolkit.escape(char, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the character.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(char))

    def test_escapable(self):
        for char in ALWAYS_ESCAPE:
            with self.subTest(char=char):
                expected_exp = f"\\{char}"
                actual_exp = regex_toolkit.escape(char, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the character.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(char))

    def test_trimmed(self):
        expected_exp = "\\x{00b0}"
        actual_exp = regex_toolkit.escape("°", self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the character.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match("°"))

    def test_untrimmed(self):
        expected_exp = "\\x{0001f170}"
        actual_exp = regex_toolkit.escape("🅰", self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the character.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match("🅰"))

    def test_unknown(self):
        # TODO: Include additional characters to test.
        # TODO: Cover chars that would be trimmed.
        # NOTE: Same as running: "\\x{" + format(ord("🌄"), "x").zfill(8).removeprefix("0000") + "}"
        for char, expected_exp in (
            # Length 1
            ("🅰", "\\x{0001f170}"),
            ("🅱", "\\x{0001f171}"),
            ("🅾", "\\x{0001f17e}"),
            ("🅿", "\\x{0001f17f}"),
            ("🆎", "\\x{0001f18e}"),
            ("🆑", "\\x{0001f191}"),
            ("🆒", "\\x{0001f192}"),
            ("🆓", "\\x{0001f193}"),
            ("🆔", "\\x{0001f194}"),
            ("🆕", "\\x{0001f195}"),
            ("🆖", "\\x{0001f196}"),
            ("🆗", "\\x{0001f197}"),
            ("🆘", "\\x{0001f198}"),
            ("🆙", "\\x{0001f199}"),
            ("🆚", "\\x{0001f19a}"),
            ("🇦", "\\x{0001f1e6}"),
            ("🇧", "\\x{0001f1e7}"),
            ("🇨", "\\x{0001f1e8}"),
            ("🈁", "\\x{0001f201}"),
            ("🈂", "\\x{0001f202}"),
            ("🈚", "\\x{0001f21a}"),
            ("🈯", "\\x{0001f22f}"),
            ("🈲", "\\x{0001f232}"),
            ("🈳", "\\x{0001f233}"),
            ("🈴", "\\x{0001f234}"),
            ("🈵", "\\x{0001f235}"),
            ("🈶", "\\x{0001f236}"),
            ("🈷", "\\x{0001f237}"),
            ("🈸", "\\x{0001f238}"),
            ("🈹", "\\x{0001f239}"),
            ("🈺", "\\x{0001f23a}"),
            ("🉐", "\\x{0001f250}"),
            ("🉑", "\\x{0001f251}"),
            ("🌀", "\\x{0001f300}"),
            ("🌁", "\\x{0001f301}"),
            ("🌂", "\\x{0001f302}"),
            ("🌃", "\\x{0001f303}"),
            ("🌄", "\\x{0001f304}"),
            # Length 2
            ("🌅", "\\x{0001f305}"),
        ):
            with self.subTest(char=char):
                actual_exp = regex_toolkit.escape(char, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the character.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(char))


class TestStringAsExpressionRE(unittest.TestCase):
    def setUp(self):
        self._flavor = RegexFlavor.RE
        self._re_compile = re.compile

    def test_safe_individual_char(self):
        # Single character.
        for char in ALWAYS_SAFE:
            with self.subTest(char=char):
                text = char
                expected_exp = char
                actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the string.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(text))

    # TODO: Add tests for mix of characters.
    def test_safe_joined_as_one(self):
        # All characters.
        text = "".join(ALWAYS_SAFE)
        expected_exp = text
        actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the string.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match(text))

    def test_escapable_individual_char(self):
        # Single character.
        for char in ALWAYS_ESCAPE:
            with self.subTest(char=char):
                text = char
                expected_exp = f"\\{char}"
                actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the string.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(text))

    def test_escapable_joined_as_one(self):
        # All characters.
        text = "".join(ALWAYS_ESCAPE)
        expected_exp = "".join(f"\\{char}" for char in ALWAYS_ESCAPE)
        actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the string.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match(text))

    def test_unsafe_joined_as_one(self):
        # All characters.
        text = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"
        expected_exp = "".join(f"\\{char}" for char in text)
        actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the string.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match(text))


class TestStringAsExpressionRE2(unittest.TestCase):
    def setUp(self):
        self._flavor = RegexFlavor.RE2
        self._re_compile = re2.compile

    # TODO: Add tests for mix of characters.
    def test_safe_individual_char(self):
        # Single character.
        for char in ALWAYS_SAFE:
            with self.subTest(char=char):
                text = char
                expected_exp = char
                actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the string.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(text))

    def test_safe_joined_as_one(self):
        # All characters.
        text = "".join(ALWAYS_SAFE)
        expected_exp = "".join(ALWAYS_SAFE)
        actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the string.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match(text))

    def test_escapable_individual_char(self):
        # Single character.
        for char in ALWAYS_ESCAPE:
            with self.subTest(char=char):
                text = char
                expected_exp = f"\\{char}"
                actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches the string.
                pattern = self._re_compile(actual_exp)
                self.assertTrue(pattern.match(text))

    def test_escapable_joined_as_one(self):
        # All characters.
        text = "".join(ALWAYS_ESCAPE)
        expected_exp = "".join(f"\\{char}" for char in ALWAYS_ESCAPE)
        actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the string.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match(text))

    def test_unknown_joined_as_one(self):
        # TODO: Include additional characters to test.
        # TODO: Cover chars that would be trimmed.
        text = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"
        expected_exp = r"".join(
            (
                "\\x{0001f170}",
                "\\x{0001f171}",
                "\\x{0001f17e}",
                "\\x{0001f17f}",
                "\\x{0001f18e}",
                "\\x{0001f191}",
                "\\x{0001f192}",
                "\\x{0001f193}",
                "\\x{0001f194}",
                "\\x{0001f195}",
                "\\x{0001f196}",
                "\\x{0001f197}",
                "\\x{0001f198}",
                "\\x{0001f199}",
                "\\x{0001f19a}",
                "\\x{0001f1e6}",
                "\\x{0001f1e7}",
                "\\x{0001f1e8}",
                "\\x{0001f201}",
                "\\x{0001f202}",
                "\\x{0001f21a}",
                "\\x{0001f22f}",
                "\\x{0001f232}",
                "\\x{0001f233}",
                "\\x{0001f234}",
                "\\x{0001f235}",
                "\\x{0001f236}",
                "\\x{0001f237}",
                "\\x{0001f238}",
                "\\x{0001f239}",
                "\\x{0001f23a}",
                "\\x{0001f250}",
                "\\x{0001f251}",
                "\\x{0001f300}",
                "\\x{0001f301}",
                "\\x{0001f302}",
                "\\x{0001f303}",
                "\\x{0001f304}",
                # Length 2
                "\\x{0001f305}",
            )
        )
        actual_exp = regex_toolkit.string_as_exp(text, self._flavor)
        self.assertEqual(actual_exp, expected_exp)
        # Ensure the expression compiles and matches the string.
        pattern = self._re_compile(actual_exp)
        self.assertTrue(pattern.match(text))


RESERVED_EXPRESSIONS = frozenset(
    {"\\A", "\\b", "\\B", "\\d", "\\D", "\\s", "\\S", "\\w", "\\W", "\\Z", "\\1"}
)


class StringsAsExpressionRE(unittest.TestCase):
    def setUp(self):
        self._flavor = RegexFlavor.RE
        self._re_compile = re.compile
        self._max_combo_length = 2

    def test_safe_of_various_lengths(self):
        # Unique combinations of `ALWAYS_SAFE` using various lengths.
        elements = ALWAYS_SAFE
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_escapable_of_various_lengths(self):
        # Unique combinations of `ALWAYS_ESCAPE` using various lengths.
        elements = ALWAYS_ESCAPE
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(f"\\{text}" for text in texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_reserved_of_various_lengths(self):
        # Unique combinations of reserved expressions using various lengths.
        # Exact matches that equate to reserved spaces
        # E.g. Should match '\\' + 'n', not r'\n'
        elements = RESERVED_EXPRESSIONS
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(f"\\{text}" for text in texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_unsafe_of_various_lengths(self):
        # TODO: Include text/chars such as punctuation, etc.
        # Unique combinations of `ALWAYS_SAFE` using various lengths.
        elements = "🅰🅱🅾🅿🆎🆑🆒🆓🆔🆕🆖🆗🆘🆙🆚🇦🇧🇨🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹🈺🉐🉑🌀🌁🌂🌃🌄🌅"
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(f"\\{text}" for text in texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_safe_and_escapable_of_various_lengths(self):
        # Unique combinations of `ALWAYS_SAFE` and `ALWAYS_ESCAPE` using various lengths.
        elements = ALWAYS_SAFE | ALWAYS_ESCAPE
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(
                    text if text in ALWAYS_SAFE else f"\\{text}" for text in texts
                )
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    # def test_actual_examples(self):
    #


######################
###################### # Multiple unsafe char
###################### self.assertEqual(
######################     regex_toolkit.strings_as_exp([".", "!", "?"], self._flavor),
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
######################         regex_toolkit.strings_as_exp(texts, self._flavor),
######################         expected_exp,
######################     )


class StringsAsExpressionRE2(unittest.TestCase):
    def setUp(self):
        self._flavor = RegexFlavor.RE2
        self._re_compile = re2.compile
        self._max_combo_length = 2

    def test_safe_of_variable_lengths(self):
        # Unique combinations of ALWAYS_SAFE using various lengths.
        elements = set(ALWAYS_SAFE)
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_escapable_of_variable_lengths(self):
        # Unique combinations of ALWAYS_ESCAPE using various lengths.
        elements = ALWAYS_ESCAPE
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(f"\\{text}" for text in texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_reserved_of_variable_lengths(self):
        # Unique combinations of reserved expressions using various lengths.
        # Exact matches that equate to reserved spaces
        # E.g. Should match '\\' + 'n', not r'\n'
        elements = RESERVED_EXPRESSIONS
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(f"\\{text}" for text in texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))

    def test_unsafe_of_variable_lengths(self):
        # TODO: Include text/chars such as punctuation, etc.
        # Unique combinations of ALWAYS_SAFE using various lengths.
        elements_map = {
            # Length 1
            "🅰": "\\x{0001f170}",
            "🅱": "\\x{0001f171}",
            "🅾": "\\x{0001f17e}",
            "🅿": "\\x{0001f17f}",
            "🆎": "\\x{0001f18e}",
            "🆑": "\\x{0001f191}",
            "🆒": "\\x{0001f192}",
            "🆓": "\\x{0001f193}",
            "🆔": "\\x{0001f194}",
            "🆕": "\\x{0001f195}",
            "🆖": "\\x{0001f196}",
            "🆗": "\\x{0001f197}",
            "🆘": "\\x{0001f198}",
            "🆙": "\\x{0001f199}",
            "🆚": "\\x{0001f19a}",
            "🇦": "\\x{0001f1e6}",
            "🇧": "\\x{0001f1e7}",
            "🇨": "\\x{0001f1e8}",
            "🈁": "\\x{0001f201}",
            "🈂": "\\x{0001f202}",
            "🈚": "\\x{0001f21a}",
            "🈯": "\\x{0001f22f}",
            "🈲": "\\x{0001f232}",
            "🈳": "\\x{0001f233}",
            "🈴": "\\x{0001f234}",
            "🈵": "\\x{0001f235}",
            "🈶": "\\x{0001f236}",
            "🈷": "\\x{0001f237}",
            "🈸": "\\x{0001f238}",
            "🈹": "\\x{0001f239}",
            "🈺": "\\x{0001f23a}",
            "🉐": "\\x{0001f250}",
            "🉑": "\\x{0001f251}",
            "🌀": "\\x{0001f300}",
            "🌁": "\\x{0001f301}",
            "🌂": "\\x{0001f302}",
            "🌃": "\\x{0001f303}",
            "🌄": "\\x{0001f304}",
            # Length 2
            "🌅": "\\x{0001f305}",
        }
        elements = tuple(elements_map)
        for texts in product(elements, repeat=self._max_combo_length):
            with self.subTest(texts=texts):
                expected_exp = r"|".join(elements_map[text] for text in texts)
                actual_exp = regex_toolkit.strings_as_exp(texts, self._flavor)
                self.assertEqual(actual_exp, expected_exp)
                # Ensure the expression compiles and matches each of the strings.
                pattern = self._re_compile(actual_exp)
                for text in texts:
                    with self.subTest("match pattern", text=text):
                        self.assertTrue(pattern.match(text))


##############################3        # Exact matches that equate to reserved spaces
##############################3        # E.g. Should match '\\' + 'n', not r'\n'
##############################3        for text in ("\\w", "\\W", "\\d", "\\D", "\\s", "\\S", "\\1"):
##############################3            texts = [text]
##############################3            with self.subTest(texts=texts):
##############################3                self.assertEqual(
##############################3                    regex_toolkit.strings_as_exp(texts, self._flavor),
##############################3                    f"\\{text}",
##############################3                )
##############################3
##############################3        # Single whitespace char
##############################3        for texts in (["\n"], ["\v"], ["\t"], ["\r"], ["\f"], ["\v"]):
##############################3            with self.subTest(texts=texts):
##############################3                self.assertEqual(regex_toolkit.strings_as_exp(texts, self._flavor), texts[0])
##############################3
##############################3        # Single unsafe char
##############################3        for texts, expected_exp in [
##############################3            (["."], "\\."),
##############################3            (["!"], "\\!"),
##############################3            (["?"], "\\?"),
##############################3        ]:
##############################3            with self.subTest(texts=texts, expected_exp=expected_exp):
##############################3                self.assertEqual(
##############################3                    regex_toolkit.strings_as_exp(texts, self._flavor),
##############################3                    expected_exp,
##############################3                )
##############################3
##############################3        # Multiple unsafe char
##############################3        texts = [".", "!", "?"]
##############################3        self.assertEqual(regex_toolkit.strings_as_exp(texts, self._flavor), "\\.|\\!|\\?")
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
##############################3                    regex_toolkit.strings_as_exp(texts, self._flavor),
##############################3                    expected_exp,
##############################3                )

# TODO: Add tests for actually compiling the e.


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
    assert regex_toolkit.make_exp(chars) == expected
