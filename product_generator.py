import os
from datetime import datetime

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Product Tracker — {date}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f0f2f5; color: #1a1a1a; line-height: 1.5;
  }}
  .header {{
    background: linear-gradient(135deg, #0f3443 0%, #34e89e 100%);
    color: white; padding: 40px 24px; text-align: center;
  }}
  .header h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 6px; }}
  .header p {{ opacity: 0.8; font-size: 0.9rem; }}
  .nav-link {{
    display: inline-block; margin-top: 10px; color: rgba(255,255,255,0.9);
    font-size: 0.85rem;
  }}
  .nav-link a {{ color: white; }}
  .container {{ max-width: 1100px; margin: 0 auto; padding: 28px 20px; }}

  .section-label {{
    font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1.5px;
    color: #999; margin: 32px 0 12px; padding-left: 4px;
  }}

  .company-grid {{
    display: grid; grid-template-columns: 1fr; gap: 20px; margin-bottom: 24px;
  }}

  .company-card {{
    background: white; border-radius: 10px; overflow: hidden;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #e8e8e8;
  }}
  .company-header {{
    padding: 14px 20px; color: white; font-weight: 600;
    font-size: 1rem; display: flex; justify-content: space-between;
    align-items: center;
  }}
  .company-header .badge {{
    background: rgba(255,255,255,0.25); padding: 2px 10px;
    border-radius: 10px; font-size: 0.78rem; font-weight: 500;
  }}

  .product-item {{
    padding: 16px 20px; border-bottom: 1px solid #f0f0f0;
  }}
  .product-item:last-child {{ border-bottom: none; }}
  .product-item .product-name {{
    font-size: 1.05rem; font-weight: 600; color: #222; margin-bottom: 4px;
  }}
  .product-item .product-name a {{
    color: #222; text-decoration: none;
  }}
  .product-item .product-name a:hover {{ color: #0f3443; }}
  .product-item .product-date {{
    font-size: 0.78rem; color: #999; margin-bottom: 8px;
  }}
  .product-item .product-desc {{
    font-size: 0.88rem; color: #555; margin-bottom: 10px;
    line-height: 1.6;
  }}
  .product-item .features-list {{
    list-style: none; padding: 0;
  }}
  .product-item .features-list li {{
    font-size: 0.84rem; color: #444; padding: 4px 0;
    padding-left: 16px; position: relative;
  }}
  .product-item .features-list li::before {{
    content: "▸"; position: absolute; left: 0; color: #34e89e;
    font-size: 0.7rem; top: 6px;
  }}
  .product-item .source-link {{
    display: inline-block; margin-top: 8px; font-size: 0.8rem;
    color: #0f3443; text-decoration: none; font-weight: 500;
  }}
  .product-item .source-link:hover {{ text-decoration: underline; }}

  .empty-state {{
    text-align: center; padding: 40px; color: #999; font-size: 0.95rem;
  }}

  .footer {{
    text-align: center; padding: 32px; color: #aaa; font-size: 0.8rem;
  }}
  .footer a {{ color: #0f3443; }}
</style>
</head>
<body>
<div class="header">
  <h1>AI Product Tracker</h1>
  <p>Latest products & features from major AI companies &mdash; Updated: {date}</p>
  <div class="nav-link">
    <a href="ai_news_today.html">News Digest</a>
  </div>
</div>
<div class="container">
  {western_label}
  <div class="company-grid">
    {western_cards}
  </div>
  {chinese_label}
  <div class="company-grid">
    {chinese_cards}
  </div>
  {empty_section}
</div>
<div class="footer">
  Data fetched from official company blogs and announcement pages. Updates daily.
  <br><a href="ai_news_today.html">AI News Digest</a> &middot; Generated automatically
</div>
</body>
</html>"""

COMPANY_CARD = """<div class="company-card">
  <div class="company-header" style="background:{color}">
    {company} <span class="badge">{count} product(s)</span>
  </div>
  {products}
</div>"""

PRODUCT_ITEM = """<div class="product-item">
  <div class="product-name">
    <a href="{link}" target="_blank" rel="noopener">{product_name}</a>
  </div>
  <div class="product-date">{date}</div>
  <div class="product-desc">{description}</div>
  {features_html}
  <a class="source-link" href="{link}" target="_blank" rel="noopener">View on official site &rarr;</a>
</div>"""

SECTION_LABEL = """<div class="section-label">{label}</div>"""


_COMPANY_COLORS = [
    "#0F3443", "#1B5E20", "#BF360C", "#0D47A1", "#E65100",
    "#880E4F", "#004D40", "#B71C1C", "#311B92", "#00695C",
    "#4A148C", "#33691E", "#827717", "#263238", "#3E2723",
    "#1A237E", "#004D40",
    # Chinese
    "#C62828", "#00838F", "#D84315", "#1565C0", "#6A1B9A",
    "#AD1457", "#EF6C00", "#00695C", "#283593", "#B71C1C",
    "#1B5E20", "#E65100", "#4527A0", "#00838F", "#558B2F",
]


# Order: Western first, then Chinese
_COMPANY_ORDER = [
    "OpenAI", "Anthropic", "Google DeepMind", "Meta", "Microsoft",
    "Amazon", "Apple", "Nvidia", "xAI", "Mistral",
    "Stability AI", "Midjourney", "Perplexity", "Cohere",
    "Hugging Face", "Scale AI",
    "DeepSeek", "百度/文心", "阿里/通义", "字节跳动/豆包",
    "腾讯/混元", "智谱AI", "月之暗面/Kimi", "百川智能",
    "零一万物", "科大讯飞", "商汤科技", "MiniMax", "华为",
    "面壁智能", "阶跃星辰",
]


def _render_product_item(product):
    features = product.get("features", [])
    features_html = ""
    if features:
        items = "\n".join(f"<li>{f}</li>" for f in features[:5])
        features_html = f'<ul class="features-list">{items}</ul>'

    date_str = product.get("date", "")
    if date_str and len(date_str) > 30:
        date_str = date_str[:30]

    description = product.get("description", "")
    if len(description) > 300:
        description = description[:297] + "..."

    return PRODUCT_ITEM.format(
        product_name=product.get("product_name", product.get("title", "")),
        link=product.get("link", "#"),
        date=date_str,
        description=description,
        features_html=features_html,
    )


def generate_product_html(products, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    # Group by company
    groups = {}
    for p in products:
        company = p.get("company", "Other")
        groups.setdefault(company, []).append(p)

    # Separate western vs chinese
    western = []
    chinese = []
    chinese_start = _COMPANY_ORDER.index("DeepSeek")
    for company in _COMPANY_ORDER:
        if company not in groups:
            continue
        idx = _COMPANY_ORDER.index(company)
        if idx >= chinese_start:
            chinese.append(company)
        else:
            western.append(company)

    def render_card(company, global_idx):
        prods = groups[company]
        color = _COMPANY_COLORS[global_idx % len(_COMPANY_COLORS)]
        items = "\n".join(_render_product_item(p) for p in prods)
        return COMPANY_CARD.format(
            company=company, count=len(prods), color=color, products=items
        )

    western_cards = "\n".join(render_card(c, i) for i, c in enumerate(western))
    chinese_cards = "\n".join(
        render_card(c, len(western) + i) for i, c in enumerate(chinese)
    )

    western_label = SECTION_LABEL.format(label="Western AI Companies") if western else ""
    chinese_label = SECTION_LABEL.format(label="Chinese AI Companies") if chinese else ""

    empty_section = ""
    if not products:
        empty_section = '<div class="empty-state">No product announcements found in recent period. Check back tomorrow.</div>'

    today = datetime.now().strftime("%B %d, %Y")
    html = HTML_TEMPLATE.format(
        date=today,
        western_label=western_label,
        western_cards=western_cards,
        chinese_label=chinese_label,
        chinese_cards=chinese_cards,
        empty_section=empty_section,
    )

    path = os.path.join(output_dir, "products.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    return path
