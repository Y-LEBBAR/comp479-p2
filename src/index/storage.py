import json
import pickle


def save_index_json(indexer, path: str):
    """
    Save the index and metadata in JSON format.
    Converts defaultdict to normal dict for compatibility.
    """

    data = {
        "index": {token: dict(postings) for token, postings in indexer.index.items()},
        "docs": indexer.docs
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_index_json(path: str):
    """
    Load index + metadata from a JSON file.
    Returns (index, docs) as Python dicts.
    """

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["index"], data["docs"]


def save_index_pickle(indexer, path: str):
    """
    Save the index using pickle (fastest).
    """

    data = {
        "index": indexer.index,
        "docs": indexer.docs
    }

    with open(path, "wb") as f:
        pickle.dump(data, f)


def load_index_pickle(path: str):
    """
    Load index and metadata from a pickle file.
    """

    with open(path, "rb") as f:
        data = pickle.load(f)

    return data["index"], data["docs"]
