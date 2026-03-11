"""
Parse natural language user query into structured preferences.
"""

from __future__ import annotations

import re
from typing import Any, Dict


class QueryParser:
    DIFFICULTY_KEYWORDS = {
        "beginner": "beginner",
        "easy": "beginner",
        "intermediate": "intermediate",
        "advanced": "advanced",
        "expert": "advanced",
    }

    TOPIC_KEYWORDS = [
        "nlp",
        "ai",
        "machine learning",
        "deep learning",
        "computer vision",
        "web scraping",
        "data science",
        "llm",
        "agent",
        "chatbot",
        "automation",
        "python",
    ]
    LANGUAGE_KEYWORDS = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "java": "Java",
        "go": "Go",
        "rust": "Rust",
        "c++": "C++",
        "c#": "C#",
    }

    def parse(self, query: str) -> Dict[str, Any]:
        normalized = query.lower().strip()

        topic = self._extract_topic(normalized)
        difficulty = self._extract_difficulty(normalized)
        popularity = self._wants_popularity(normalized)
        innovation = self._wants_innovation(normalized)
        tutorial_required = self._wants_tutorial(normalized)
        language = self._extract_language(normalized)
        youtube_preferred = self._wants_youtube(normalized)
        free_resources = self._wants_free_resources(normalized)
        if youtube_preferred:
            tutorial_required = True

        return {
            "raw_query": query,
            "topic": topic,
            "difficulty": difficulty,
            "popularity": popularity,
            "innovation": innovation,
            "tutorial_required": tutorial_required,
            "language": language,
            "youtube_preferred": youtube_preferred,
            "free_resources": free_resources,
        }

    def estimate_difficulty_label(self, preferences: Dict[str, Any], repo: Dict[str, Any]) -> str:
        if preferences.get("difficulty"):
            return preferences["difficulty"].capitalize()

        stars = repo.get("stars", 0)
        readme_length = repo.get("readme_length", 0)
        has_tutorial = repo.get("has_tutorial", False)

        if has_tutorial and readme_length > 3000:
            return "Beginner"
        if stars > 10000 and readme_length > 1500:
            return "Intermediate"
        return "Advanced"

    def _extract_topic(self, normalized_query: str) -> str:
        for topic in sorted(self.TOPIC_KEYWORDS, key=len, reverse=True):
            if topic in normalized_query:
                return topic

        # Fallback: remove common meta words and keep the meaningful text.
        cleaned = re.sub(r"\b(projects?|with|and|for|most|popular|innovative|beginner|advanced|intermediate)\b", "", normalized_query)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned or "python"

    def _extract_difficulty(self, normalized_query: str) -> str | None:
        for word, label in self.DIFFICULTY_KEYWORDS.items():
            if re.search(rf"\b{re.escape(word)}\b", normalized_query):
                return label
        return None

    @staticmethod
    def _wants_popularity(normalized_query: str) -> bool:
        keywords = ["popular", "top", "best", "stars", "starred", "trending"]
        return any(k in normalized_query for k in keywords)

    @staticmethod
    def _wants_innovation(normalized_query: str) -> bool:
        keywords = ["innovative", "new", "recent", "latest", "cutting edge", "state of the art"]
        return any(k in normalized_query for k in keywords)

    @staticmethod
    def _wants_tutorial(normalized_query: str) -> bool:
        keywords = ["tutorial", "guide", "walkthrough", "course", "youtube", "how to", "example"]
        return any(k in normalized_query for k in keywords)

    @staticmethod
    def _wants_youtube(normalized_query: str) -> bool:
        keywords = ["youtube", "video tutorial", "yt"]
        return any(k in normalized_query for k in keywords)

    @staticmethod
    def _wants_free_resources(normalized_query: str) -> bool:
        keywords = ["free", "free resources", "no paid", "without paid"]
        return any(k in normalized_query for k in keywords)

    def _extract_language(self, normalized_query: str) -> str | None:
        for keyword, label in self.LANGUAGE_KEYWORDS.items():
            if re.search(rf"\b{re.escape(keyword)}\b", normalized_query):
                return label
        return None
