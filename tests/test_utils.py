import unittest
from crawler.utils import normalize_url, in_same_domain, is_pdf


class TestUtils(unittest.TestCase):

    def test_normalize_url(self):
        base = "https://spectrum.library.concordia.ca/page/"
        self.assertEqual(
            normalize_url(base, "../doc/test.pdf"),
            "https://spectrum.library.concordia.ca/doc/test.pdf"
        )

    def test_in_same_domain(self):
        domain = "https://spectrum.library.concordia.ca"
        self.assertTrue(in_same_domain("https://spectrum.library.concordia.ca/x", domain))
        self.assertFalse(in_same_domain("https://google.com", domain))

    def test_is_pdf(self):
        self.assertTrue(is_pdf("file.pdf"))
        self.assertTrue(is_pdf("file.PDF"))
        self.assertTrue(is_pdf("file.pdf?download=1"))
        self.assertFalse(is_pdf("file.html"))


if __name__ == "__main__":
    unittest.main()
