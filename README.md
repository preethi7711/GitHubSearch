# Smart Developer Repo Agent

Smart Developer Repo Agent is a local AI-powered GitHub discovery tool for learners and developers. It turns natural-language search prompts into curated repository recommendations, checks README quality, detects tutorial coverage, and surfaces learning-friendly projects through both a CLI and a polished Streamlit web app.

## Overview

Finding a good project to learn from is usually messy:

- GitHub search returns too many weak matches
- beginner-friendly projects are hard to separate from advanced ones
- tutorials are often missing or buried in the README
- strong repositories are not always the easiest ones to learn from

Smart Developer Repo Agent helps solve that by combining:

- natural-language query parsing
- GitHub repository search
- README tutorial detection
- ranking based on learning intent
- YouTube fallback suggestions when built-in tutorials are missing

The result is a more useful shortlist of repositories for learning, exploring, and project selection.

## Key Features

- Natural-language repository discovery
  - parse topic, difficulty, popularity, innovation, tutorials, and language intent from plain English
- GitHub search pipeline
  - search public repositories using the GitHub REST API
- Tutorial-aware learning analysis
  - inspect READMEs for tutorial signals, tutorial links, and embedded YouTube resources
- Ranking engine
  - prioritize beginner-friendly, popular, or recently active projects depending on user intent
- Learning metadata enrichment
  - include stars, forks, contributors, activity status, technologies, and difficulty estimates
- YouTube fallback support
  - suggest free YouTube tutorials when the repository itself does not provide enough guidance
- Dual interface support
  - CLI for lightweight local use
  - premium Streamlit dashboard for a more visual workflow

## Web App Experience

The Streamlit frontend is designed as an AI developer discovery workspace with:

- dark SaaS-style UI
- sidebar filtering workspace
- AI-style search experience
- repository health and tutorial confidence indicators
- recommendation reasoning such as "Why Recommended"
- responsive repository cards with richer learning signals
- loading states, overview tables, and detailed learning resources

## Project Structure

```text
smart-dev-agent
|-- app_logic.py
|-- github_search.py
|-- main.py
|-- query_parser.py
|-- ranking.py
|-- readme_analyzer.py
|-- streamlit_app.py
|-- tutorial_detector.py
|-- ui_components.py
|-- utils.py
|-- youtube_finder.py
|-- requirements.txt
`-- README.md
```

## Architecture

The project is intentionally split into small focused modules:

- [main.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/main.py)
  CLI entry point
- [streamlit_app.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/streamlit_app.py)
  Streamlit frontend
- [app_logic.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/app_logic.py)
  shared search workflow used by both interfaces
- [query_parser.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/query_parser.py)
  natural-language intent parsing
- [github_search.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/github_search.py)
  GitHub API search and repository enrichment
- [readme_analyzer.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/readme_analyzer.py)
  README retrieval and preprocessing
- [tutorial_detector.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/tutorial_detector.py)
  tutorial and link extraction
- [ranking.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/ranking.py)
  repository scoring and ranking
- [youtube_finder.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/youtube_finder.py)
  YouTube tutorial fallback search
- [ui_components.py](/abs/c:/Users/Preet/Documents/Projects/Github_agent/smart-dev-agent/ui_components.py)
  reusable frontend styling and presentation helpers

## Requirements

- Python 3.10+
- internet access for GitHub and tutorial lookup

## Installation

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Optional but recommended: configure a GitHub token to avoid low anonymous rate limits.

Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="your_token_here"
```

Linux/macOS:

```bash
export GITHUB_TOKEN="your_token_here"
```

## Usage

### Run The CLI

From the `smart-dev-agent` directory:

```bash
python main.py
```

Example query:

```text
beginner NLP projects with tutorial
```

### Run The Web App

From the `smart-dev-agent` directory:

```bash
streamlit run streamlit_app.py
```

The web app lets you:

- search using natural language
- refine discovery intent with sidebar controls
- review repository metrics and ranking summaries
- inspect tutorial coverage and YouTube suggestions
- browse richer repository cards with learning insights

## Example Queries

```text
beginner NLP projects with tutorial
popular Python agent repos with free YouTube tutorials
latest computer vision repositories for beginners
best LLM repositories in Python
data science projects with walkthrough
```

## Example Output

```text
Project: NLP Sentiment Analyzer
Stars: 8500
Language: Python
Difficulty: Beginner
Tutorial inside repo: YES
Tutorial links:
- https://youtube.com/...
```

If no tutorial is found inside the repository:

```text
Tutorial not found in repo.
Suggested YouTube tutorials:
- https://youtube.com/...
- https://youtube.com/...
```

## Ranking Signals

Depending on the user query, the app can weigh:

- popularity
  stars, forks, contributors
- beginner friendliness
  README depth, tutorial presence, contributor activity
- innovation and freshness
  recent pushes, active development, modern tooling signals

The Streamlit app also derives presentation signals such as:

- tutorial confidence
- repository health
- estimated learning difficulty
- suitability analysis
- "Why Recommended" explanations

## Data Sources

The project uses free/public sources only:

- GitHub REST API
- `youtube-search-python`

No paid APIs are required. No OpenAI API is required.

## Notes

- If GitHub rate limits are hit, set `GITHUB_TOKEN` and retry.
- The CLI and Streamlit app share the same backend search workflow, so results stay consistent across both interfaces.
- The frontend improves presentation only; repository discovery and ranking logic remain centralized in the shared service layer.

## Future Improvement Ideas

- saved searches and history
- repository comparison mode
- exportable learning shortlists
- richer sorting and filtering
- multi-page dashboard navigation
- deeper README quality scoring
  
## Live Demo

[Try the App](https://search-smart-repo-agent.streamlit.app/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://search-smart-repo-agent.streamlit.app/)
