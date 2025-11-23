import unittest
from index.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def test_token_basic(self):
        t = Tokenizer()
        tokens = t.tokenize("Sustainability in Waste Management!!!")
        self.assertIn("sustainability", tokens)
        self.assertIn("waste", tokens)
        self.assertIn("management", tokens)
        self.assertNotIn("in", tokens)

    def test_case_normalization(self):
        t = Tokenizer()
        tokens = t.tokenize("HELLO World")
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)


if __name__ == "__main__":
    unittest.main()
