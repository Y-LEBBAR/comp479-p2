from crawler.crawler import SpectrumCrawler
from index.pdf_extractor import download_pdf, extract_pdf_text
from index.tokenizer import Tokenizer
from index.indexer import Indexer
from index.storage import save_index_json


def run_pipeline(
    seed_url: str = "https://spectrum.library.concordia.ca/",
    max_files: int = 50,
    output_path: str = "data/index.json"
):
    """
    Full pipeline:
        - crawl Spectrum for PDF URLs
        - download each PDF
        - extract text
        - tokenize
        - index tokens
        - save index to disk
    """

    print("=== Starting Spectrum Crawler ===")
    print(f"Max files set to : {max_files}")
    crawler = SpectrumCrawler(seed_url, max_files)
    crawl_results = crawler.crawl()

    pdf_urls = crawl_results["pdf_urls"]
    print(f"Found {len(pdf_urls)} PDF links")

    tokenizer = Tokenizer(use_stemming=False)
    indexer = Indexer()

    print("\n=== Processing PDFs ===")

    for url in pdf_urls:
        print(f"Processing: {url}")

        pdf_bytes = download_pdf(url)
        if not pdf_bytes:
            print("  [Error] Failed to download PDF")
            continue

        text = extract_pdf_text(pdf_bytes)
        if not text.strip():
            print("  [Warning] Empty or unreadable PDF")
            continue

        tokens = tokenizer.tokenize(text)
        indexer.add_document(tokens, url)
        print(f"  Indexed {len(tokens)} tokens")

    print("\n=== Saving Index ===")
    save_index_json(indexer, output_path)
    print(f"Index saved to {output_path}")

    print("\n=== Pipeline Complete ===")
    print(f"Total documents indexed: {indexer.total_docs()}")


if __name__ == "__main__":
    run_pipeline()
