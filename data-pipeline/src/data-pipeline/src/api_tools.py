from __future__ import annotations
import os
from typing import Dict, List, Optional
import requests
from .utils import get_logger

logger = get_logger("breweries.api")

class APITools:
    """Handles API requests to Open Brewery DB."""

    def __init__(self, base_url: str | None = None, per_page: int | None = None, timeout: int = 30):
        self.base_url = base_url or os.getenv("BREWERY_API_BASE", "https://api.openbrewerydb.org/v1")
        self.per_page = int(per_page or os.getenv("BREWERY_PER_PAGE", 50))
        self.timeout = timeout

    def _get(self, path: str, params: Optional[Dict] = None) -> requests.Response:
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        logger.info(f"HTTP GET {url} params={params}")
        resp = requests.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def fetch_page(self, page: int) -> List[Dict]:
        params = {"page": page, "per_page": self.per_page}
        resp = self._get("breweries", params=params)
        return resp.json()

    def valid_brewery_types(self) -> List[str]:
        return [
            "micro", "nano", "regional", "brewpub", "large", "planning",
            "bar", "contract", "proprietor", "closed", "taproom"
        ]
