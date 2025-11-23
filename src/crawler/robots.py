import requests
from urllib.parse import urlparse


class RobotsTxt:
    """
    Handles fetching and parsing robots.txt for a given domain.
    Provides is_allowed(url) to verify whether a URL is crawlable.
    """

    def __init__(self, seed_url: str):
        self.seed_url = seed_url
        self.domain_root = self._get_domain_root(seed_url)
        self.disallowed_paths = []       # list of path prefixes to block
        self.allowed_paths = []          # optional (not strictly required)
        self.fetched = False

        self._fetch_and_parse()

    def _get_domain_root(self, url: str) -> str:
        """
        Convert the seed URL into the root domain (scheme + netloc).
        Example:
            https://spectrum.library.concordia.ca/some/page
            → https://spectrum.library.concordia.ca
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def _fetch_and_parse(self):
        """
        Download and parse robots.txt from the domain root.
        If robots.txt cannot be fetched, the crawler proceeds as if everything is allowed.
        """
        robots_url = f"{self.domain_root}/robots.txt"

        try:
            resp = requests.get(robots_url, timeout=5)
        except Exception:
            # Treat as fully allowed if unreachable
            self.fetched = True
            return

        if resp.status_code != 200:
            # No robots file or unavailable → fully allowed
            self.fetched = True
            return

        self._parse_robots_text(resp.text)
        self.fetched = True

    def _parse_robots_text(self, text: str):
        """
        Minimal robots.txt parser:
        - Reads Disallow: and Allow: lines
        - Does not handle user-agent selection; assumes global rules
        """
        for line in text.splitlines():
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Normalize line e.g. "Disallow: /path"
            if line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    self.disallowed_paths.append(path)

            elif line.lower().startswith("allow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    self.allowed_paths.append(path)

    def is_allowed(self, url: str) -> bool:
        """
        Check whether a given URL is permitted under robots.txt rules.
        We match paths based on prefix rules:
          disallow path:   block
          allow path:      allow (overrides disallow)

        Returns: True if allowed, False if disallowed.
        """
        parsed = urlparse(url)
        path = parsed.path

        # Allow rules override disallow rules, so check them first
        for allowed in self.allowed_paths:
            if path.startswith(allowed):
                return True

        # Check disallowed rules
        for disallowed in self.disallowed_paths:
            if path.startswith(disallowed):
                return False

        # Default: allowed
        return True
