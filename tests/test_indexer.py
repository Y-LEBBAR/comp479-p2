import unittest
from index.indexer import Indexer


class TestIndexer(unittest.TestCase):

    def test_add_document(self):
        idx = Indexer()
        tokens = ["waste", "waste", "management"]
        url = "http://example.com/doc.pdf"

        doc_id = idx.add_document(tokens, url)

        self.assertEqual(doc_id, 0)
        self.assertIn("waste", idx.index)
        self.assertEqual(idx.index["waste"][0], 2)
        self.assertEqual(idx.index["management"][0], 1)

        self.assertEqual(idx.docs[0]["url"], url)
        self.assertEqual(idx.docs[0]["length"], 3)


if __name__ == "__main__":
    unittest.main()
