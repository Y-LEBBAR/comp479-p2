from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from .robots import RobotsTxt
from .utils import (
    normalize_url,
    in_same_domain,
    is_pdf,
    safe_request
)

import warnings
from bs4 import XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

class SpectrumCrawler:
    """
    BFS-based crawler for Concordia Spectrum.
    Collects PDF URLs while respecting robots.txt and domain restrictions.
    """

    def __init__(self, seed_url: str, max_files: int):
        self.seed_url = seed_url
        self.max_files = max_files

        # Domain root, e.g., "https://spectrum.library.concordia.ca"
        parsed = urlparse(seed_url)
        self.domain_root = f"{parsed.scheme}://{parsed.netloc}"

        # Data structures
        self.frontier = deque([seed_url])
        self.visited = set()
        self.pdf_links = []

        # Always respect robots.txt (default assignment requirement)
        self.robots = RobotsTxt(seed_url)

    def crawl(self):
        """
        Main BFS crawl loop.
        Returns a dictionary summarizing crawl results.
        """

        while self.frontier and len(self.pdf_links) < self.max_files:

            current_url = self.frontier.popleft()

            # Skip revisits
            if current_url in self.visited:
                continue

            # Enforce robots.txt
            if not self.robots.is_allowed(current_url):
                continue

            # Enforce domain restriction
            if not in_same_domain(current_url, self.domain_root):
                continue

            # Mark visited
            self.visited.add(current_url)

            # Fetch HTML
            resp = safe_request(current_url)
            if resp is None or resp.status_code != 200:
                continue

            html = resp.text
            new_links = self._extract_links(current_url, html)

            # Process discovered links
            for link in new_links:
                if is_pdf(link):
                    if len(self.pdf_links) < self.max_files:
                        self.pdf_links.append(link)
                else:
                    self.frontier.append(link)

        return {
            "pdf_urls": self.pdf_links,
            "visited_count": len(self.visited),
            "pages_visited": list(self.visited),
        }

    def _extract_links(self, base_url: str, html: str):
        """
        Extract all links, normalize them, and return a list of valid URLs.
        """
        soup = BeautifulSoup(html, "html.parser")


        collected = []

        for tag in soup.find_all("a"):
            href = tag.get("href")
            normalized = normalize_url(base_url, href)

            if not normalized:
                continue

            # Stay inside allowed domain
            if not in_same_domain(normalized, self.domain_root):
                continue

            collected.append(normalized)

        return collected
