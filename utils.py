"""
Shared helper utilities for API calls, parsing, and scoring.
"""

from __future__ import annotations

import base64
import datetime as dt
import os
from typing import Any, Dict, Optional

import requests


GITHUB_API_BASE = "https://api.github.com"


def github_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "smart-dev-agent",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def safe_get_json(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 20) -> Dict[str, Any]:
    try:
        response = requests.get(url, headers=github_headers(), params=params, timeout=timeout)
    except requests.exceptions.ProxyError:
        # Retry without system proxy settings when local proxy config is broken.
        try:
            with requests.Session() as session:
                session.trust_env = False
                response = session.get(url, headers=github_headers(), params=params, timeout=timeout)
        except requests.RequestException as exc:
            return {"_error": f"Request failed: {exc}"}
    except requests.RequestException as exc:
        return {"_error": f"Request failed: {exc}"}

    try:
        if response.status_code == 403:
            return {"_error": "GitHub API rate limit reached. Add GITHUB_TOKEN for higher limits."}
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        return {"_error": f"Request failed: {exc}"}


def decode_readme_base64(encoded: str) -> str:
    if not encoded:
        return ""
    try:
        return base64.b64decode(encoded).decode("utf-8", errors="ignore")
    except Exception:
        return ""


def parse_github_datetime(value: str | None) -> Optional[dt.datetime]:
    if not value:
        return None
    try:
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


def days_since(timestamp: str | None) -> int:
    parsed = parse_github_datetime(timestamp)
    if not parsed:
        return 10_000
    now = dt.datetime.utcnow()
    return max(0, (now - parsed).days)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))
