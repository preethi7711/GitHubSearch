"""
Detect tutorial presence and links inside README content.
"""

from __future__ import annotations

import re
from typing import List


class TutorialDetector:
    KEYWORDS = [
        "tutorial",
        "guide",
        "walkthrough",
        "youtube",
        "course",
        "how to",
        "example",
    ]

    URL_PATTERN = re.compile(r"https?://[^\s<>\"]+", flags=re.IGNORECASE)

    def has_tutorial_content(self, readme_text: str) -> bool:
        if not readme_text:
            return False
        lower = readme_text.lower()
        return any(keyword in lower for keyword in self.KEYWORDS)

    def extract_tutorial_links(self, readme_text: str) -> List[str]:
        if not readme_text:
            return []

        lines = readme_text.splitlines()
        candidates = []
        for line in lines:
            lower = line.lower()
            if any(keyword in lower for keyword in self.KEYWORDS):
                candidates.extend(self.URL_PATTERN.findall(line))

        # fallback: include YouTube/tutorial-like links from the entire README
        all_links = self.URL_PATTERN.findall(readme_text)
        for link in all_links:
            ll = link.lower()
            if any(k in ll for k in ["youtube.com", "youtu.be", "tutorial", "guide", "course"]):
                candidates.append(link)

        # Keep order, remove duplicates, and trim markdown artifacts.
        seen = set()
        deduped = []
        for link in candidates:
            cleaned = link.strip().rstrip(".,)]}\"'`")
            cleaned = cleaned.lstrip("([\"'`")
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                deduped.append(cleaned)
        return deduped[:10]

    def extract_youtube_links(self, readme_text: str) -> List[str]:
        links = self.extract_tutorial_links(readme_text)
        youtube_links = []
        for link in links:
            lowered = link.lower()
            if "youtube.com/" in lowered or "youtu.be/" in lowered:
                youtube_links.append(link)
        return youtube_links[:10]
