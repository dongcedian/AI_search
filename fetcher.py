import logging
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher

import feedparser

from classifier import is_ai_related, classify_company

logger = logging.getLogger(__name__)


def _title_similarity(a, b):
    """Return similarity ratio between two titles (0.0 to 1.0)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _is_recent(entry, max_age_hours=48):
    """Check if a feed entry is within max_age_hours of now."""
    now = datetime.now(timezone.utc)
    published = None

    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except (TypeError, ValueError):
            pass

    if published is None and hasattr(entry, "updated_parsed") and entry.updated_parsed:
        try:
            published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
        except (TypeError, ValueError):
            pass

    if published is None:
        # No date available — include it anyway
        return True

    age = now - published
    return age <= timedelta(hours=max_age_hours)


def fetch_all(sources, max_age_hours=48):
    """Fetch articles from all sources, returning a list of article dicts.

    Each dict: {title, link, summary, source, published, lang}
    """
    all_articles = []

    for src in sources:
        name = src["name"]
        url = src["url"]
        lang = src["lang"]
        logger.info("Fetching %s (%s)...", name, url)

        try:
            feed = feedparser.parse(url)
        except Exception as e:
            logger.warning("Failed to fetch %s: %s", name, e)
            continue

        if feed.bozo and not feed.entries:
            logger.warning("Bozo feed for %s: %s", name, feed.bozo_exception)
            continue

        for entry in feed.entries:
            if not _is_recent(entry, max_age_hours):
                continue

            title = getattr(entry, "title", "").strip()
            summary = _clean_summary(getattr(entry, "summary", ""))

            if not is_ai_related(title, summary):
                continue

            article = {
                "title": title or "(no title)",
                "link": getattr(entry, "link", ""),
                "summary": summary,
                "source": name,
                "published": _format_date(entry),
                "lang": lang,
                "company": classify_company(title, summary),
            }
            all_articles.append(article)

    logger.info("Fetched %d AI-related articles before dedup", len(all_articles))
    all_articles = _deduplicate(all_articles)
    logger.info("%d articles after dedup", len(all_articles))
    return all_articles


def _clean_summary(text):
    """Strip HTML tags, keep plain text, limit length."""
    import re
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean[:300]


def _format_date(entry):
    """Extract a human-readable date string from a feed entry."""
    if hasattr(entry, "published") and entry.published:
        return entry.published
    if hasattr(entry, "updated") and entry.updated:
        return entry.updated
    return ""


def _deduplicate(articles, threshold=0.85):
    """Remove articles with very similar titles."""
    seen = []
    for article in articles:
        if any(_title_similarity(article["title"], s["title"]) > threshold for s in seen):
            continue
        seen.append(article)
    return seen
