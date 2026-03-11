"""
GitHub repository search and metadata enrichment.
"""

from __future__ import annotations

import datetime as dt
from typing import Any, Dict, List

from utils import GITHUB_API_BASE, safe_get_json


class GitHubSearchClient:
    def search_repositories(self, preferences: Dict[str, Any], max_results: int = 20) -> List[Dict[str, Any]]:
        topic = preferences.get("topic", "python")
        tutorial_required = preferences.get("tutorial_required", False)
        innovation = preferences.get("innovation", False)
        popularity = preferences.get("popularity", False)
        language = preferences.get("language")

        q_parts = [f"{topic} in:name,description,readme", "archived:false"]
        if language:
            q_parts.append(f"language:{language}")
        if tutorial_required:
            q_parts.append("(tutorial OR guide OR walkthrough OR example)")
        if preferences.get("difficulty") == "beginner":
            q_parts.append("(beginner OR starter OR easy)")
        if popularity:
            q_parts.append("stars:>=100")
        if innovation:
            recent_cutoff = (dt.datetime.utcnow() - dt.timedelta(days=365)).strftime("%Y-%m-%d")
            q_parts.extend([f"pushed:>={recent_cutoff}", "stars:>=25"])

        sort = "best match"
        if popularity:
            sort = "stars"
        elif innovation:
            sort = "updated"

        data = safe_get_json(
            f"{GITHUB_API_BASE}/search/repositories",
            params={
                "q": " ".join(q_parts),
                "sort": sort if sort != "best match" else None,
                "order": "desc",
                "per_page": max_results,
            },
        )
        items = []
        if "_error" not in data:
            items = data.get("items", [])

        # Fallback: relax strict text qualifiers if nothing is found.
        if not items:
            relaxed_q = [f"{topic} in:name,description", "archived:false"]
            if language:
                relaxed_q.append(f"language:{language}")
            if popularity:
                relaxed_q.append("stars:>=50")
            if innovation:
                recent_cutoff = (dt.datetime.utcnow() - dt.timedelta(days=365)).strftime("%Y-%m-%d")
                relaxed_q.extend([f"pushed:>={recent_cutoff}", "stars:>=10"])

            retry = safe_get_json(
                f"{GITHUB_API_BASE}/search/repositories",
                params={
                    "q": " ".join(relaxed_q),
                    "sort": sort if sort != "best match" else None,
                    "order": "desc",
                    "per_page": max_results,
                },
            )
            if "_error" not in retry:
                items = retry.get("items", [])

        # Exclude low-signal placeholder repos.
        filtered = [item for item in items if item.get("size", 0) > 10]
        return filtered

    def get_readme(self, owner: str, repo: str) -> Dict[str, Any]:
        return safe_get_json(f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme")

    def get_contributor_count(self, owner: str, repo: str) -> int:
        # contributors endpoint is paginated; first page is enough for a useful count signal.
        data = safe_get_json(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contributors",
            params={"per_page": 100, "anon": "true"},
        )
        if isinstance(data, dict) and "_error" in data:
            return 0
        if isinstance(data, list):
            return len(data)
        return 0

    def extract_technologies(self, repo: Dict[str, Any], readme_text: str) -> List[str]:
        tech = set()

        if repo.get("language"):
            tech.add(repo["language"])
        for topic in repo.get("topics", []):
            tech.add(topic)

        lower_readme = readme_text.lower()
        known = [
            "pytorch",
            "tensorflow",
            "scikit-learn",
            "fastapi",
            "flask",
            "django",
            "streamlit",
            "langchain",
            "opencv",
            "transformers",
            "docker",
            "kubernetes",
            "postgresql",
            "redis",
        ]
        for item in known:
            if item in lower_readme:
                tech.add(item)

        return sorted(tech)
