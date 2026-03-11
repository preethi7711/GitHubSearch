"""
CLI entry point for Smart Developer Repo Agent.
"""

from __future__ import annotations

from typing import Any, Dict, List

from github_search import GitHubSearchClient
from query_parser import QueryParser
from ranking import RepoRanker
from readme_analyzer import ReadmeAnalyzer
from tutorial_detector import TutorialDetector
from youtube_finder import YouTubeFinder


def _print_repo_result(repo: Dict[str, Any]) -> None:
    print("=" * 80)
    print(f"Project: {repo.get('name', 'N/A')}")
    print(f"Description: {repo.get('description', 'N/A')}")
    print(f"Stars: {repo.get('stars', 0)}")
    print(f"Forks: {repo.get('forks', 0)}")
    print(f"Language: {repo.get('language', 'Unknown')}")
    print(f"Difficulty: {repo.get('difficulty', 'Unknown')}")
    print(f"Contributors: {repo.get('contributors', 0)}")
    print(f"Activity Status: {repo.get('activity_status', 'unknown')}")
    print(f"Technologies: {', '.join(repo.get('technologies', [])) or 'N/A'}")
    print(f"Last Updated: {repo.get('updated_at', 'N/A')}")
    print(f"Repo Link: {repo.get('html_url', 'N/A')}")
    print(f"Tutorial inside repo: {'YES' if repo.get('has_tutorial') else 'NO'}")

    tutorial_links = repo.get("tutorial_links", [])
    youtube_links = repo.get("youtube_tutorial_links", [])
    if youtube_links:
        print("Free YouTube tutorial links:")
        for link in youtube_links:
            print(f"- {link}")
    elif tutorial_links:
        print("Tutorial links:")
        for link in tutorial_links:
            print(f"- {link}")
    else:
        if repo.get("has_tutorial"):
            print("Tutorial references found in README, but no direct links were extracted.")
        else:
            print("Tutorial not found in repo.")
        yt_links = repo.get("youtube_suggestions", [])
        if yt_links:
            print("Suggested YouTube tutorials:")
            for link in yt_links:
                print(f"- {link}")
    print(f"Ranking score: {repo.get('score', 0):.2f}/100")


def run() -> None:
    print("Smart Developer Repo Agent")
    print("Enter a search query (example: beginner NLP projects with tutorial)")
    user_query = input("> ").strip()
    if not user_query:
        print("No query provided. Exiting.")
        return

    parser = QueryParser()
    preferences = parser.parse(user_query)
    print("\nDetected preferences:")
    for key, value in preferences.items():
        print(f"- {key}: {value}")

    github_client = GitHubSearchClient()
    readme_analyzer = ReadmeAnalyzer(github_client)
    tutorial_detector = TutorialDetector()
    ranker = RepoRanker()
    youtube_finder = YouTubeFinder()

    repos = github_client.search_repositories(preferences, max_results=20)
    if not repos:
        print("\nNo repositories found for the given query.")
        return

    enriched: List[Dict[str, Any]] = []
    for repo in repos:
        owner = repo.get("owner", {}).get("login")
        name = repo.get("name")
        if not owner or not name:
            continue

        readme_data = readme_analyzer.analyze(owner, name)
        has_tutorial = tutorial_detector.has_tutorial_content(readme_data["text"])
        tutorial_links = tutorial_detector.extract_tutorial_links(readme_data["text"])
        youtube_tutorial_links = tutorial_detector.extract_youtube_links(readme_data["text"])
        contributors = github_client.get_contributor_count(owner, name)
        technologies = github_client.extract_technologies(repo, readme_data["text"])

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
        merged_repo["activity_status"] = ranker.activity_status(merged_repo.get("pushed_at"))
        merged_repo["difficulty"] = parser.estimate_difficulty_label(preferences, merged_repo)
        enriched.append(merged_repo)

    ranked = ranker.rank(enriched, preferences)
    top_n = min(8, len(ranked))

    needs_tutorial = preferences.get("tutorial_required", False)
    youtube_preferred = preferences.get("youtube_preferred", False) or preferences.get("free_resources", False)
    topic = preferences.get("topic", "")
    for repo in ranked[:top_n]:
        existing_youtube = repo.get("youtube_tutorial_links", [])
        should_fetch_youtube = (needs_tutorial or youtube_preferred) and not existing_youtube
        if should_fetch_youtube:
            repo_name = repo.get("name", "")
            search_term = f"{topic} {repo_name} free youtube tutorial".strip()
            repo["youtube_suggestions"] = youtube_finder.search(search_term, limit=3)
        else:
            repo["youtube_suggestions"] = []

    print(f"\nTop {top_n} repositories:\n")
    for repo in ranked[:top_n]:
        _print_repo_result(repo)


if __name__ == "__main__":
    run()
