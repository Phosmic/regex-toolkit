import unittest
from collections.abc import Generator, Iterable

import regex_toolkit


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


class TestSortByLength(unittest.TestCase):
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
                    try_type=try_type,
                    typed_texts=typed_texts,
                    reverse=reverse,
                ):
                    result = regex_toolkit.iter_sort_by_len(
                        typed_texts,
                        reverse=reverse,
                    )
                    self.assertIsInstance(result, Generator)
                    result_tuple = tuple(result)
                    self.assertTrue(is_sorted_by_len(result_tuple, reverse=reverse))
                    self.assertEqual(
                        result_tuple,
                        tuple(sorted(typed_texts, key=len, reverse=reverse)),
                    )

    def test_sort_by_len(self):
        for try_type, typed_texts in self.texts_by_type:
            for reverse in (False, True):
                with self.subTest(
                    try_type=try_type,
                    typed_texts=typed_texts,
                    reverse=reverse,
                ):
                    result = regex_toolkit.sort_by_len(typed_texts, reverse=reverse)
                    self.assertIsInstance(result, tuple)
                    self.assertTrue(is_sorted_by_len(result, reverse=reverse))
                    self.assertEqual(
                        result,
                        tuple(sorted(typed_texts, key=len, reverse=reverse)),
                    )


class TestIterCharRange(unittest.TestCase):
    def test_iter_char_range(self):
        result = regex_toolkit.iter_char_range("a", "z")
        self.assertIsInstance(result, Generator)
        self.assertTupleEqual(
            tuple(result),
            tuple("abcdefghijklmnopqrstuvwxyz"),
        )

    def test_char_range(self):
        result = regex_toolkit.char_range("a", "z")
        self.assertIsInstance(result, tuple)
        self.assertTupleEqual(
            result,
            tuple("abcdefghijklmnopqrstuvwxyz"),
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
