"""
Reusable UI helpers for the Streamlit frontend.
"""

from __future__ import annotations

import html
import math
import textwrap
from typing import Any, Dict, Iterable, List

import pandas as pd
import streamlit as st


SUGGESTION_CHIPS = ["AI", "NLP", "Beginner", "Python", "LLMs", "Data Science"]
TOPIC_OPTIONS = [
    "Any",
    "AI",
    "NLP",
    "Machine Learning",
    "Deep Learning",
    "Computer Vision",
    "Data Science",
    "Web Scraping",
    "LLM",
    "Agent",
    "Chatbot",
    "Automation",
]
DIFFICULTY_OPTIONS = ["Any", "Beginner", "Intermediate", "Advanced"]
LANGUAGE_OPTIONS = ["Any", "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust", "C++", "C#"]


def apply_global_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg-primary: #0f172a;
            --bg-card: #111827;
            --bg-elevated: rgba(17, 24, 39, 0.94);
            --bg-soft: rgba(15, 23, 42, 0.82);
            --border: #1f2937;
            --border-strong: rgba(99, 102, 241, 0.38);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --primary: #6366f1;
            --accent: #8b5cf6;
            --success: #22c55e;
            --warning: #f59e0b;
            --surface-glow: 0 0 0 1px rgba(99, 102, 241, 0.08), 0 18px 38px rgba(2, 6, 23, 0.42);
            --shadow-lg: 0 22px 70px rgba(2, 6, 23, 0.46);
            --shadow-md: 0 14px 36px rgba(2, 6, 23, 0.32);
            --shadow-sm: 0 10px 24px rgba(2, 6, 23, 0.22);
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(99, 102, 241, 0.15), transparent 28%),
                radial-gradient(circle at top right, rgba(139, 92, 246, 0.11), transparent 24%),
                radial-gradient(circle at bottom center, rgba(56, 189, 248, 0.07), transparent 30%),
                linear-gradient(180deg, #050816 0%, #0a1020 32%, #0f172a 100%);
            color: var(--text-primary);
        }

        [data-testid="stHeader"] {
            background: rgba(5, 8, 22, 0.48);
            backdrop-filter: blur(14px);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 0.95rem;
            padding-bottom: 1.6rem;
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(10, 16, 32, 0.98), rgba(17, 24, 39, 0.98));
            border-right: 1px solid rgba(31, 41, 55, 0.96);
        }

        [data-testid="stSidebarContent"] {
            padding-top: 0.6rem;
        }

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {
            color: var(--text-secondary);
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            gap: 0.55rem;
        }

        [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(180deg, rgba(17, 24, 39, 0.9), rgba(15, 23, 42, 0.86));
            border: 1px solid rgba(42, 51, 66, 0.92);
            border-radius: 18px;
            box-shadow: var(--shadow-sm);
            padding: 0.1rem;
        }

        [data-testid="stSidebar"] h3 {
            font-size: 0.96rem;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] > div,
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stTextArea textarea,
        .stSelectbox > div > div,
        .stMultiSelect > div > div {
            background: rgba(17, 24, 39, 0.94) !important;
            color: var(--text-primary) !important;
            border: 1px solid #2a3342 !important;
            border-radius: 16px !important;
            box-shadow: none !important;
        }

        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea,
        .stSelectbox input,
        .stMultiSelect input {
            color: var(--text-primary) !important;
            caret-color: var(--text-primary) !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #6b7280 !important;
        }

        .stTextInput > div > div:focus-within,
        .stTextArea textarea:focus,
        div[data-baseweb="select"] > div:focus-within {
            border-color: rgba(99, 102, 241, 0.72) !important;
            box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.22), 0 0 0 6px rgba(99, 102, 241, 0.08) !important;
        }

        div[data-baseweb="select"] svg,
        .stSelectbox svg {
            fill: #94a3b8 !important;
        }

        .stSlider [data-baseweb="slider"] {
            padding-top: 0.15rem;
            padding-bottom: 0.15rem;
        }

        .stSlider [role="slider"] {
            background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
            border: 2px solid rgba(248, 250, 252, 0.8) !important;
            box-shadow: 0 0 0 6px rgba(99, 102, 241, 0.1);
        }

        .stSlider [data-baseweb="slider"] > div > div {
            background: rgba(99, 102, 241, 0.26) !important;
        }

        .stToggle label[data-baseweb="checkbox"] > div:first-child {
            background: rgba(30, 41, 59, 0.9) !important;
            border: 1px solid #2a3342 !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stLinkButton"] a {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.98), rgba(139, 92, 246, 0.92)) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(129, 140, 248, 0.38) !important;
            border-radius: 15px !important;
            box-shadow: 0 10px 26px rgba(79, 70, 229, 0.22) !important;
            transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="stLinkButton"] a:hover {
            transform: translateY(-1px) scale(1.01);
            box-shadow: 0 14px 30px rgba(79, 70, 229, 0.3) !important;
            border-color: rgba(165, 180, 252, 0.46) !important;
        }

        .stButton > button[kind="secondary"],
        .stButton > button:disabled {
            background: rgba(17, 24, 39, 0.84) !important;
            color: #94a3b8 !important;
            border: 1px solid #2a3342 !important;
            box-shadow: none !important;
        }

        .topbar {
            position: sticky;
            top: 0.45rem;
            z-index: 40;
            margin-bottom: 0.9rem;
            padding: 0.72rem 0.88rem;
            border: 1px solid rgba(31, 41, 55, 0.98);
            border-radius: 18px;
            background: rgba(10, 16, 32, 0.76);
            backdrop-filter: blur(20px);
            box-shadow: var(--shadow-md);
        }

        .topbar-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.85rem;
            flex-wrap: wrap;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .brand-mark {
            width: 40px;
            height: 40px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 1), rgba(139, 92, 246, 0.88));
            box-shadow: 0 10px 26px rgba(99, 102, 241, 0.34);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }

        .brand-copy h1 {
            margin: 0;
            font-size: 0.98rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .brand-copy p {
            margin: 0.16rem 0 0 0;
            color: var(--text-muted);
            font-size: 0.8rem;
        }

        .status-pills {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.72rem;
            border-radius: 999px;
            border: 1px solid rgba(42, 51, 66, 0.96);
            background: rgba(17, 24, 39, 0.86);
            color: var(--text-secondary);
            font-size: 0.78rem;
            font-weight: 600;
        }

        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #22c55e;
            box-shadow: 0 0 12px rgba(34, 197, 94, 0.44);
        }

        .hero-shell {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(31, 41, 55, 0.98);
            border-radius: 26px;
            background:
                linear-gradient(150deg, rgba(17, 24, 39, 0.95), rgba(15, 23, 42, 0.9)),
                linear-gradient(145deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.08));
            box-shadow: var(--shadow-lg);
            padding: 1.2rem 1.2rem 1.1rem 1.2rem;
            margin-bottom: 0.78rem;
        }

        .hero-shell::before {
            content: "";
            position: absolute;
            inset: -34% auto auto -8%;
            width: 300px;
            height: 300px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.22), transparent 68%);
            pointer-events: none;
        }

        .hero-shell::after {
            content: "";
            position: absolute;
            right: -4%;
            bottom: -30%;
            width: 260px;
            height: 260px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.1), transparent 68%);
            pointer-events: none;
        }

        .hero-grid {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: minmax(0, 2.5fr) minmax(250px, 1fr);
            gap: 0.95rem;
            align-items: start;
        }

        .hero-kicker {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.4rem 0.66rem;
            border-radius: 999px;
            border: 1px solid rgba(99, 102, 241, 0.24);
            background: rgba(79, 70, 229, 0.14);
            color: #c7d2fe;
            font-size: 0.76rem;
            font-weight: 600;
            margin-bottom: 0.72rem;
        }

        .hero-title {
            font-size: clamp(1.82rem, 3.4vw, 2.9rem);
            line-height: 1.02;
            letter-spacing: -0.05em;
            font-weight: 800;
            color: var(--text-primary);
            margin: 0 0 0.55rem 0;
            max-width: 12ch;
        }

        .hero-subtitle {
            color: var(--text-secondary);
            max-width: 60ch;
            line-height: 1.56;
            font-size: 0.95rem;
            margin: 0;
        }

        .hero-panel,
        .repo-card,
        .metric-card,
        .empty-state,
        .warning-state {
            border: 1px solid rgba(31, 41, 55, 0.98);
            background: rgba(17, 24, 39, 0.82);
            box-shadow: var(--surface-glow);
            backdrop-filter: blur(18px);
        }

        .hero-panel {
            padding: 0.92rem;
            border-radius: 20px;
        }

        .hero-panel strong {
            color: var(--text-primary);
        }

        .search-shell {
            border: 1px solid rgba(42, 51, 66, 0.96);
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(17, 24, 39, 0.88), rgba(15, 23, 42, 0.82));
            box-shadow: var(--surface-glow);
            backdrop-filter: blur(18px);
            padding: 0.78rem;
            margin-bottom: 0.65rem;
        }

        .search-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }

        .search-meta-left {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: var(--text-secondary);
            font-size: 0.88rem;
            font-weight: 600;
        }

        .search-shortcut {
            padding: 0.22rem 0.5rem;
            border-radius: 999px;
            background: rgba(30, 41, 59, 0.78);
            border: 1px solid rgba(42, 51, 66, 0.96);
            color: var(--text-muted);
            font-size: 0.75rem;
            font-weight: 700;
        }

        .search-hint {
            color: var(--text-muted);
            font-size: 0.77rem;
            line-height: 1.5;
            margin-top: 0.25rem;
        }

        .chip-label {
            color: var(--text-muted);
            font-size: 0.78rem;
            font-weight: 600;
            margin: 0.1rem 0 0.48rem 0;
        }

        .section-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.56rem;
        }

        .section-title h3 {
            margin: 0;
            color: var(--text-primary);
            font-size: 0.96rem;
            font-weight: 700;
        }

        .section-title p {
            margin: 0.18rem 0 0 0;
            color: var(--text-muted);
            font-size: 0.8rem;
            line-height: 1.5;
        }

        .metric-card {
            position: relative;
            overflow: hidden;
            border-radius: 20px;
            padding: 0.88rem 0.92rem;
            min-height: 118px;
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
            animation: fadeUp 420ms ease both;
        }

        .metric-card::before,
        .repo-card::before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(145deg, rgba(99, 102, 241, 0.07), transparent 45%, rgba(56, 189, 248, 0.03));
            pointer-events: none;
        }

        .metric-card:hover,
        .repo-card:hover {
            transform: translateY(-3px);
            border-color: rgba(99, 102, 241, 0.42);
            box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.08), 0 18px 38px rgba(79, 70, 229, 0.14);
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.76rem;
            font-weight: 600;
            margin-bottom: 0.38rem;
            position: relative;
            z-index: 1;
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 800;
            color: var(--text-primary);
            letter-spacing: -0.04em;
            margin-bottom: 0.25rem;
            position: relative;
            z-index: 1;
        }

        .metric-footnote {
            color: var(--text-secondary);
            font-size: 0.78rem;
            line-height: 1.45;
            position: relative;
            z-index: 1;
        }

        .metric-icon {
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: rgba(99, 102, 241, 0.14);
            border: 1px solid rgba(99, 102, 241, 0.22);
            color: #c7d2fe;
            margin-bottom: 0.62rem;
            position: relative;
            z-index: 1;
        }

        .metric-icon svg,
        .brand-mark svg,
        .search-meta-left svg {
            width: 18px;
            height: 18px;
            stroke: currentColor;
            stroke-width: 1.9;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        .filter-strip,
        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.48rem;
        }

        .filter-pill,
        .badge {
            padding: 0.4rem 0.72rem;
            border-radius: 999px;
            background: rgba(30, 41, 59, 0.72);
            border: 1px solid rgba(42, 51, 66, 0.96);
            color: var(--text-secondary);
            font-size: 0.76rem;
            font-weight: 600;
        }

        .badge {
            padding: 0.28rem 0.58rem;
        }

        .badge.success {
            border-color: rgba(34, 197, 94, 0.24);
            background: rgba(34, 197, 94, 0.12);
            color: #bbf7d0;
        }

        .badge.warning {
            border-color: rgba(245, 158, 11, 0.24);
            background: rgba(245, 158, 11, 0.12);
            color: #fde68a;
        }

        .repo-card {
            position: relative;
            border-radius: 22px;
            padding: 0.92rem;
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
            animation: fadeUp 440ms ease both;
            margin-bottom: 0.78rem;
        }

        .repo-top {
            display: flex;
            justify-content: space-between;
            gap: 0.9rem;
            align-items: flex-start;
            margin-bottom: 0.74rem;
            position: relative;
            z-index: 1;
        }

        .repo-identity {
            display: flex;
            align-items: flex-start;
            gap: 0.72rem;
        }

        .repo-avatar {
            width: 42px;
            height: 42px;
            min-width: 42px;
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.16));
            border: 1px solid rgba(99, 102, 241, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e2e8f0;
            font-weight: 800;
            font-size: 0.9rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .repo-name {
            color: var(--text-primary);
            font-size: 1.02rem;
            font-weight: 700;
            margin-bottom: 0.22rem;
            word-break: break-word;
        }

        .repo-description {
            color: var(--text-secondary);
            font-size: 0.88rem;
            line-height: 1.52;
            max-width: 50ch;
        }

        .repo-subline {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.42rem;
            margin-top: 0.35rem;
            color: var(--text-muted);
            font-size: 0.76rem;
            font-weight: 600;
        }

        .lang-dot {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            display: inline-block;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.08);
        }

        .score-chip {
            min-width: 94px;
            padding: 0.5rem 0.65rem;
            border-radius: 16px;
            border: 1px solid rgba(99, 102, 241, 0.2);
            background: rgba(79, 70, 229, 0.12);
            text-align: right;
        }

        .score-chip strong {
            display: block;
            color: var(--text-primary);
            font-size: 1.05rem;
        }

        .score-chip span {
            color: #c7d2fe;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .meta-grid,
        .insight-grid {
            display: grid;
            gap: 0.62rem;
            position: relative;
            z-index: 1;
        }

        .meta-grid {
            grid-template-columns: repeat(4, minmax(0, 1fr));
            margin-bottom: 0.74rem;
        }

        .insight-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            margin-bottom: 0.74rem;
        }

        .meta-box,
        .insight-box {
            padding: 0.68rem 0.72rem;
            border-radius: 16px;
            background: rgba(12, 18, 32, 0.64);
            border: 1px solid rgba(42, 51, 66, 0.82);
        }

        .meta-label {
            color: var(--text-muted);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.18rem;
        }

        .meta-value {
            color: var(--text-primary);
            font-size: 0.9rem;
            font-weight: 700;
        }

        .insight-box h4 {
            margin: 0 0 0.42rem 0;
            color: var(--text-primary);
            font-size: 0.88rem;
            font-weight: 700;
        }

        .insight-box p,
        .insight-box li {
            color: var(--text-secondary);
            font-size: 0.8rem;
            line-height: 1.48;
        }

        .insight-box ul {
            margin: 0;
            padding-left: 1.05rem;
        }

        .progress-label {
            display: flex;
            justify-content: space-between;
            gap: 0.75rem;
            color: var(--text-secondary);
            font-size: 0.78rem;
            margin-bottom: 0.26rem;
            position: relative;
            z-index: 1;
        }

        .progress-track {
            width: 100%;
            height: 8px;
            border-radius: 999px;
            background: rgba(30, 41, 59, 0.92);
            overflow: hidden;
            border: 1px solid rgba(42, 51, 66, 0.82);
            margin-bottom: 0.54rem;
            position: relative;
            z-index: 1;
        }

        .progress-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #6366f1, #8b5cf6 58%, #38bdf8);
            box-shadow: 0 0 18px rgba(99, 102, 241, 0.34);
            animation: shimmerGrow 900ms ease both;
        }

        .empty-state,
        .warning-state {
            border-radius: 24px;
            padding: 1.7rem 1.3rem;
            text-align: center;
        }

        .empty-state h2,
        .warning-state h2 {
            color: var(--text-primary);
            margin-bottom: 0.35rem;
            font-size: 1.22rem;
        }

        .empty-state p,
        .warning-state p {
            color: var(--text-secondary);
            max-width: 38rem;
            margin: 0 auto;
            line-height: 1.55;
            font-size: 0.92rem;
        }

        .loading-stack {
            display: grid;
            gap: 0.6rem;
            margin-bottom: 0.75rem;
        }

        .loading-header {
            display: grid;
            gap: 0.22rem;
            margin-bottom: 0.7rem;
        }

        .loading-title {
            color: var(--text-primary);
            font-size: 1rem;
            font-weight: 700;
        }

        .loading-subtitle {
            color: var(--text-muted);
            font-size: 0.82rem;
            line-height: 1.5;
            max-width: 60ch;
        }

        .loading-line {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            color: var(--text-secondary);
            font-size: 0.82rem;
            font-weight: 600;
        }

        .loading-pulse {
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            box-shadow: 0 0 16px rgba(99, 102, 241, 0.4);
            animation: pulse 1.4s ease-in-out infinite;
        }

        .skeleton-card {
            min-height: 208px;
            border-radius: 22px;
            border: 1px solid rgba(42, 51, 66, 0.9);
            background: linear-gradient(110deg, rgba(17, 24, 39, 0.98) 8%, rgba(28, 37, 54, 0.96) 18%, rgba(17, 24, 39, 0.98) 33%);
            background-size: 200% 100%;
            animation: shimmer 1.45s linear infinite;
            box-shadow: var(--shadow-sm);
            margin-bottom: 0.78rem;
            padding: 0.95rem;
            display: grid;
            gap: 0.72rem;
        }

        .skeleton-row {
            display: flex;
            align-items: center;
            gap: 0.72rem;
        }

        .skeleton-avatar {
            width: 42px;
            height: 42px;
            border-radius: 14px;
            background: rgba(51, 65, 85, 0.7);
        }

        .skeleton-copy {
            flex: 1;
            display: grid;
            gap: 0.35rem;
        }

        .skeleton-line {
            height: 10px;
            border-radius: 999px;
            background: rgba(51, 65, 85, 0.7);
        }

        .skeleton-line.title {
            width: 58%;
            height: 12px;
        }

        .skeleton-line.short {
            width: 34%;
        }

        .skeleton-line.medium {
            width: 72%;
        }

        .skeleton-line.long {
            width: 88%;
        }

        .skeleton-badges {
            display: flex;
            gap: 0.45rem;
            flex-wrap: wrap;
        }

        .skeleton-badge {
            width: 72px;
            height: 26px;
            border-radius: 999px;
            background: rgba(51, 65, 85, 0.68);
        }

        .skeleton-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.55rem;
        }

        .skeleton-metric {
            height: 48px;
            border-radius: 14px;
            background: rgba(30, 41, 59, 0.76);
        }

        .skeleton-progress {
            display: grid;
            gap: 0.3rem;
        }

        .skeleton-track {
            width: 100%;
            height: 8px;
            border-radius: 999px;
            background: rgba(30, 41, 59, 0.88);
        }

        .skeleton-fill {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.75), rgba(139, 92, 246, 0.52));
        }

        .skeleton-actions {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
        }

        .skeleton-action {
            height: 34px;
            border-radius: 12px;
            background: rgba(51, 65, 85, 0.72);
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.55rem;
            background: rgba(15, 23, 42, 0.62);
            border: 1px solid rgba(31, 41, 55, 0.98);
            border-radius: 16px;
            padding: 0.28rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: auto;
            padding: 0.52rem 0.9rem;
            border-radius: 12px;
            color: var(--text-muted);
        }

        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.16) !important;
            color: var(--text-primary) !important;
        }

        .stExpander {
            border: 1px solid rgba(31, 41, 55, 0.92) !important;
            border-radius: 16px !important;
            background: rgba(15, 23, 42, 0.56) !important;
        }

        @media (max-width: 1080px) {
            .hero-grid,
            .meta-grid,
            .insight-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .block-container {
                padding-top: 0.85rem;
            }

            .hero-shell {
                padding: 1rem;
            }

            .hero-title {
                font-size: 2rem;
            }
        }

        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        @keyframes fadeUp {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        @keyframes shimmerGrow {
            0% { width: 0%; opacity: 0.65; }
            100% { opacity: 1; }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(0.9); opacity: 0.72; }
            50% { transform: scale(1.15); opacity: 1; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _icon_svg(name: str) -> str:
    icons = {
        "brand": '<svg viewBox="0 0 24 24"><path d="M12 3l7 4v10l-7 4-7-4V7l7-4Z"/><path d="M9 10l3-2 3 2v4l-3 2-3-2v-4Z"/></svg>',
        "search": '<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
        "repo": '<svg viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15.5A2.5 2.5 0 0 0 17.5 16H4z"/><path d="M6 3v13"/></svg>',
        "tutorial": '<svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 17A2.5 2.5 0 0 0 4 19.5V6a2.5 2.5 0 0 1 2.5-2.5H20v13.5"/><path d="m10 8 5 3-5 3Z"/></svg>',
        "chart": '<svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
        "pulse": '<svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 7-4-14-3 7H2"/></svg>',
        "sparkles": '<svg viewBox="0 0 24 24"><path d="m12 3 1.7 4.3L18 9l-4.3 1.7L12 15l-1.7-4.3L6 9l4.3-1.7Z"/><path d="M5 19l.8 2 .8-2 2-.8-2-.8-.8-2-.8 2-2 .8 2 .8Z"/><path d="M19 16l.8 2 .8-2 2-.8-2-.8-.8-2-.8 2-2 .8 2 .8Z"/></svg>',
        "star": '<svg viewBox="0 0 24 24"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.2 6.4 20.2l1.1-6.2L3 9.6l6.2-.9Z"/></svg>',
    }
    return icons.get(name, icons["sparkles"])


def _language_color(language: str) -> str:
    colors = {
        "Python": "#3572A5",
        "JavaScript": "#f1e05a",
        "TypeScript": "#3178c6",
        "Java": "#b07219",
        "Go": "#00ADD8",
        "Rust": "#dea584",
        "C++": "#f34b7d",
        "C#": "#178600",
    }
    return colors.get(language, "#94a3b8")


def _repo_initials(repo_name: str) -> str:
    chunks = [part for part in repo_name.replace("_", "-").split("-") if part]
    if not chunks:
        return "GH"
    if len(chunks) == 1:
        return chunks[0][:2].upper()
    return (chunks[0][:1] + chunks[1][:1]).upper()


def render_topbar(last_query: str | None) -> None:
    query_text = html.escape(last_query) if last_query else "Awaiting your first search"
    st.markdown(
        f"""
        <div class="topbar">
            <div class="topbar-row">
                <div class="brand">
                    <div class="brand-mark">{_icon_svg("brand")}</div>
                    <div class="brand-copy">
                        <h1>Smart Developer Repo Agent</h1>
                        <p>AI-powered GitHub learning discovery platform</p>
                    </div>
                </div>
                <div class="status-pills">
                    <div class="status-pill"><span class="status-dot"></span>AI ranking active</div>
                    <div class="status-pill"><span class="status-dot"></span>Tutorial engine online</div>
                    <div class="status-pill"><span class="status-dot"></span>Query: {query_text}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str, pill: str | None = None) -> None:
    extra = f'<div class="filter-pill">{html.escape(pill)}</div>' if pill else ""
    st.markdown(
        f"""
        <div class="section-title">
            <div>
                <h3>{html.escape(title)}</h3>
                <p>{html.escape(subtitle)}</p>
            </div>
            {extra}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(icon: str, label: str, value: str, footnote: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{_icon_svg(icon)}</div>
            <div class="metric-label">{html.escape(label)}</div>
            <div class="metric-value">{html.escape(value)}</div>
            <div class="metric-footnote">{html.escape(footnote)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_skeleton(count: int = 4) -> None:
    st.markdown(
        """
        <div class="loading-header">
            <div class="loading-title">Building your GitHub learning shortlist</div>
            <div class="loading-subtitle">
                The app is searching repositories, checking README quality, detecting tutorials,
                and ranking which projects are the best fit for your learning goals.
            </div>
        </div>
        <div class="loading-stack">
            <div class="loading-line"><span class="loading-pulse"></span>Analyzing repositories...</div>
            <div class="loading-line"><span class="loading-pulse"></span>Extracting tutorials...</div>
            <div class="loading-line"><span class="loading-pulse"></span>Ranking learning quality...</div>
            <div class="loading-line"><span class="loading-pulse"></span>Generating recommendations...</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for idx in range(count):
        with cols[idx % 2]:
            st.markdown(
                """
                <div class="skeleton-card">
                    <div class="skeleton-row">
                        <div class="skeleton-avatar"></div>
                        <div class="skeleton-copy">
                            <div class="skeleton-line title"></div>
                            <div class="skeleton-line short"></div>
                        </div>
                    </div>
                    <div class="skeleton-copy">
                        <div class="skeleton-line long"></div>
                        <div class="skeleton-line medium"></div>
                    </div>
                    <div class="skeleton-badges">
                        <div class="skeleton-badge"></div>
                        <div class="skeleton-badge"></div>
                        <div class="skeleton-badge"></div>
                    </div>
                    <div class="skeleton-metrics">
                        <div class="skeleton-metric"></div>
                        <div class="skeleton-metric"></div>
                        <div class="skeleton-metric"></div>
                    </div>
                    <div class="skeleton-progress">
                        <div class="skeleton-track"><div class="skeleton-fill" style="width:74%;"></div></div>
                        <div class="skeleton-track"><div class="skeleton-fill" style="width:61%;"></div></div>
                    </div>
                    <div class="skeleton-actions">
                        <div class="skeleton-action"></div>
                        <div class="skeleton-action"></div>
                        <div class="skeleton-action"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_empty_state(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <h2>{html.escape(title)}</h2>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_warning_state(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="warning-state">
            <h2>{html.escape(title)}</h2>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search_shell(query_preview: str) -> None:
    safe_preview = html.escape(query_preview or "Natural language prompt will appear here as you shape the request.")
    st.markdown(
        f"""
        <div class="search-shell">
            <div class="search-meta">
                <div class="search-meta-left">{_icon_svg("search")} Search the learning graph</div>
                <div class="search-shortcut">Enter to run</div>
            </div>
            <div class="search-hint">AI-composed prompt: {safe_preview}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def compose_search_query(base_query: str, controls: Dict[str, Any]) -> str:
    tokens: List[str] = []
    cleaned = base_query.strip()
    if cleaned:
        tokens.append(cleaned)

    topic = controls.get("topic", "Any")
    if topic and topic != "Any":
        tokens.append(str(topic))

    difficulty = controls.get("difficulty", "Any")
    if difficulty and difficulty != "Any":
        tokens.append(str(difficulty).lower())

    language = controls.get("language", "Any")
    if language and language != "Any":
        tokens.append(str(language))

    if controls.get("tutorial_required"):
        tokens.append("with tutorial")
    if controls.get("popularity"):
        tokens.append("popular")
    if controls.get("innovation"):
        tokens.append("latest innovative")

    seen = set()
    deduped: List[str] = []
    for part in tokens:
        normalized = str(part).strip().lower()
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(str(part).strip())
    return " ".join(deduped).strip()


def active_filter_pills(filters: Dict[str, Any]) -> List[str]:
    pills: List[str] = []
    for key, value in filters.items():
        if value in (None, False, "", "Any"):
            continue
        label = key.replace("_", " ").title()
        pills.append(f"{label}: {value}")
    return pills


def result_table(repositories: Iterable[Dict[str, Any]]) -> pd.DataFrame:
    rows: List[Dict[str, Any]] = []
    for repo in repositories:
        signals = derive_repo_signals(repo)
        rows.append(
            {
                "Repository": repo.get("full_name") or repo.get("name"),
                "Match Score": round(float(repo.get("score", 0.0)), 1),
                "Tutorial Confidence": signals["tutorial_confidence"],
                "Suitability": signals["suitability_label"],
                "Health": signals["health_label"],
                "Language": repo.get("language", "Unknown"),
                "Difficulty": signals["difficulty_summary"],
                "Stars": int(repo.get("stars", 0)),
                "Activity": repo.get("activity_status", "unknown"),
            }
        )
    return pd.DataFrame(rows)


def derive_repo_signals(repo: Dict[str, Any]) -> Dict[str, Any]:
    stars = float(repo.get("stars", 0))
    contributors = float(repo.get("contributors", 0))
    readme_length = float(repo.get("readme_length", 0))
    has_tutorial = bool(repo.get("has_tutorial"))
    tutorial_links = len(repo.get("tutorial_links", []))
    youtube_links = len(repo.get("youtube_tutorial_links", [])) + len(repo.get("youtube_suggestions", []))
    technologies = len(repo.get("technologies", []))
    activity_status = str(repo.get("activity_status", "unknown"))
    score = float(repo.get("score", 0.0))

    tutorial_confidence_score = min(
        100.0,
        (36 if has_tutorial else 0)
        + min(tutorial_links * 18, 36)
        + min(youtube_links * 10, 20)
        + min(readme_length / 120, 18),
    )

    health_score = min(
        100.0,
        min(math.log1p(stars) * 16, 44)
        + min(math.log1p(contributors) * 10, 18)
        + min(technologies * 3.5, 14)
        + (24 if activity_status == "active" else 12 if activity_status == "moderately active" else 3),
    )

    suitability_score = min(100.0, (score * 0.55) + (tutorial_confidence_score * 0.25) + (health_score * 0.2))

    reasons: List[str] = []
    if repo.get("difficulty") == "Beginner":
        reasons.append("Strong beginner onboarding")
    if readme_length >= 1800:
        reasons.append("Detailed README guidance")
    if activity_status == "active":
        reasons.append("Active maintainer ecosystem")
    if has_tutorial or tutorial_links > 0:
        reasons.append("High tutorial confidence")
    if stars >= 500:
        reasons.append("Healthy community traction")
    if technologies >= 4:
        reasons.append("Good first-project candidate")
    if not reasons:
        reasons.append("Relevant match for the query")

    tutorial_confidence = "High" if tutorial_confidence_score >= 75 else "Medium" if tutorial_confidence_score >= 45 else "Low"
    health_label = "Excellent" if health_score >= 75 else "Good" if health_score >= 50 else "Developing"
    suitability_label = "High fit" if suitability_score >= 75 else "Promising" if suitability_score >= 50 else "Exploratory"

    difficulty_label = str(repo.get("difficulty", "Unknown"))
    if difficulty_label == "Beginner":
        difficulty_summary = "Low lift"
    elif difficulty_label == "Intermediate":
        difficulty_summary = "Moderate ramp"
    elif difficulty_label == "Advanced":
        difficulty_summary = "Higher commitment"
    else:
        difficulty_summary = "Unclear"

    return {
        "tutorial_confidence_score": tutorial_confidence_score,
        "tutorial_confidence": tutorial_confidence,
        "health_score": health_score,
        "health_label": health_label,
        "difficulty_summary": difficulty_summary,
        "reasons": reasons[:4],
        "suitability_score": suitability_score,
        "suitability_label": suitability_label,
    }


def filter_repositories(repositories: List[Dict[str, Any]], min_score: int, active_only: bool, tutorial_only: bool) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for repo in repositories:
        if float(repo.get("score", 0.0)) < min_score:
            continue
        if active_only and repo.get("activity_status") != "active":
            continue
        if tutorial_only and not repo.get("has_tutorial"):
            continue
        filtered.append(repo)
    return filtered


def render_repo_card(repo: Dict[str, Any], position: int) -> None:
    signals = derive_repo_signals(repo)
    repo_name = str(repo.get("full_name") or repo.get("name", "Unknown repository"))
    description = textwrap.shorten(str(repo.get("description", "No description provided.")), width=185, placeholder="...")
    repo_short_name = str(repo.get("name", "repo"))
    initials = _repo_initials(repo_short_name)
    language = str(repo.get("language", "Unknown"))
    language_color = _language_color(language)
    technologies = [str(item) for item in repo.get("technologies", [])][:5]
    tutorial_links = [str(link) for link in repo.get("tutorial_links", [])]
    youtube_links = [str(link) for link in repo.get("youtube_tutorial_links", [])]
    youtube_suggestions = [str(link) for link in repo.get("youtube_suggestions", [])]
    first_tutorial = tutorial_links[0] if tutorial_links else None
    first_video = youtube_links[0] if youtube_links else youtube_suggestions[0] if youtube_suggestions else None

    badge_items = [
        f'<span class="badge"><span class="lang-dot" style="background:{language_color};"></span> {html.escape(language)}</span>',
        f'<span class="badge">{html.escape(str(repo.get("difficulty", "Unknown")))}</span>',
        f'<span class="badge">{html.escape(signals["suitability_label"])}</span>',
        '<span class="badge success">Tutorial ready</span>' if repo.get("has_tutorial") else '<span class="badge warning">Tutorial needed</span>',
    ]
    for tech in technologies:
        badge_items.append(f'<span class="badge">{html.escape(tech)}</span>')

    reasons_html = "".join(f"<li>{html.escape(reason)}</li>" for reason in signals["reasons"])
    st.markdown(
        f"""
        <div class="repo-card">
            <div class="repo-top">
                <div class="repo-identity">
                    <div class="repo-avatar">{html.escape(initials)}</div>
                    <div>
                        <div class="repo-name">#{position} {html.escape(repo_name)}</div>
                        <div class="repo-description">{html.escape(description)}</div>
                        <div class="repo-subline">
                            <span class="lang-dot" style="background:{language_color};"></span>
                            <span>{html.escape(language)}</span>
                            <span>•</span>
                            <span>{int(repo.get("stars", 0))} stars</span>
                            <span>•</span>
                            <span>{html.escape(str(repo.get("activity_status", "unknown")).title())}</span>
                        </div>
                    </div>
                </div>
                <div class="score-chip">
                    <span>Match score</span>
                    <strong>{float(repo.get("score", 0.0)):.1f}</strong>
                </div>
            </div>
            <div class="meta-grid">
                <div class="meta-box">
                    <div class="meta-label">Stars</div>
                    <div class="meta-value">{int(repo.get("stars", 0))}</div>
                </div>
                <div class="meta-box">
                    <div class="meta-label">Forks</div>
                    <div class="meta-value">{int(repo.get("forks", 0))}</div>
                </div>
                <div class="meta-box">
                    <div class="meta-label">Contributors</div>
                    <div class="meta-value">{int(repo.get("contributors", 0))}</div>
                </div>
                <div class="meta-box">
                    <div class="meta-label">Health</div>
                    <div class="meta-value">{html.escape(signals["health_label"])}</div>
                </div>
            </div>
            <div class="badge-row">
                {''.join(badge_items)}
            </div>
            <div class="insight-grid">
                <div class="insight-box">
                    <h4>Why Recommended</h4>
                    <ul>{reasons_html}</ul>
                </div>
                <div class="insight-box">
                    <h4>Learning Snapshot</h4>
                    <p>Estimated difficulty: {html.escape(signals["difficulty_summary"])}</p>
                    <p>Tutorial confidence: {html.escape(signals["tutorial_confidence"])}</p>
                    <p>Suitability analysis: {html.escape(signals["suitability_label"])}</p>
                </div>
            </div>
            <div class="progress-label"><span>Match score visualization</span><span>{float(repo.get("score", 0.0)):.1f}%</span></div>
            <div class="progress-track"><div class="progress-fill" style="width:{max(4.0, min(float(repo.get("score", 0.0)), 100.0)):.1f}%;"></div></div>
            <div class="progress-label"><span>Tutorial confidence score</span><span>{signals["tutorial_confidence_score"]:.0f}%</span></div>
            <div class="progress-track"><div class="progress-fill" style="width:{max(4.0, signals["tutorial_confidence_score"]):.1f}%;"></div></div>
            <div class="progress-label"><span>Repository health indicator</span><span>{signals["health_score"]:.0f}%</span></div>
            <div class="progress-track"><div class="progress-fill" style="width:{max(4.0, signals["health_score"]):.1f}%;"></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    action_1, action_2, action_3 = st.columns(3)
    with action_1:
        st.link_button("Open Repository", str(repo.get("html_url", "#")), use_container_width=True)
    with action_2:
        if first_tutorial:
            st.link_button("View Tutorials", first_tutorial, use_container_width=True)
        else:
            st.button("View Tutorials", disabled=True, use_container_width=True, key=f"tutorial_{position}")
    with action_3:
        if first_video:
            st.link_button("Watch Tutorials", first_video, use_container_width=True)
        else:
            st.button("Watch Tutorials", disabled=True, use_container_width=True, key=f"youtube_{position}")

    if tutorial_links or youtube_links or youtube_suggestions:
        with st.expander("Learning resources", expanded=False):
            if tutorial_links:
                st.markdown("**Repository tutorial links**")
                for link in tutorial_links[:5]:
                    st.markdown(f"- {link}")
            if youtube_links:
                st.markdown("**YouTube links found in README**")
                for link in youtube_links[:4]:
                    st.markdown(f"- {link}")
            if youtube_suggestions:
                st.markdown("**Suggested YouTube tutorials**")
                for link in youtube_suggestions[:4]:
                    st.markdown(f"- {link}")
    else:
        st.caption("No tutorial or YouTube links surfaced for this repository yet.")
