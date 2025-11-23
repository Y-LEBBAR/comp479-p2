import unittest
import os
from index.indexer import Indexer
from index.storage import save_index_json, load_index_json


class TestStorage(unittest.TestCase):

    def test_save_and_load_json(self):
        idx = Indexer()
        idx.add_document(["waste", "management"], "http://example.com")

        save_index_json(idx, "tests/tmp_index.json")
        index, docs = load_index_json("tests/tmp_index.json")

        self.assertIn("waste", index)
        self.assertIn("0", docs or {})

        os.remove("tests/tmp_index.json")


if __name__ == "__main__":
    unittest.main()
