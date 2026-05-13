"""
Premium Streamlit frontend for Smart Developer Repo Agent.
"""

from __future__ import annotations

import html
from typing import Any, Dict, List

import streamlit as st

from app_logic import SearchResult, SmartDevAgentService
from ui_components import (
    DIFFICULTY_OPTIONS,
    LANGUAGE_OPTIONS,
    SUGGESTION_CHIPS,
    TOPIC_OPTIONS,
    active_filter_pills,
    apply_global_styles,
    compose_search_query,
    filter_repositories,
    render_empty_state,
    render_loading_skeleton,
    render_metric_card,
    render_repo_card,
    render_search_shell,
    render_section_header,
    render_topbar,
    render_warning_state,
    result_table,
)


st.set_page_config(
    page_title="Smart Developer Repo Agent",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _init_state() -> None:
    defaults = {
        "query": "beginner NLP projects with tutorial",
        "difficulty": "Any",
        "topic": "Any",
        "tutorial_required": True,
        "popularity": False,
        "innovation": False,
        "language": "Any",
        "max_results": 20,
        "top_n": 8,
        "min_score": 0,
        "active_only": False,
        "tutorial_only": False,
        "last_result": None,
        "last_query": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _sidebar_controls() -> Dict[str, Any]:
    with st.sidebar:
        st.markdown("### Workspace")
        st.caption("Compact search controls for shaping ranking quality without leaving the flow.")

        with st.container(border=True):
            st.markdown("**Search Setup**")
            max_results = st.slider("GitHub candidates", 5, 30, value=st.session_state.max_results, step=5, key="max_results")
            top_n = st.slider("Results shown", 3, 12, value=st.session_state.top_n, step=1, key="top_n")

        with st.container(border=True):
            st.markdown("**Difficulty**")
            difficulty = st.selectbox("Learning ramp", DIFFICULTY_OPTIONS, key="difficulty")

        with st.container(border=True):
            st.markdown("**Topic**")
            topic = st.selectbox("Primary topic", TOPIC_OPTIONS, key="topic")

        with st.container(border=True):
            st.markdown("**Tutorial Required**")
            tutorial_required = st.toggle("Prioritize tutorial-backed repositories", key="tutorial_required")

        with st.container(border=True):
            st.markdown("**Popularity**")
            popularity = st.toggle("Favor proven community traction", key="popularity")

        with st.container(border=True):
            st.markdown("**Innovation**")
            innovation = st.toggle("Favor more recent or cutting-edge repos", key="innovation")

        with st.container(border=True):
            st.markdown("**Language Filters**")
            language = st.selectbox("Preferred language", LANGUAGE_OPTIONS, key="language")

    return {
        "max_results": max_results,
        "top_n": top_n,
        "difficulty": difficulty,
        "topic": topic,
        "tutorial_required": tutorial_required,
        "popularity": popularity,
        "innovation": innovation,
        "language": language,
    }


def _render_hero(controls: Dict[str, Any]) -> bool:
    composed_query = compose_search_query(st.session_state.query, controls)
    safe_query = html.escape(composed_query or "Add a learning goal to generate a high-signal search prompt.")
    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="hero-grid">
                <div>
                    <div class="hero-kicker">AI learning discovery workspace</div>
                    <div class="hero-title">Find the right GitHub project to learn from.</div>
                    <div class="hero-subtitle">
                        Search repositories like a premium developer platform: describe your goal in natural language,
                        layer in learning preferences, and surface projects with the strongest tutorial signals and community health.
                    </div>
                </div>
                <div class="hero-panel">
                    <strong style="color:#f8fafc;">Composed search intent</strong>
                    <p style="color:#cbd5e1; line-height:1.55; margin:0.55rem 0 0 0;">{safe_query}</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_search_shell(composed_query)
    with st.form("hero_search_form", clear_on_submit=False):
        query = st.text_input(
            "Search query",
            value=st.session_state.query,
            placeholder="Try: popular Python agent repos with free YouTube tutorials",
        )
        search_clicked = st.form_submit_button("Search Repositories", type="primary", use_container_width=True)
        if search_clicked:
            st.session_state.query = query

    chip_cols = st.columns(len(SUGGESTION_CHIPS))
    for idx, chip in enumerate(SUGGESTION_CHIPS):
        with chip_cols[idx]:
            if st.button(chip, use_container_width=True, key=f"chip_{chip}"):
                if chip.lower() not in st.session_state.query.lower():
                    st.session_state.query = f"{st.session_state.query} {chip}".strip()
                st.rerun()

    st.caption("Suggestion chips keep prompt building fast while the sidebar refines intent and ranking behavior.")
    return search_clicked


def _run_search(controls: Dict[str, Any]) -> None:
    composed_query = compose_search_query(st.session_state.query, controls)
    st.session_state.last_query = composed_query
    render_loading_skeleton(count=4)
    with st.spinner("Scanning GitHub, parsing READMEs, and assembling ranked learning paths..."):
        service = SmartDevAgentService()
        result = service.search(
            query=composed_query,
            max_results=int(controls["max_results"]),
            top_n=int(controls["top_n"]),
        )
    st.session_state.last_result = result


def _render_filters_section() -> Dict[str, Any]:
    with st.container(border=True):
        render_section_header(
            "Filters",
            "Refine the current result set without rerunning the backend search.",
            "Client-side narrowing",
        )
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            min_score = st.slider("Minimum match score", 0, 100, value=st.session_state.min_score, key="min_score")
        with col_2:
            active_only = st.toggle("Only active repositories", key="active_only")
        with col_3:
            tutorial_only = st.toggle("Only tutorial-ready repositories", key="tutorial_only")

    return {
        "min_score": min_score,
        "active_only": active_only,
        "tutorial_only": tutorial_only,
    }


def _render_stats(repositories: List[Dict[str, Any]]) -> None:
    tutorial_count = sum(1 for repo in repositories if repo.get("has_tutorial"))
    active_count = sum(1 for repo in repositories if repo.get("activity_status") == "active")
    avg_score = sum(float(repo.get("score", 0.0)) for repo in repositories) / len(repositories)

    stat_1, stat_2, stat_3, stat_4 = st.columns(4)
    with stat_1:
        render_metric_card("repo", "Repositories Shown", str(len(repositories)), "Tuned for your current discovery brief.")
    with stat_2:
        render_metric_card("tutorial", "Tutorial Signal", str(tutorial_count), "Repositories with tutorial coverage detected in the README.")
    with stat_3:
        render_metric_card("chart", "Average Match Score", f"{avg_score:.1f}", "Normalized ranking confidence across the visible result set.")
    with stat_4:
        render_metric_card("pulse", "Active Repositories", str(active_count), "Projects still showing recent development momentum.")


def _render_results(result: SearchResult) -> None:
    filters = _render_filters_section()
    filtered_repositories = filter_repositories(
        repositories=result.repositories,
        min_score=int(filters["min_score"]),
        active_only=bool(filters["active_only"]),
        tutorial_only=bool(filters["tutorial_only"]),
    )

    active_pills = active_filter_pills(
        {
            **result.preferences,
            "minimum_score": filters["min_score"] if filters["min_score"] > 0 else None,
            "active_only": filters["active_only"],
            "tutorial_only": filters["tutorial_only"],
        }
    )

    with st.container(border=True):
        render_section_header(
            "Discovery Snapshot",
            "A recruiter-ready view of what the AI search engine considered most promising.",
            f"{len(filtered_repositories)} visible results",
        )
        if active_pills:
            pill_markup = "".join(f'<div class="filter-pill">{html.escape(pill)}</div>' for pill in active_pills[:8])
            st.markdown(f'<div class="filter-strip">{pill_markup}</div>', unsafe_allow_html=True)

    if not filtered_repositories:
        render_warning_state(
            "No repositories match the current view filters",
            "Broaden the minimum score, include non-active repositories, or allow projects without built-in tutorials.",
        )
        return

    _render_stats(filtered_repositories)

    overview_tab, cards_tab = st.tabs(["Platform Overview", "Repository Grid"])
    with overview_tab:
        with st.container(border=True):
            render_section_header(
                "Overview Table",
                "Scan the ranked set quickly, then jump into the richer repository cards.",
            )
            st.dataframe(result_table(filtered_repositories), use_container_width=True, hide_index=True)

    with cards_tab:
        cols = st.columns(2)
        for idx, repo in enumerate(filtered_repositories, start=1):
            with cols[(idx - 1) % 2]:
                render_repo_card(repo, position=idx)


def main() -> None:
    _init_state()
    apply_global_styles()
    controls = _sidebar_controls()
    render_topbar(st.session_state.last_query or None)

    search_clicked = _render_hero(controls)
    if search_clicked:
        _run_search(controls)

    result: SearchResult | None = st.session_state.last_result
    if result and result.errors:
        for error in result.errors[:6]:
            st.warning(error)

    if not result:
        render_empty_state(
            "A polished AI search workspace is ready",
            "Start with a natural-language search, add product-style filters in the sidebar, and the platform will assemble a ranked learning shortlist from GitHub.",
        )
        return

    if not result.repositories:
        render_warning_state(
            "No repositories were found for this search",
            "Try a broader topic, remove strict tutorial language, or switch off popularity and innovation constraints for a wider candidate pool.",
        )
        return

    _render_results(result)


if __name__ == "__main__":
    main()
