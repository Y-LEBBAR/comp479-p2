import requests
from urllib.parse import urljoin, urlparse, urlunparse


def normalize_url(base_url: str, link: str) -> str | None:
    """
    Convert a raw href extracted from HTML into a normalized absolute URL.
    Handles:
        - relative paths
        - absolute paths
        - stripping fragments
        - ignoring javascript/mailto links

    Returns:
        Absolute URL (str) or None if invalid.
    """

    if not link or link.startswith("#"):
        return None

    # Skip non-HTTP links
    if link.startswith("javascript:") or link.startswith("mailto:"):
        return None

    # Create a full URL relative to current page
    absolute = urljoin(base_url, link)

    # Remove fragments (#section)
    parsed = urlparse(absolute)
    cleaned = parsed._replace(fragment="")
    return urlunparse(cleaned)


def in_same_domain(url: str, domain_root: str) -> bool:
    """
    Ensure the URL belongs to the same domain as domain_root.
    Example:
        url:          https://spectrum.library.concordia.ca/page/1
        domain_root:  https://spectrum.library.concordia.ca
        → True
    """
    if not url:
        return False

    parsed = urlparse(url)
    root = urlparse(domain_root)

    return parsed.netloc == root.netloc


def is_pdf(url: str) -> bool:
    """
    Detect if the URL points to a PDF.
    Handles:
        file.pdf
        file.PDF
        file.pdf?download=1
    """
    if not url:
        return False

    parsed = urlparse(url)
    return parsed.path.lower().endswith(".pdf")


def safe_request(url: str, timeout: float = 5.0) -> requests.Response | None:
    """
    Safe wrapper around requests.get().
    Returns:
        Response object or None on error.
    """

    try:
        resp = requests.get(url, timeout=timeout)
        return resp
    except Exception:
        return None
