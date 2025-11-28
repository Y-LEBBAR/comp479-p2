#from index.storage import load_index_json
from src.index.storage import load_index_json

def get_docs_for_term(index: dict, term: str) -> set[int]:
    """
    Returns the set of document IDs containing the given token.
    """
    term = term.lower()
    if term not in index:
        return set()
    return set(index[term].keys())


def save_collection_to_file(doc_ids: set[int], docs_meta: dict, path: str):
    """
    Save (doc_id, url) pairs to a text file.
    Format:
        doc_id    url
    """
    with open(path, "w", encoding="utf-8") as f:
        for doc_id in sorted(doc_ids):
            url = docs_meta[str(doc_id)]["url"] if isinstance(doc_id, str) else docs_meta[doc_id]["url"]
            f.write(f"{doc_id}\t{url}\n")


def run_queries(index_path: str = "data/index.json"):
    """
    Load index and run queries for 'sustainability' and 'waste'.
    Save:
        sustainability_docs.txt
        waste_docs.txt
        my_collection.txt
    """

    print("=== Loading Index ===")
    index, docs_meta = load_index_json(index_path)

    # 1. Query terms
    sustainability_docs = get_docs_for_term(index, "sustainability")
    waste_docs = get_docs_for_term(index, "waste")

    print(f"Documents with 'sustainability': {len(sustainability_docs)}")
    print(f"Documents with 'waste': {len(waste_docs)}")

    # 2. Intersection + union
    intersection = sustainability_docs.intersection(waste_docs)
    my_collection = sustainability_docs.union(waste_docs)

    print(f"Documents in both: {len(intersection)}")
    print(f"MyCollection size: {len(my_collection)}")

    # 3. Save output files
    save_collection_to_file(sustainability_docs, docs_meta, "data/sustainability_docs.txt")
    save_collection_to_file(waste_docs, docs_meta, "data/waste_docs.txt")
    save_collection_to_file(my_collection, docs_meta, "data/my_collection.txt")

    print("\n=== Query Phase Complete ===")
    print("Saved: sustainability_docs.txt, waste_docs.txt, my_collection.txt")


if __name__ == "__main__":
    run_queries(r"C:\Yannis\School\UNI\Y4-T1\COMP479\Coding\Project_2\data\index.json")
