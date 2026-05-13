"""
CLI entry point for Smart Developer Repo Agent.
"""

from __future__ import annotations

from typing import Any, Dict

from app_logic import SmartDevAgentService


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

    service = SmartDevAgentService()
    result = service.search(user_query)
    preferences = result.preferences
    print("\nDetected preferences:")
    for key, value in preferences.items():
        print(f"- {key}: {value}")

    if result.errors:
        for error in result.errors:
            print(f"\nWarning: {error}")

    if not result.repositories:
        print("\nNo repositories found for the given query.")
        return

    print(f"\nTop {len(result.repositories)} repositories:\n")
    for repo in result.repositories:
        _print_repo_result(repo)


if __name__ == "__main__":
    run()
