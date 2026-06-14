import os
from datetime import datetime


# Company display order (Western then Chinese)
_COMPANY_ORDER = [
    "OpenAI", "Anthropic", "Google DeepMind", "Meta", "Microsoft",
    "Amazon", "Apple", "Nvidia", "xAI", "Tesla", "Mistral",
    "Stability AI", "Midjourney", "Perplexity", "Cohere",
    "Hugging Face", "Scale AI",
    # Chinese
    "DeepSeek", "百度/文心", "阿里/通义", "字节跳动/豆包",
    "腾讯/混元", "智谱AI", "月之暗面/Kimi", "百川智能",
    "零一万物", "科大讯飞", "商汤科技", "MiniMax", "华为",
    "面壁智能", "阶跃星辰",
]


# Color palette for company cards (cycles if more companies than colors)
_COMPANY_COLORS = [
    "#6C5CE7", "#00B894", "#E17055", "#0984E3", "#FDCB6E",
    "#E84393", "#00CEC9", "#D63031", "#6C5CE7", "#55E6C1",
    "#FDA7DF", "#A29BFE", "#FF7675", "#74B9FF", "#FFEAA7",
    "#DDA0DD", "#98D8C8",
    # Chinese section
    "#FF6B6B", "#4ECDC4", "#FF8A5C", "#3B82F6", "#8B5CF6",
    "#EC4899", "#F97316", "#14B8A6", "#6366F1", "#EF4444",
    "#10B981", "#F59E0B", "#8B5CF6", "#06B6D4", "#84CC16",
]


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI News Digest — {date}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f0f2f5; color: #1a1a1a; line-height: 1.5;
  }}
  .header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: white; padding: 40px 24px; text-align: center;
  }}
  .header h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 6px; }}
  .header p {{ opacity: 0.7; font-size: 0.9rem; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 28px 20px; }}

  .section-label {{
    font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px;
    color: #999; margin: 32px 0 12px; padding-left: 4px;
  }}

  .company-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
    gap: 16px; margin-bottom: 24px;
  }}
  @media (max-width: 540px) {{
    .company-grid {{ grid-template-columns: 1fr; }}
  }}

  .company-card {{
    background: white; border-radius: 10px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    border: 1px solid #e8e8e8;
  }}
  .company-header {{
    padding: 12px 18px; color: white; font-weight: 600;
    font-size: 0.95rem; display: flex; justify-content: space-between;
    align-items: center;
  }}
  .company-header .badge {{
    background: rgba(255,255,255,0.25); padding: 2px 10px;
    border-radius: 10px; font-size: 0.78rem; font-weight: 500;
  }}

  .article-item {{
    padding: 10px 18px; border-bottom: 1px solid #f2f2f2;
  }}
  .article-item:last-child {{ border-bottom: none; }}
  .article-item a {{
    color: #222; text-decoration: none; font-size: 0.9rem;
    font-weight: 500; display: block; margin-bottom: 3px;
  }}
  .article-item a:hover {{ color: #6C5CE7; }}
  .article-item .meta {{
    font-size: 0.75rem; color: #999; display: flex; gap: 10px;
    align-items: center;
  }}
  .article-item .meta .src-tag {{
    background: #f0f0f0; padding: 1px 7px; border-radius: 3px;
    font-size: 0.7rem; color: #666;
  }}
  .article-item .summary {{
    font-size: 0.8rem; color: #777; margin-top: 4px;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
    overflow: hidden;
  }}

  .other-section {{
    background: white; border-radius: 10px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #e8e8e8;
    margin-bottom: 24px;
  }}
  .other-header {{
    padding: 12px 18px; background: #555; color: white; font-weight: 600;
    font-size: 0.95rem; display: flex; justify-content: space-between;
    align-items: center;
  }}
  .other-header .badge {{
    background: rgba(255,255,255,0.25); padding: 2px 10px;
    border-radius: 10px; font-size: 0.78rem; font-weight: 500;
  }}

  .footer {{
    text-align: center; padding: 32px; color: #aaa; font-size: 0.8rem;
  }}
  .footer a {{ color: #667eea; text-decoration: none; }}
  .footer a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
<div class="header">
  <h1>AI Company News Digest</h1>
  <p>{date} &mdash; {total} articles across {company_count} companies &middot; {source_count} sources</p>
</div>
<div class="container">
  {western_label}
  {western_cards}
  {chinese_label}
  {chinese_cards}
  {other_section}
</div>
<div class="footer">
  Generated automatically from TechCrunch, The Verge, Ars Technica, VentureBeat,
  MIT Tech Review, Hacker News, 机器之心, 量子位, 36氪.
  <br><a href="products.html">AI Product Tracker</a> &mdash; latest products & features
</div>
</body>
</html>"""

CARD_TEMPLATE = """<div class="company-card">
  <div class="company-header" style="background:{color}">
    {name} <span class="badge">{count}</span>
  </div>
  {articles}
</div>"""

OTHER_TEMPLATE = """<div class="other-section">
  <div class="other-header">
    Other AI News <span class="badge">{count}</span>
  </div>
  {articles}
</div>"""

ARTICLE_ITEM = """<div class="article-item">
  <a href="{link}" target="_blank" rel="noopener">{title}</a>
  <div class="meta">
    <span class="src-tag">{source}</span>
    <span>{published}</span>
  </div>
  {summary_html}
</div>"""

SECTION_LABEL = """<div class="section-label">{label}</div>"""


def _render_article_item(article):
    summary = article.get("summary", "")
    summary_html = ""
    if summary:
        summary = summary[:200] + "..." if len(summary) > 200 else summary
        summary_html = f'<div class="summary">{summary}</div>'

    published = article.get("published", "")
    if published and len(published) > 25:
        published = published[:25]

    return ARTICLE_ITEM.format(
        title=article["title"],
        link=article["link"],
        source=article["source"],
        published=published,
        summary_html=summary_html,
    )


def generate_html(articles, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    # Group articles by company
    groups = {}
    for a in articles:
        company = a.get("company", "other")
        groups.setdefault(company, []).append(a)

    # Separate into western, chinese, other
    western_companies = []
    chinese_companies = []
    for company in _COMPANY_ORDER:
        if company not in groups:
            continue
        # Chinese companies start from DeepSeek in the order list
        if _COMPANY_ORDER.index(company) >= _COMPANY_ORDER.index("DeepSeek"):
            chinese_companies.append(company)
        else:
            western_companies.append(company)

    other_articles = groups.get("other", [])

    # Render company cards
    def render_company_card(company, idx):
        arts = groups[company]
        color = _COMPANY_COLORS[_COMPANY_ORDER.index(company) % len(_COMPANY_COLORS)]
        items = "\n".join(_render_article_item(a) for a in arts)
        return CARD_TEMPLATE.format(name=company, count=len(arts), color=color, articles=items)

    western_cards = "\n".join(render_company_card(c, i) for i, c in enumerate(western_companies))
    chinese_cards = "\n".join(
        render_company_card(c, len(western_companies) + i)
        for i, c in enumerate(chinese_companies)
    )

    western_label = SECTION_LABEL.format(label="Western AI Companies") if western_companies else ""
    chinese_label = SECTION_LABEL.format(label="Chinese AI Companies") if chinese_companies else ""

    # Render other section
    other_section = ""
    if other_articles:
        items = "\n".join(_render_article_item(a) for a in other_articles)
        other_section = OTHER_TEMPLATE.format(count=len(other_articles), articles=items)

    date_str = datetime.now().strftime("%Y-%m-%d")
    today = datetime.now().strftime("%B %d, %Y")

    companies_with_news = set(a.get("company", "other") for a in articles)
    all_sources = set(a["source"] for a in articles)

    html = HTML_TEMPLATE.format(
        date=today,
        total=len(articles),
        company_count=len(companies_with_news),
        source_count=len(all_sources),
        western_label=western_label,
        western_cards=western_cards,
        chinese_label=chinese_label,
        chinese_cards=chinese_cards,
        other_section=other_section,
    )

    dated_path = os.path.join(output_dir, f"ai_news_{date_str}.html")
    with open(dated_path, "w", encoding="utf-8") as f:
        f.write(html)

    today_path = os.path.join(output_dir, "ai_news_today.html")
    with open(today_path, "w", encoding="utf-8") as f:
        f.write(html)

    return today_path
