#!/usr/bin/env python3
"""AI News Daily Aggregator — fetch AI news from RSS feeds, generate HTML digest."""

import argparse
import logging
import os
import sys
import time
from datetime import datetime

from sources import ALL_SOURCES
from fetcher import fetch_all
from unified_generator import generate_unified_page
from product_fetcher import fetch_products

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_once(output_dir="output", max_age_hours=48, fetch_products_flag=False):
    """Fetch news and generate the HTML page once."""
    logger.info("Starting AI News fetch (%d sources)...", len(ALL_SOURCES))
    articles = fetch_all(ALL_SOURCES, max_age_hours=max_age_hours)

    if not articles:
        logger.warning("No articles found.")
        articles = []

    if articles:
        companies = {}
        for a in articles:
            c = a.get("company", "other")
            companies[c] = companies.get(c, 0) + 1
        top_companies = sorted(companies.items(), key=lambda x: -x[1])
        summary = ", ".join(f"{c}({n})" for c, n in top_companies[:8])
        logger.info("%d articles across %d companies: %s", len(articles), len(companies), summary)

    products = []
    if fetch_products_flag:
        logger.info("Fetching product announcements from official sources...")
        products = fetch_products(max_age_days=60)
        if products:
            logger.info("%d products across %d companies",
                        len(products), len(set(p["company"] for p in products)))

    path = generate_unified_page(articles, products, output_dir=output_dir)
    logger.info("Dashboard saved to %s", path)
    return path


def run_daemon(output_dir="output", fetch_time="07:00", max_age_hours=48, fetch_products_flag=False):
    """Run as a background daemon, fetching at the specified time each day."""
    import schedule

    logger.info("Daemon mode: will fetch daily at %s", fetch_time)

    schedule.every().day.at(fetch_time).do(
        lambda: run_once(output_dir, max_age_hours, fetch_products_flag)
    )
    run_once(output_dir, max_age_hours, fetch_products_flag)

    logger.info("Daemon running. Press Ctrl+C to stop.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Daemon stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="AI News Daily Aggregator"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for HTML output (default: output/)",
    )
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run as a background daemon, fetching daily",
    )
    parser.add_argument(
        "--fetch-time",
        default="07:00",
        help="Time to fetch each day in daemon mode (default: 07:00)",
    )
    parser.add_argument(
        "--max-age",
        type=int,
        default=48,
        help="Max article age in hours (default: 48)",
    )
    parser.add_argument(
        "--products",
        action="store_true",
        help="Also fetch product announcements from official company sources",
    )
    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.output_dir, args.fetch_time, args.max_age, args.products)
    else:
        path = run_once(args.output_dir, args.max_age, args.products)
        if path:
            abs_path = os.path.abspath(path)
            print(f"\nDone! Open: file:///{abs_path}")


if __name__ == "__main__":
    main()
