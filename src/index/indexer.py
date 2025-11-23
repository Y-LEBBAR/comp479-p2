from collections import defaultdict, Counter


class Indexer:
    """
    Builds and maintains an inverted index for the Spectrum documents.
    """

    def __init__(self):
        # token -> { doc_id: tf }
        self.index = defaultdict(dict)

        # doc_id -> metadata
        self.docs = {}

        # internal document counter
        self.next_doc_id = 0

    def add_document(self, tokens: list[str], url: str):
        """
        Add a new document to the inverted index.

        Steps:
            - assign doc_id
            - compute term frequencies
            - update index
            - store metadata
        """

        doc_id = self.next_doc_id
        self.next_doc_id += 1

        # Count TF using Counter
        tf_counts = Counter(tokens)

        # Update index
        for token, freq in tf_counts.items():
            self.index[token][doc_id] = freq

        # Store metadata
        self.docs[doc_id] = {
            "url": url,
            "length": len(tokens)
        }

        return doc_id

    def get_index(self):
        """
        Returns the full inverted index.
        """
        return self.index

    def get_docs(self):
        """
        Returns document metadata.
        """
        return self.docs

    def total_docs(self):
        """
        Number of indexed documents.
        """
        return len(self.docs)
