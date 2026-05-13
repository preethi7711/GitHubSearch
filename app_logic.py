"""
Shared application workflow for CLI and web frontends.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from github_search import GitHubSearchClient
from query_parser import QueryParser
from ranking import RepoRanker
from readme_analyzer import ReadmeAnalyzer
from tutorial_detector import TutorialDetector
from youtube_finder import YouTubeFinder


@dataclass
class SearchResult:
    query: str
    preferences: Dict[str, Any]
    repositories: List[Dict[str, Any]]
    errors: List[str]


class SmartDevAgentService:
    def __init__(self) -> None:
        self.parser = QueryParser()
        self.github_client = GitHubSearchClient()
        self.readme_analyzer = ReadmeAnalyzer(self.github_client)
        self.tutorial_detector = TutorialDetector()
        self.ranker = RepoRanker()
        self.youtube_finder = YouTubeFinder()

    def search(self, query: str, max_results: int = 20, top_n: int = 8) -> SearchResult:
        cleaned_query = query.strip()
        if not cleaned_query:
            return SearchResult(query=query, preferences={}, repositories=[], errors=["No query provided."])

        preferences = self.parser.parse(cleaned_query)
        repos = self.github_client.search_repositories(preferences, max_results=max_results)
        if not repos:
            return SearchResult(
                query=cleaned_query,
                preferences=preferences,
                repositories=[],
                errors=["No repositories found for the given query."],
            )

        enriched: List[Dict[str, Any]] = []
        errors: List[str] = []

        for repo in repos:
            owner = repo.get("owner", {}).get("login")
            name = repo.get("name")
            if not owner or not name:
                continue

            readme_data = self.readme_analyzer.analyze(owner, name)
            if readme_data.get("error"):
                errors.append(f"README unavailable for {owner}/{name}: {readme_data['error']}")

            has_tutorial = self.tutorial_detector.has_tutorial_content(readme_data["text"])
            tutorial_links = self.tutorial_detector.extract_tutorial_links(readme_data["text"])
            youtube_tutorial_links = self.tutorial_detector.extract_youtube_links(readme_data["text"])
            contributors = self.github_client.get_contributor_count(owner, name)
            technologies = self.github_client.extract_technologies(repo, readme_data["text"])

            merged_repo = {
                "name": name,
                "full_name": repo.get("full_name"),
                "description": repo.get("description") or "No description provided.",
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "language": repo.get("language") or "Unknown",
                "updated_at": repo.get("updated_at"),
                "pushed_at": repo.get("pushed_at"),
                "html_url": repo.get("html_url"),
                "readme_length": readme_data["length"],
                "has_tutorial": has_tutorial,
                "tutorial_links": tutorial_links,
                "youtube_tutorial_links": youtube_tutorial_links,
                "contributors": contributors,
                "topics": repo.get("topics", []),
                "technologies": technologies,
            }
            merged_repo["activity_status"] = self.ranker.activity_status(merged_repo.get("pushed_at"))
            merged_repo["difficulty"] = self.parser.estimate_difficulty_label(preferences, merged_repo)
            enriched.append(merged_repo)

        ranked = self.ranker.rank(enriched, preferences)
        limited = ranked[: min(top_n, len(ranked))]

        needs_tutorial = preferences.get("tutorial_required", False)
        youtube_preferred = preferences.get("youtube_preferred", False) or preferences.get("free_resources", False)
        topic = preferences.get("topic", "")
        for repo in limited:
            existing_youtube = repo.get("youtube_tutorial_links", [])
            should_fetch_youtube = (needs_tutorial or youtube_preferred) and not existing_youtube
            if should_fetch_youtube:
                repo_name = repo.get("name", "")
                search_term = f"{topic} {repo_name} free youtube tutorial".strip()
                repo["youtube_suggestions"] = self.youtube_finder.search(search_term, limit=3)
            else:
                repo["youtube_suggestions"] = []

        return SearchResult(
            query=cleaned_query,
            preferences=preferences,
            repositories=limited,
            errors=errors,
        )
