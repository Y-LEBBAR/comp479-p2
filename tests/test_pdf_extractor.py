import unittest
from index.pdf_extractor import extract_pdf_text


class TestPDFExtractor(unittest.TestCase):

    def test_extract_pdf_text(self):
        with open("tests/assets/479_test.pdf", "rb") as f:
            pdf_bytes = f.read()

        text = extract_pdf_text(pdf_bytes)
        self.assertTrue(isinstance(text, str))
        self.assertGreater(len(text.strip()), 0)


if __name__ == "__main__":
    unittest.main()
