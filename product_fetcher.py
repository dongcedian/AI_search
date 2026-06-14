"""Fetch product announcements from official company blogs/sites."""

import logging
import re
from datetime import datetime, timedelta, timezone

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# ── Product launch detection keywords ──

_LAUNCH_EN = [
    "launch", "released", "announcing", "introducing", "new model",
    "now available", "unveil", "preview", "roll out", "shipping",
    "here", "meet", "presenting", "general availability", "ga release",
]

_LAUNCH_ZH = [
    "发布", "推出", "上线", "正式开放", "新版本", "升级", "首发",
    "全新", "来了", "开源", "公测", "内测", "更新",
]

# ── Feature extraction keywords ──

_FEATURE_EN = [
    "support", "capable of", "features", "can now", "powered by",
    "trained on", "context window", "tokens", "benchmark", "accuracy",
    "outperforms", "generation", "multimodal", "vision", "audio",
]

_FEATURE_ZH = [
    "支持", "功能", "特性", "参数", "上下文", "能力", "性能",
    "评测", "推理", "训练", "生成", "多模态", "识别",
]


def _is_product_post(title, summary=""):
    """Check if a blog post title looks like a product launch announcement."""
    text = f"{title} {summary}".lower()
    for kw in _LAUNCH_EN:
        if kw in text:
            return True
    for kw in _LAUNCH_ZH:
        if kw in text:
            return True
    return False


def _extract_features(text):
    """Extract feature-like sentences from description text."""
    features = []
    sentences = re.split(r"[.。!！;；\n]", text)
    en_keywords = set(_FEATURE_EN)
    zh_keywords = set(_FEATURE_ZH)
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 15 or len(sent) > 300:
            continue
        if any(kw in sent.lower() for kw in en_keywords):
            features.append(sent)
        elif any(kw in sent for kw in zh_keywords):
            features.append(sent)
    return features[:5]


def _fetch_rss(source):
    """Try RSS feed, return list of post dicts."""
    logger.info("  Trying RSS: %s", source["rss"])
    try:
        feed = feedparser.parse(source["rss"])
    except Exception as e:
        logger.warning("  RSS parse error: %s", e)
        return []

    posts = []
    for entry in feed.entries[:20]:
        title = getattr(entry, "title", "").strip()
        summary = getattr(entry, "summary", "")
        if hasattr(entry, "content"):
            summary = getattr(entry.content[0], "value", summary) if entry.content else summary
        link = getattr(entry, "link", "")
        published = getattr(entry, "published", "")

        if not _is_product_post(title, summary):
            continue

        posts.append({
            "title": title,
            "link": link,
            "summary": _clean_text(summary)[:400],
            "published": published,
        })
    return posts


def _scrape_blog(source):
    """Scrape a blog index page for recent posts, return list of post dicts."""
    url = source["blog"]
    logger.info("  Scraping blog: %s", url)
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp.raise_for_status()
    except Exception as e:
        logger.warning("  Failed to fetch %s: %s", url, e)
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    posts = []
    seen_links = set()

    # Look for article-like elements with headings containing links
    for tag in soup.find_all(["article", "h1", "h2", "h3"]):
        # Find the main heading link
        link_tag = tag.find("a", href=True)
        if not link_tag:
            continue

        # Get the text from the heading/title element specifically, not the whole tag
        title_tag = tag.find(["h1", "h2", "h3"])
        if title_tag:
            title = title_tag.get_text(strip=True)
        else:
            title = link_tag.get_text(strip=True)

        # If link text is generic ("Learn more", "Read more"), try parent text
        if title.lower() in ("learn more", "read more", "view more", "more", "click here", ""):
            parent_text = tag.get_text(strip=True)
            if len(parent_text) > len(title) + 5:
                title = parent_text

        href = link_tag["href"]
        if not title or len(title) < 10 or len(title) > 250:
            continue
        if href in seen_links:
            continue
        seen_links.add(href)

        # Skip non-content links
        if any(skip in href.lower() for skip in ["/category/", "/tag/", "#", "twitter.com", "linkedin.com"]):
            continue

        # Make relative URLs absolute
        if href.startswith("/"):
            from urllib.parse import urljoin
            href = urljoin(url, href)

        # Extract date from <time> tag
        time_tag = tag.find("time")
        date_text = ""
        if time_tag:
            dt = time_tag.get("datetime", "")
            date_text = dt if dt else time_tag.get_text(strip=True)

        # Extract description
        desc_tag = tag.find(["p"])
        if not desc_tag:
            parent = tag.parent
            desc_tag = parent.find(["p"]) if parent else None
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        if not _is_product_post(title, description):
            continue

        posts.append({
            "title": _clean_title(title),
            "link": href,
            "summary": _clean_text(description)[:400],
            "published": _clean_date(date_text),
        })

        if len(posts) >= 5:
            break

    return posts


def _clean_title(raw_title):
    """Clean up scraped titles — remove date prefixes, category labels, etc."""
    # Remove leading date patterns like "Jun 11, 2026" or "2026-06-11"
    title = re.sub(r'^\w{3,9}\s+\d{1,2},?\s*\d{4}\s*', '', raw_title)
    title = re.sub(r'^\d{4}-\d{2}-\d{2}\s*', '', title)
    # Remove leading category labels (single word followed by title)
    title = re.sub(r'^(Announcements?|Blog|News|Release|Update|Press)\s+', '', title)
    # Collapse whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def _clean_date(raw_date):
    """Normalize date strings."""
    if not raw_date:
        return ""
    # ISO format -> shorten
    if 'T' in raw_date:
        return raw_date[:10]
    # Already clean
    if len(raw_date) < 30:
        return raw_date.strip()
    return raw_date[:25]


def _clean_text(text):
    """Strip HTML tags and normalize whitespace."""
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def _extract_product_name(title, company):
    """Extract product name from title. Heuristic: remove company name, keep key nouns."""
    # Remove common prefixes
    name = title.replace(company, "").strip()
    for prefix in ["Introducing ", "Announcing ", "Presenting ", "Meet ",
                    "发布", "推出", "上线", "开源"]:
        name = name.replace(prefix, "")
    # Take first 60 chars as product identifier
    if len(name) > 60:
        name = name[:57] + "..."
    return name.strip(" :：-–—")


def fetch_products(sources=None, max_age_days=60):
    """Fetch product announcements from all company sources.

    Returns list of dicts:
      {company, product_name, description, features: [str], link, date, lang}
    """
    if sources is None:
        from product_sources import PRODUCT_SOURCES as sources

    all_products = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)

    for src in sources:
        company = src["company"]
        logger.info("Fetching products for %s...", company)

        # Try RSS first, then scrape
        posts = []
        if src.get("rss"):
            posts = _fetch_rss(src)
        if not posts:
            posts = _scrape_blog(src)

        if not posts:
            logger.info("  No product posts found for %s", company)
            continue

        for post in posts[:3]:  # top 3 product posts per company
            product_name = _extract_product_name(post["title"], company)
            features = _extract_features(post.get("summary", ""))
            all_products.append({
                "company": company,
                "product_name": product_name,
                "description": post.get("summary", ""),
                "features": features,
                "link": post.get("link", ""),
                "date": post.get("published", ""),
                "lang": src["lang"],
            })

        logger.info("  %s: %d product post(s)", company, len(posts[:3]))

    logger.info("Total: %d products across %d companies",
                len(all_products),
                len(set(p["company"] for p in all_products)))
    return all_products
