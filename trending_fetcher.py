"""Fetch trending GitHub repos, MCP servers, and Claude Code skills via gh CLI."""

import json
import logging
import subprocess

logger = logging.getLogger(__name__)

GH = "gh"


def _search(query, limit=20, sort="stars"):
    """Run `gh search repos` and return parsed JSON list."""
    cmd = [
        GH, "search", "repos", query,
        "--sort", sort,
        "--limit", str(limit),
        "--json", "name,fullName,url,stargazersCount,description,language",
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace",
        )
        if result.returncode != 0:
            logger.warning("gh search failed: %s", result.stderr.strip())
            return []
        return json.loads(result.stdout)
    except Exception as e:
        logger.warning("gh search error: %s", e)
        return []


def _fmt_repo(r):
    """Normalize repo dict."""
    return {
        "name": r["fullName"],
        "url": r["url"],
        "stars": r["stargazersCount"],
        "description": (r.get("description") or "")[:200],
        "language": r.get("language") or "",
    }


def fetch_trending_repos():
    """Fetch trending AI repos — recently pushed, high stars."""
    logger.info("Fetching trending AI repos...")
    raw = _search("ai OR llm OR machine-learning OR agent pushed:>2026-05-01", limit=30)
    repos = []
    for r in raw:
        if r["stargazersCount"] < 50:
            continue
        repos.append(_fmt_repo(r))
    # Sort by stars desc
    repos.sort(key=lambda r: -r["stars"])
    logger.info("  %d trending repos found", len(repos))
    return repos[:20]


def fetch_mcp_servers():
    """Fetch popular MCP server repos."""
    logger.info("Fetching popular MCP servers...")
    raw = _search("mcp server", limit=25)
    repos = []
    for r in raw:
        name = (r["name"] + " " + (r.get("description") or "")).lower()
        if "mcp" not in name:
            continue
        repos.append(_fmt_repo(r))
    repos.sort(key=lambda r: -r["stars"])
    logger.info("  %d MCP servers found", len(repos))
    return repos[:15]


def fetch_claude_skills():
    """Fetch popular Claude Code skill repos."""
    logger.info("Fetching Claude Code skills...")
    raw = _search("claude code skill", limit=25)
    repos = [_fmt_repo(r) for r in raw if r["stargazersCount"] >= 10]
    repos.sort(key=lambda r: -r["stars"])
    logger.info("  %d skills found", len(repos))
    return repos[:15]


def fetch_all_trending():
    """Fetch all trending data in one call."""
    return {
        "trending": fetch_trending_repos(),
        "mcp": fetch_mcp_servers(),
        "skills": fetch_claude_skills(),
    }
