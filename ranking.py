"""
Ranking engine for repositories based on user intent.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List

from utils import clamp, days_since


class RepoRanker:
    def rank(self, repos: List[Dict[str, Any]], preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        scored = []
        for repo in repos:
            score = self._score(repo, preferences)
            repo_copy = dict(repo)
            repo_copy["raw_score"] = score
            scored.append(repo_copy)

        # Normalize to 0-100 for user-friendly ranking display.
        raw_scores = [float(item.get("raw_score", 0.0)) for item in scored]
        min_score = min(raw_scores) if raw_scores else 0.0
        max_score = max(raw_scores) if raw_scores else 0.0

        for item in scored:
            raw = float(item.get("raw_score", 0.0))
            if max_score == min_score:
                item["score"] = 100.0 if raw > 0 else 0.0
            else:
                item["score"] = ((raw - min_score) / (max_score - min_score)) * 100.0

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def activity_status(self, pushed_at: str | None) -> str:
        days = days_since(pushed_at)
        if days <= 60:
            return "active"
        if days <= 180:
            return "moderately active"
        return "inactive"

    def _score(self, repo: Dict[str, Any], preferences: Dict[str, Any]) -> float:
        stars = float(repo.get("stars", 0))
        forks = float(repo.get("forks", 0))
        contributors = float(repo.get("contributors", 0))
        readme_length = float(repo.get("readme_length", 0))
        has_tutorial = 1.0 if repo.get("has_tutorial") else 0.0
        tutorial_links = float(len(repo.get("tutorial_links", [])))
        tech_count = float(len(repo.get("technologies", [])))
        recency_days = float(days_since(repo.get("pushed_at")))

        popularity_score = (
            math.log1p(stars) * 22
            + math.log1p(forks) * 12
            + math.log1p(contributors) * 8
        )
        beginner_score = (
            clamp(readme_length / 300.0, 0, 35) * 1.8
            + has_tutorial * 22
            + clamp(tutorial_links, 0, 6) * 2
            + (6 if contributors >= 3 else 0)
        )
        innovation_score = (
            clamp((365 - recency_days) / 365, 0, 1) * 70
            + tech_count * 3
            + (10 if repo.get("activity_status") == "active" else 0)
            + math.log1p(stars) * 4
        )

        final = 0.0

        if preferences.get("popularity"):
            final += popularity_score
        if preferences.get("innovation"):
            final += innovation_score
        if preferences.get("difficulty") == "beginner":
            final += beginner_score

        # Default balanced scoring when intent is broad.
        if not any(
            [
                preferences.get("popularity"),
                preferences.get("innovation"),
                preferences.get("difficulty") == "beginner",
            ]
        ):
            final += (popularity_score * 0.5) + (innovation_score * 0.3) + (beginner_score * 0.2)

        if preferences.get("tutorial_required"):
            final += 20 if has_tutorial else -10

        return float(final)
