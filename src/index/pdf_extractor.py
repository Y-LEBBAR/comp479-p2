import io
import requests
from pdfminer.high_level import extract_text_to_fp


def download_pdf(url: str) -> bytes | None:
    """
    Downloads a PDF and returns the raw bytes.
    Returns None if the download fails.
    """
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        return resp.content
    except Exception:
        return None


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes using pdfminer.
    Returns raw text (UTF-8).
    """
    if not pdf_bytes:
        return ""

    input_buffer = io.BytesIO(pdf_bytes)
    output_buffer = io.StringIO()

    try:
        extract_text_to_fp(input_buffer, output_buffer, laparams=None)
        text = output_buffer.getvalue()
        return text
    except Exception:
        return ""
