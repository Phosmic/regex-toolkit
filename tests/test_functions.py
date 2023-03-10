import unittest
from collections.abc import Iterable
from itertools import product

import regex_toolkit


class TestStringMethods(unittest.TestCase):
    def test_iter_sort_by_len(self):
        # Words used during test
        texts = {
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

        # Run test using different iterable types
        for try_type, texts_as_try_type in {
            set: texts,
            Iterable: iter(texts),
            tuple: tuple(texts),
            list: list(texts),
            dict: dict.fromkeys(texts, None),
        }.items():
            # Not reversed (shortest to longest)
            result = regex_toolkit.iter_sort_by_len(texts_as_try_type, reverse=False)

            # Returns a iterable (allows for duplicate entries)
            self.assertIsInstance(result, Iterable)

            # Result should have a equal number of texts
            self.assertEqual(len(texts), len(tuple(result)))

            prev_len = None
            for text in result:
                if prev_len is not None:
                    self.assertGreaterEqual(len(text), prev_len)

                prev_len = len(text)

        # Run test using different iterable types
        for try_type, texts_as_try_type in {
            set: texts,
            Iterable: iter(texts),
            tuple: tuple(texts),
            list: list(texts),
        }.items():
            # Not reversed (longest to shortest)
            result = regex_toolkit.iter_sort_by_len(texts_as_try_type, reverse=True)

            # Returns a iterable (allows for duplicate entries)
            self.assertIsInstance(result, Iterable)

            # Result should have a equal number of texts
            self.assertEqual(len(texts), len(tuple(result)))

            prev_len = None
            for text in result:
                if prev_len is not None:
                    self.assertLessEqual(len(text), prev_len)

                prev_len = len(text)

    def test_sort_by_len(self):
        # Words used during test
        texts = {
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

        # Run test using different iterable types
        for try_type, texts_as_try_type in {
            set: texts,
            Iterable: iter(texts),
            tuple: tuple(texts),
            list: list(texts),
            dict: dict.fromkeys(texts, None),
        }.items():
            # Not reversed (shortest to longest)
            result = regex_toolkit.sort_by_len(texts_as_try_type, reverse=False)

            # Returns a tuple (allows for duplicate entries)
            self.assertIsInstance(result, tuple)

            # Result should have a equal number of texts
            self.assertEqual(len(texts), len(result))

            prev_len = None
            for text in result:
                if prev_len is not None:
                    self.assertGreaterEqual(len(text), prev_len)

                prev_len = len(text)

        # Run test using different iterable types
        for try_type, texts_as_try_type in {
            set: texts,
            Iterable: iter(texts),
            tuple: tuple(texts),
            list: list(texts),
        }.items():
            # Not reversed (longest to shortest)
            result = regex_toolkit.sort_by_len(texts_as_try_type, reverse=True)

            # Returns a tuple (allows for duplicate entries)
            self.assertIsInstance(result, tuple)

            # Result should have a equal number of texts
            self.assertEqual(len(texts), len(result))

            prev_len = None
            for text in result:
                if prev_len is not None:
                    self.assertLessEqual(len(text), prev_len)

                prev_len = len(text)

    def test_string_as_exp_safe_chars(self):
        text = "".join(regex_toolkit.constants.SAFE_CHARS)
        actual_exp = regex_toolkit.string_as_exp(text)
        expected_exp = "".join(regex_toolkit.constants.SAFE_CHARS)
        self.assertEqual(actual_exp, expected_exp)

    def test_string_as_exp2_escapable_chars(self):
        text = "".join(regex_toolkit.constants.RE2_ESCAPABLE_CHARS)
        actual_exp = regex_toolkit.string_as_exp2(text)
        expected_exp = "\\" + "\\".join(regex_toolkit.constants.RE2_ESCAPABLE_CHARS)
        self.assertEqual(actual_exp, expected_exp)

    def test_string_as_exp_safe_chars(self):
        text = "".join(regex_toolkit.constants.SAFE_CHARS)
        actual_exp = regex_toolkit.string_as_exp(text)
        expected_exp = "".join(regex_toolkit.constants.SAFE_CHARS)
        self.assertEqual(actual_exp, expected_exp)

    def test_string_as_exp2_escapable_chars(self):
        text = "".join(regex_toolkit.constants.RE2_ESCAPABLE_CHARS)
        actual_exp = regex_toolkit.string_as_exp2(text)
        expected_exp = "\\" + "\\".join(regex_toolkit.constants.RE2_ESCAPABLE_CHARS)
        self.assertEqual(actual_exp, expected_exp)

    def test_iter_char_range(self):
        result = regex_toolkit.iter_char_range("a", "z")

        # Returns a iterable (no duplicate entries)
        self.assertIsInstance(result, Iterable)

        # Validate output
        actual_char_range = tuple(result)
        excpected_char_range = tuple("abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(actual_char_range, excpected_char_range)

    def test_char_range(self):
        result = regex_toolkit.char_range("a", "z")

        # Returns a tuple (no duplicate entries)
        self.assertIsInstance(result, tuple)

        # Validate output
        actual_char_range = result
        excpected_char_range = tuple("abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(actual_char_range, excpected_char_range)

    def test_mask_span(self):
        text = "This is an example"

        # Run test using different acceptable sequence types
        indexes = (8, 8)
        for try_type, indexes_as_try_type in {
            tuple: indexes,
            list: list(indexes),
        }.items():
            actual_text = regex_toolkit.mask_span(text, indexes_as_try_type, "not ")
            expected_text = "This is not an example"
            self.assertEqual(actual_text, expected_text)

        # Run test using different acceptable sequence types
        indexes = (5, 7)
        for try_type, indexes_as_try_type in {
            tuple: indexes,
            list: list(indexes),
        }.items():
            actual_text = regex_toolkit.mask_span(text, indexes_as_try_type, "isn't")
            expected_text = "This isn't an example"
            self.assertEqual(actual_text, expected_text)

    def test_char_as_exp(self):
        for char, expected_exp in (
            ("s", "s"),
            ("d", "d"),
            ("\n", "\n"),
            (".", "\\."),
            ("!", "\\!"),
            ("?", "\\?"),
            ("🅰", "\\🅰"),
        ):
            actual_exp = regex_toolkit.char_as_exp(char)
            self.assertEqual(actual_exp, expected_exp)

    def test_char_as_exp2(self):
        for char, expected_exp in (
            ("s", "s"),
            ("d", "d"),
            ("\n", "\n"),
            (".", "\\."),
            ("!", "\\!"),
            ("?", "\\?"),
            ("🅰", r"\x{0001f170}"),
        ):
            actual_exp = regex_toolkit.char_as_exp2(char)
            self.assertEqual(actual_exp, expected_exp)

    def test_strings_as_exp(self):
        # Alphanumeric single char and multi-char combos
        for i in range(4):
            for char_tuple in product(i * ["a", "b", "0", "1"]):
                actual_exp = regex_toolkit.strings_as_exp(char_tuple)
                expected_exp = "|".join(char_tuple)
                self.assertEqual(actual_exp, expected_exp)

        # Exact matches that equate to reserved spaces
        # E.g. Should match '\\' + 'd', not r'\d'
        for text in {r"\w", r"\W", r"\d", r"\D", r"\s", r"\S", r"\1"}:
            actual_exp = regex_toolkit.strings_as_exp([text])
            expected_exp = f"\\{text}"
            self.assertEqual(actual_exp, expected_exp)

        # Single whitespace char
        for text in {"\n", "\v", "\t", "\r", "\f", "\v"}:
            actual_exp = regex_toolkit.strings_as_exp([text])
            expected_exp = text
            self.assertEqual(actual_exp, expected_exp)

        # Single unsafe char
        for texts, expected_exp in [
            (["."], "\\."),
            (["!"], "\\!"),
            (["?"], "\\?"),
        ]:
            actual_exp = regex_toolkit.strings_as_exp(texts)
            self.assertEqual(actual_exp, expected_exp)

        # Multiple unsafe char
        texts = [".", "!", "?"]
        expected_exp = "\\.|\\!|\\?"
        actual_exp = regex_toolkit.strings_as_exp(texts)
        self.assertEqual(actual_exp, expected_exp)

        for texts, expected_exp in [
            (["🅰"], "\\🅰"),
            (["🅰", "🅱"], "\\🅰|\\🅱"),
            (["alpha", "beta"], "alpha|beta"),
            (["🅰lpha", "🅱eta"], "\\🅰lpha|\\🅱eta"),
            (["🅰lpha", "Beta"], "\\🅰lpha|Beta"),
        ]:
            actual_exp = regex_toolkit.strings_as_exp(texts)
            self.assertEqual(actual_exp, expected_exp)

    def test_strings_as_exp2(self):
        # Alphanumeric single char and multi-char combos
        for i in range(4):
            for char_tuple in product(i * ["a", "b", "0", "1"]):
                actual_exp = regex_toolkit.strings_as_exp2(char_tuple)
                expected_exp = "|".join(char_tuple)
                self.assertEqual(actual_exp, expected_exp)

        # Exact matches that equate to reserved spaces
        # E.g. Should match '\\' + 'd', not r'\d'
        for text in {r"\w", r"\W", r"\d", r"\D", r"\s", r"\S", r"\1"}:
            actual_exp = regex_toolkit.strings_as_exp2([text])
            expected_exp = f"\\{text}"
            self.assertEqual(actual_exp, expected_exp)

        # Single whitespace char
        for text in {"\n", "\v", "\t", "\r", "\f", "\v"}:
            actual_exp = regex_toolkit.strings_as_exp2([text])
            expected_exp = text
            self.assertEqual(actual_exp, expected_exp)

        # Single unsafe char
        for texts, expected_exp in [
            (["."], "\\."),
            (["!"], "\\!"),
            (["?"], "\\?"),
        ]:
            actual_exp = regex_toolkit.strings_as_exp2(texts)
            self.assertEqual(actual_exp, expected_exp)

        # Multiple unsafe char
        texts = [".", "!", "?"]
        expected_exp = "\\.|\\!|\\?"
        actual_exp = regex_toolkit.strings_as_exp2(texts)
        self.assertEqual(actual_exp, expected_exp)

        for texts, expected_exp in [
            (["🅰"], "\\x{0001f170}"),
            (["🅰", "🅱"], "\\x{0001f170}|\\x{0001f171}"),
            (["alpha", "beta"], "alpha|beta"),
            (["🅰lpha", "🅱eta"], "\\x{0001f170}lpha|\\x{0001f171}eta"),
            (["🅰lpha", "Beta"], "\\x{0001f170}lpha|Beta"),
        ]:
            actual_exp = regex_toolkit.strings_as_exp2(texts)
            self.assertEqual(actual_exp, expected_exp)
