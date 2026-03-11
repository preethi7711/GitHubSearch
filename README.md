# Smart Developer Repo Agent

Smart Developer Repo Agent is a local Python CLI assistant that finds useful GitHub repositories from natural language queries and detects tutorial resources in each project.

## Features

- Natural query parsing
  - topic (NLP, AI, scraping, etc.)
  - difficulty (beginner/intermediate/advanced)
  - popularity intent
  - innovation intent
  - tutorial requirement
- GitHub repository search using GitHub REST API
- README analyzer for tutorial detection and tutorial link extraction
- Ranking engine for:
  - popular projects
  - beginner-friendly projects
  - innovative/recent projects
- YouTube fallback finder (top 3) if no tutorial is found in the repo
- Extra metadata:
  - contributors count
  - activity status (active/moderately active/inactive)
  - technologies used

## Project Structure

```text
smart-dev-agent
│
├── main.py
├── query_parser.py
├── github_search.py
├── readme_analyzer.py
├── tutorial_detector.py
├── youtube_finder.py
├── ranking.py
├── utils.py
├── requirements.txt
└── README.md
```

## Installation

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: set a GitHub token to avoid low anonymous rate limits.

Windows PowerShell:

```powershell
$env:GITHUB_TOKEN="your_token_here"
```

Linux/macOS:

```bash
export GITHUB_TOKEN="your_token_here"
```

## Usage

Run from the `smart-dev-agent` directory:

```bash
python main.py
```

Example query:

```text
beginner NLP projects with tutorial
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

If no tutorial is present in README:

```text
Tutorial not found in repo.
Suggested YouTube tutorials:
- https://youtube.com/...
- https://youtube.com/...
```

## Notes

- The app uses only free APIs/sources:
  - GitHub REST API
  - `youtube-search-python`
- No paid APIs and no OpenAI API are required.
- If GitHub rate limits are hit, add `GITHUB_TOKEN` and retry.
