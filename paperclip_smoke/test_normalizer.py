"""Behavior tests for label normalization."""

import unittest

from normalizer import normalize_label


class NormalizeLabelTests(unittest.TestCase):
    def test_mixed_case_and_whitespace(self):
        self.assertEqual(normalize_label("  HeLLo\t  WoRLD\n "), "hello world")

    def test_empty_input(self):
        self.assertEqual(normalize_label(""), "")

    def test_whitespace_only_input(self):
        self.assertEqual(normalize_label(" \t\r\n\u2003\u00a0 "), "")

    def test_unicode_text_and_whitespace(self):
        self.assertEqual(
            normalize_label("\u2003ÉCOLE\u00a0한글\tSTRAẞE\n"),
            "école 한글 straße",
        )


if __name__ == "__main__":
    unittest.main()
