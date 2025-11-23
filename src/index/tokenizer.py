import re

# Basic English stopword list (can be expanded)
STOPWORDS = {
    "the", "and", "is", "in", "of", "to", "a", "for", "on", "with", "as", "by",
    "an", "be", "this", "that", "are", "from", "it", "at", "or", "which"
}


class Tokenizer:
    """
    Lightweight, fast tokenizer for document text.
    Steps:
        - lowercase
        - remove punctuation/non-alphanumerics
        - split on whitespace
        - remove stopwords
    """

    def __init__(self, use_stemming: bool = False):
        self.use_stemming = use_stemming

        # Lazy import for stemmer (only if needed)
        if use_stemming:
            from nltk.stem import SnowballStemmer
            self.stemmer = SnowballStemmer("english")

    def tokenize(self, text: str) -> list[str]:
        """
        Convert raw text to normalized tokens.
        """
        if not text:
            return []

        # Lowercase
        text = text.lower()

        # Replace non-alphanumeric characters with spaces
        # Keeps only letters and numbers
        text = re.sub(r"[^a-z0-9]+", " ", text)

        # Split into tokens
        tokens = text.split()

        # Remove stopwords
        tokens = [tok for tok in tokens if tok not in STOPWORDS]

        # Optional stemming
        if self.use_stemming:
            tokens = [self.stemmer.stem(tok) for tok in tokens]

        return tokens
