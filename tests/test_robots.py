import unittest
from crawler.robots import RobotsTxt

class TestRobots(unittest.TestCase):

    def test_robots_fetch(self):
        r = RobotsTxt("https://spectrum.library.concordia.ca/")
        self.assertTrue(r.fetched)

    def test_allowed_default(self):
        r = RobotsTxt("https://example.com/")
        self.assertTrue(r.is_allowed("https://example.com/page"))

    def test_disallow(self):
        # Mock manual insertion of rule
        r = RobotsTxt("https://example.com/")
        r.disallowed_paths.append("/private")
        self.assertFalse(r.is_allowed("https://example.com/private/stuff"))

    def test_allow_over_disallow(self):
        r = RobotsTxt("https://example.com/")
        r.disallowed_paths.append("/data")
        r.allowed_paths.append("/data/public")
        self.assertTrue(r.is_allowed("https://example.com/data/public/abc"))


if __name__ == "__main__":
    unittest.main()
