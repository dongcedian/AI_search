"""Unified HTML generator — single page with tabs for News + Products."""

import os
from datetime import datetime


# ── Company display order & colors ──

_COMPANY_ORDER = [
    "OpenAI", "Anthropic", "Google DeepMind", "Meta", "Microsoft",
    "Amazon", "Apple", "Nvidia", "xAI", "Tesla", "Mistral",
    "Stability AI", "Midjourney", "Perplexity", "Cohere",
    "Hugging Face", "Scale AI",
    "DeepSeek", "百度/文心", "阿里/通义", "字节跳动/豆包",
    "腾讯/混元", "智谱AI", "月之暗面/Kimi", "百川智能",
    "零一万物", "科大讯飞", "商汤科技", "MiniMax", "华为",
    "面壁智能", "阶跃星辰",
]

_COMPANY_COLORS = [
    "#6C5CE7", "#00B894", "#E17055", "#0984E3", "#FDCB6E",
    "#E84393", "#00CEC9", "#D63031", "#6C5CE7", "#55E6C1",
    "#FDA7DF", "#A29BFE", "#FF7675", "#74B9FF", "#FFEAA7",
    "#DDA0DD", "#98D8C8",
    "#FF6B6B", "#4ECDC4", "#FF8A5C", "#3B82F6", "#8B5CF6",
    "#EC4899", "#F97316", "#14B8A6", "#6366F1", "#EF4444",
    "#10B981", "#F59E0B", "#8B5CF6", "#06B6D4", "#84CC16",
]

_CHINESE_START = _COMPANY_ORDER.index("DeepSeek")

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Dashboard — {date}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f0f2f5; color: #1a1a1a; line-height: 1.5;
  }}
  .header {{
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    color: white; padding: 32px 24px 0; text-align: center;
  }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 6px; }}
  .header p {{ opacity: 0.7; font-size: 0.85rem; padding-bottom: 0; }}

  /* ── Tab bar ── */
  .tab-bar {{
    display: flex; justify-content: center; gap: 0; margin-top: 16px;
  }}
  .tab-btn {{
    padding: 10px 28px; border: none; cursor: pointer;
    font-size: 0.9rem; font-weight: 600; color: rgba(255,255,255,0.6);
    background: transparent; border-bottom: 3px solid transparent;
    transition: all 0.2s;
  }}
  .tab-btn.active {{
    color: white; border-bottom-color: #00B894;
  }}
  .tab-btn:hover {{ color: rgba(255,255,255,0.85); }}

  .container {{ max-width: 1100px; margin: 0 auto; padding: 24px 20px; }}

  .section-label {{
    font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.5px;
    color: #999; margin: 28px 0 10px; padding-left: 4px;
  }}

  /* ── Company cards (shared) ── */
  .company-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(480px, 1fr));
    gap: 14px; margin-bottom: 20px;
  }}
  @media (max-width: 540px) {{
    .company-grid {{ grid-template-columns: 1fr; }}
  }}
  .company-card {{
    background: white; border-radius: 10px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #e8e8e8;
  }}
  .company-header {{
    padding: 11px 16px; color: white; font-weight: 600;
    font-size: 0.9rem; display: flex; justify-content: space-between; align-items: center;
  }}
  .company-header .badge {{
    background: rgba(255,255,255,0.25); padding: 2px 10px;
    border-radius: 10px; font-size: 0.75rem; font-weight: 500;
  }}

  /* ── News articles ── */
  .article-item {{
    padding: 10px 16px; border-bottom: 1px solid #f2f2f2;
  }}
  .article-item:last-child {{ border-bottom: none; }}
  .article-item a {{
    color: #222; text-decoration: none; font-size: 0.88rem;
    font-weight: 500; display: block; margin-bottom: 2px;
  }}
  .article-item a:hover {{ color: #6C5CE7; }}
  .article-item .meta {{
    font-size: 0.73rem; color: #999; display: flex; gap: 8px; align-items: center;
  }}
  .article-item .meta .src-tag {{
    background: #f0f0f0; padding: 1px 6px; border-radius: 3px;
    font-size: 0.68rem; color: #666;
  }}
  .article-item .summary {{
    font-size: 0.78rem; color: #777; margin-top: 3px;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  }}

  /* ── Products ── */
  .product-item {{
    padding: 12px 16px; border-bottom: 1px solid #f0f0f0;
  }}
  .product-item:last-child {{ border-bottom: none; }}
  .product-item .product-name {{
    font-size: 0.93rem; font-weight: 600; margin-bottom: 3px;
  }}
  .product-item .product-name a {{
    color: #222; text-decoration: none;
  }}
  .product-item .product-name a:hover {{ color: #0f3443; }}
  .product-item .product-desc {{
    font-size: 0.82rem; color: #777; line-height: 1.5;
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  }}

  /* ── Other section ── */
  .other-section {{
    background: white; border-radius: 10px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #e8e8e8;
    margin-bottom: 20px;
  }}
  .other-header {{
    padding: 11px 16px; background: #555; color: white; font-weight: 600;
    font-size: 0.9rem; display: flex; justify-content: space-between; align-items: center;
  }}
  .other-header .badge {{
    background: rgba(255,255,255,0.25); padding: 2px 10px;
    border-radius: 10px; font-size: 0.75rem; font-weight: 500;
  }}

  .empty-state {{ text-align: center; padding: 40px; color: #999; font-size: 0.9rem; }}
  .footer {{
    text-align: center; padding: 28px; color: #aaa; font-size: 0.78rem;
  }}

  /* ── Tab content visibility ── */
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
</style>
</head>
<body>
<div class="header">
  <h1>AI Dashboard</h1>
  <p>{date} &middot; {news_total} news articles &middot; {product_total} product updates</p>
  <div class="tab-bar">
    <button class="tab-btn active" onclick="switchTab('news')">News Digest</button>
    <button class="tab-btn" onclick="switchTab('products')">Product Tracker</button>
  </div>
</div>

<div class="container">
  <!-- ═══════ NEWS TAB ═══════ -->
  <div id="tab-news" class="tab-content active">
    {news_western_label}
    <div class="company-grid">{news_western_cards}</div>
    {news_chinese_label}
    <div class="company-grid">{news_chinese_cards}</div>
    {news_other_section}
  </div>

  <!-- ═══════ PRODUCTS TAB ═══════ -->
  <div id="tab-products" class="tab-content">
    {prod_western_label}
    <div class="company-grid">{prod_western_cards}</div>
    {prod_chinese_label}
    <div class="company-grid">{prod_chinese_cards}</div>
    {prod_empty}
  </div>
</div>

<div class="footer">
  Generated automatically from official sources and major tech news feeds.
</div>

<script>
  function switchTab(tab) {{
    document.querySelectorAll('.tab-btn').forEach(function(b) {{ b.classList.remove('active'); }});
    document.querySelectorAll('.tab-content').forEach(function(c) {{ c.classList.remove('active'); }});
    document.getElementById('tab-' + tab).classList.add('active');
    event.target.classList.add('active');
  }}
</script>
</body>
</html>"""

NEWS_ARTICLE = """<div class="article-item">
  <a href="{link}" target="_blank" rel="noopener">{title}</a>
  <div class="meta">
    <span class="src-tag">{source}</span>
    <span>{published}</span>
  </div>
  {summary_html}
</div>"""

NEWS_CARD = """<div class="company-card">
  <div class="company-header" style="background:{color}">{name} <span class="badge">{count}</span></div>
  {articles}
</div>"""

NEWS_OTHER = """<div class="other-section">
  <div class="other-header">Other AI News <span class="badge">{count}</span></div>
  {articles}
</div>"""

PRODUCT_ITEM = """<div class="product-item">
  <div class="product-name"><a href="{link}" target="_blank" rel="noopener">{name}</a></div>
  <div class="product-desc">{desc}</div>
</div>"""

PRODUCT_CARD = """<div class="company-card">
  <div class="company-header" style="background:{color}">{name} <span class="badge">{count} product(s)</span></div>
  {products}
</div>"""

SECTION_LABEL = '<div class="section-label">{label}</div>'


# ═══════════════════════════════════════════════════════════
#  Rendering helpers
# ═══════════════════════════════════════════════════════════

def _render_news_article(a):
    summary = a.get("summary", "")
    summary_html = ""
    if summary:
        summary = summary[:200] + "..." if len(summary) > 200 else summary
        summary_html = f'<div class="summary">{summary}</div>'
    published = a.get("published", "")
    if published and len(published) > 25:
        published = published[:25]
    return NEWS_ARTICLE.format(
        title=a["title"], link=a["link"], source=a["source"],
        published=published, summary_html=summary_html,
    )


def _render_product(p):
    desc = p.get("description", "")
    if len(desc) > 150:
        desc = desc[:147] + "..."
    return PRODUCT_ITEM.format(
        name=p.get("product_name", p.get("title", "")),
        link=p.get("link", "#"),
        desc=desc,
    )


def _render_company_section(company, items, render_fn, card_tmpl, color_idx):
    color = _COMPANY_COLORS[color_idx % len(_COMPANY_COLORS)]
    rendered = "\n".join(render_fn(it) for it in items)
    return card_tmpl.format(name=company, count=len(items), color=color, articles=rendered, products=rendered)


def _split_companies(groups):
    western, chinese = [], []
    for company in _COMPANY_ORDER:
        if company not in groups:
            continue
        if _COMPANY_ORDER.index(company) >= _CHINESE_START:
            chinese.append(company)
        else:
            western.append(company)
    return western, chinese


def _render_news_html(articles):
    groups = {}
    for a in articles:
        c = a.get("company", "other")
        groups.setdefault(c, []).append(a)

    other_articles = groups.pop("other", [])
    western, chinese = _split_companies(groups)

    western_cards = "\n".join(
        _render_company_section(c, groups[c], _render_news_article, NEWS_CARD,
                                _COMPANY_ORDER.index(c))
        for c in western
    )
    chinese_cards = "\n".join(
        _render_company_section(c, groups[c], _render_news_article, NEWS_CARD,
                                _COMPANY_ORDER.index(c))
        for c in chinese
    )

    w_label = SECTION_LABEL.format(label="Western AI Companies") if western else ""
    c_label = SECTION_LABEL.format(label="Chinese AI Companies") if chinese else ""

    other_section = ""
    if other_articles:
        items = "\n".join(_render_news_article(a) for a in other_articles)
        other_section = NEWS_OTHER.format(count=len(other_articles), articles=items)

    return w_label, western_cards, c_label, chinese_cards, other_section


def _render_products_html(products):
    groups = {}
    for p in products:
        c = p.get("company", "Other")
        groups.setdefault(c, []).append(p)

    western, chinese = _split_companies(groups)

    western_cards = "\n".join(
        _render_company_section(c, groups[c], _render_product, PRODUCT_CARD,
                                _COMPANY_ORDER.index(c))
        for c in western
    )
    chinese_cards = "\n".join(
        _render_company_section(c, groups[c], _render_product, PRODUCT_CARD,
                                _COMPANY_ORDER.index(c))
        for c in chinese
    )

    w_label = SECTION_LABEL.format(label="Western AI Companies") if western else ""
    c_label = SECTION_LABEL.format(label="Chinese AI Companies") if chinese else ""

    empty = ""
    if not products:
        empty = '<div class="empty-state">No product announcements found. Check back later.</div>'

    return w_label, western_cards, c_label, chinese_cards, empty


# ═══════════════════════════════════════════════════════════
#  Main entry
# ═══════════════════════════════════════════════════════════

def generate_unified_page(articles, products, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    nwl, nwc, ncl, ncc, nother = _render_news_html(articles)
    pwl, pwc, pcl, pcc, pempty = _render_products_html(products)

    date_str = datetime.now().strftime("%Y-%m-%d")
    today = datetime.now().strftime("%B %d, %Y")

    html = HTML.format(
        date=today,
        news_total=len(articles),
        product_total=len(products),
        news_western_label=nwl,
        news_western_cards=nwc,
        news_chinese_label=ncl,
        news_chinese_cards=ncc,
        news_other_section=nother,
        prod_western_label=pwl,
        prod_western_cards=pwc,
        prod_chinese_label=pcl,
        prod_chinese_cards=pcc,
        prod_empty=pempty,
    )

    dated_path = os.path.join(output_dir, f"ai_dashboard_{date_str}.html")
    with open(dated_path, "w", encoding="utf-8") as f:
        f.write(html)

    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    return index_path
