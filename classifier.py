"""AI relevance filter and company classifier for news articles."""

import re

# --- AI relevance keywords ---

_EN_AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "llm",
    "large language model", "gpt", "chatgpt", "claude", "gemini",
    "deep learning", "neural net", "transformer model", "diffusion model",
    "foundation model", "open source model", "text-to-image",
    "video generation", "ai agent", "copilot", "fine-tuning", "fine tuning",
    "rag", "token", "inference", "training data", "prompt", "jailbreak",
    "alignment", "ai safety", "language model", "multimodal",
]

_ZH_AI_KEYWORDS = [
    "人工智能", "大模型", "机器学习", "深度学习", "模型",
    "智能体", "开源模型", "基座模型", "训练", "推理", "微调",
    "多模态", "文生图", "文生视频", "智能助手", "对话模型",
    "语言模型", "视觉模型", "生成式", "ai",
]


def _contains_any(text, keywords):
    """Case-insensitive check if text contains any keyword, with Unicode normalization."""
    normalized = _normalize(text)
    for kw in keywords:
        if _normalize(kw) in normalized:
            return True
    return False


def is_ai_related(title, summary=""):
    """Return True if the article is about AI based on title + summary keywords."""
    text = f"{title} {summary}"
    return _contains_any(text, _EN_AI_KEYWORDS) or _contains_any(text, _ZH_AI_KEYWORDS)


# --- Company classification ---

_COMPANY_PATTERNS = [
    # Western companies
    ("OpenAI", ["openai", "chatgpt", "gpt-4", "gpt-5", "dall-e", "sora", "sam altman", "o3", "o4"]),
    ("Anthropic", ["anthropic", "claude", "dario amodei"]),
    ("Google DeepMind", ["deepmind", "gemini", "google deepmind", "bard", "alphafold", "veo", "google brain", "google ai", "google's ai"]),
    ("Meta", ["meta ai", "llama", "meta's", "mark zuckerberg", "facebook ai"]),
    ("Microsoft", ["microsoft", "copilot", "phi-3", "phi-4", "satya nadella", "msft ai"]),
    ("Amazon", ["amazon", "aws ai", "amazon nova", "alexa ai"]),
    ("Apple", ["apple intelligence", "apple ai", "siri ai", "tim cook"]),
    ("Nvidia", ["nvidia ai", "cuda", "h100", "h200", "b100", "b200", "gpu", "jensen huang"]),
    ("xAI", ["xai", "grok", "x.ai"]),
    ("Tesla", ["tesla ai", "fsd", "optimus robot", "tesla bot"]),
    ("Mistral", ["mistral"]),
    ("Stability AI", ["stability ai", "stable diffusion", "sd3", "stable cascade"]),
    ("Midjourney", ["midjourney"]),
    ("Perplexity", ["perplexity"]),
    ("Cohere", ["cohere"]),
    ("Hugging Face", ["hugging face", "huggingface"]),
    ("Scale AI", ["scale ai"]),

    # Chinese companies
    ("百度/文心", ["百度", "文心", "文心一言", "ernie"]),
    ("阿里/通义", ["阿里", "阿里巴巴", "通义", "通义千问", "qwen"]),
    ("字节跳动/豆包", ["字节", "字节跳动", "豆包", "云雀", "bytedance"]),
    ("腾讯/混元", ["腾讯", "混元", "hunyuan"]),
    ("DeepSeek", ["deepseek", "深度求索"]),
    ("智谱AI", ["智谱", "glm", "chatglm"]),
    ("月之暗面/Kimi", ["月之暗面", "kimi", "moonshot"]),
    ("百川智能", ["百川", "baichuan"]),
    ("零一万物", ["零一万物", "yi", "李开复"]),
    ("科大讯飞", ["科大讯飞", "讯飞星火", "spark"]),
    ("商汤科技", ["商汤", "sensetime", "日日新"]),
    ("MiniMax", ["minimax", "稀宇"]),
    ("华为", ["华为", "盘古", "huawei ai"]),
    ("面壁智能", ["面壁", "minicpm"]),
    ("阶跃星辰", ["阶跃星辰", "stepfun"]),
]


def _normalize(text):
    """Normalize text for matching: lowercase, replace curly quotes, etc."""
    text = text.lower()
    text = text.replace("‘", "'").replace("’", "'")  # curly single quotes
    text = text.replace("“", '"').replace("”", '"')  # curly double quotes
    text = text.replace("–", "-").replace("—", "-")  # en/em dashes
    return text


def classify_company(title, summary=""):
    """Return the company name this article is about, or 'other' if no specific company.

    Title matches take priority over summary-only matches, since the title
    usually names the primary subject.
    """
    title_lower = _normalize(title)
    full_text = f"{title_lower} {_normalize(summary)}"

    # First pass: check title only (stronger signal)
    for company, patterns in _COMPANY_PATTERNS:
        for p in patterns:
            if _normalize(p) in title_lower:
                return company

    # Second pass: check title + summary
    for company, patterns in _COMPANY_PATTERNS:
        for p in patterns:
            if _normalize(p) in full_text:
                return company

    return "other"
