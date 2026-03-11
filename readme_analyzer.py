"""
Repository README fetch and preprocessing.
"""

from __future__ import annotations

from typing import Any, Dict

from github_search import GitHubSearchClient
from utils import decode_readme_base64


class ReadmeAnalyzer:
    def __init__(self, github_client: GitHubSearchClient) -> None:
        self.github_client = github_client

    def analyze(self, owner: str, repo: str) -> Dict[str, Any]:
        data = self.github_client.get_readme(owner, repo)
        if "_error" in data:
            return {"text": "", "length": 0, "error": data["_error"]}

        text = decode_readme_base64(data.get("content", ""))
        return {
            "text": text,
            "length": len(text),
            "error": None,
        }
