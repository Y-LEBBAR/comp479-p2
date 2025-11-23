import unittest
from main import run_pipeline


class TestPipeline(unittest.TestCase):

    def test_pipeline_smoke(self):
        # Run pipeline with max_files=0 meaning no downloads
        run_pipeline(max_files=0, output_path="tests/tmp_index.json")

        # File should exist
        import os
        self.assertTrue(os.path.exists("tests/tmp_index.json"))

        os.remove("tests/tmp_index.json")


if __name__ == "__main__":
    unittest.main()
