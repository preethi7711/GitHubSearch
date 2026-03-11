"""
Find YouTube tutorials using a free search package.
"""

from __future__ import annotations

import re
from typing import List
from urllib.parse import quote_plus

import requests

try:
    from youtubesearchpython import VideosSearch
except Exception:  # pragma: no cover
    VideosSearch = None


class YouTubeFinder:
    def search(self, query: str, limit: int = 3) -> List[str]:
        if not query or VideosSearch is None:
            return self._search_by_scraping(query, limit=limit)
        try:
            videos = VideosSearch(query, limit=limit)
            result = videos.result()
            links = []
            for item in result.get("result", []):
                link = item.get("link")
                if link:
                    links.append(link)
            if links:
                return links[:limit]
            return self._search_by_scraping(query, limit=limit)
        except Exception:
            return self._search_by_scraping(query, limit=limit)

    def _search_by_scraping(self, query: str, limit: int = 3) -> List[str]:
        # Fallback scraper when youtube-search-python/httpx fails due local proxy config.
        if not query:
            return []
        url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            with requests.Session() as session:
                session.trust_env = False
                response = session.get(url, headers=headers, timeout=15)
                response.raise_for_status()
        except requests.RequestException:
            return []

        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', response.text)
        seen = set()
        links = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                links.append(f"https://www.youtube.com/watch?v={vid}")
            if len(links) >= limit:
                break
        return links
