"""Official blog / product announcement sources for each AI company.

For each company: preferred RSS feed, blog page URL as fallback.
"""

PRODUCT_SOURCES = [
    # ── Western Companies ──
    {
        "company": "OpenAI",
        "rss": None,  # no official RSS
        "blog": "https://openai.com/blog",
        "lang": "en",
    },
    {
        "company": "Anthropic",
        "rss": None,
        "blog": "https://www.anthropic.com/news",
        "lang": "en",
    },
    {
        "company": "Google DeepMind",
        "rss": None,
        "blog": "https://deepmind.google/discover/blog/",
        "lang": "en",
    },
    {
        "company": "Meta",
        "rss": None,
        "blog": "https://ai.meta.com/blog/",
        "lang": "en",
    },
    {
        "company": "Microsoft",
        "rss": None,
        "blog": "https://azure.microsoft.com/en-us/blog/category/ai-machine-learning/",
        "lang": "en",
    },
    {
        "company": "Amazon",
        "rss": "https://aws.amazon.com/blogs/machine-learning/feed/",
        "blog": "https://aws.amazon.com/blogs/machine-learning/",
        "lang": "en",
    },
    {
        "company": "Apple",
        "rss": None,
        "blog": "https://machinelearning.apple.com/",
        "lang": "en",
    },
    {
        "company": "Nvidia",
        "rss": None,
        "blog": "https://blogs.nvidia.com/ai-pc/",
        "lang": "en",
    },
    {
        "company": "xAI",
        "rss": None,
        "blog": "https://x.ai/blog",
        "lang": "en",
    },
    {
        "company": "Mistral",
        "rss": None,
        "blog": "https://mistral.ai/news/",
        "lang": "en",
    },
    {
        "company": "Stability AI",
        "rss": None,
        "blog": "https://stability.ai/news",
        "lang": "en",
    },
    {
        "company": "Midjourney",
        "rss": None,
        "blog": "https://www.midjourney.com/blog",
        "lang": "en",
    },
    {
        "company": "Perplexity",
        "rss": None,
        "blog": "https://www.perplexity.ai/blog",
        "lang": "en",
    },
    {
        "company": "Cohere",
        "rss": None,
        "blog": "https://cohere.com/blog",
        "lang": "en",
    },
    {
        "company": "Hugging Face",
        "rss": "https://huggingface.co/blog/feed.xml",
        "blog": "https://huggingface.co/blog",
        "lang": "en",
    },
    {
        "company": "Scale AI",
        "rss": None,
        "blog": "https://scale.com/blog",
        "lang": "en",
    },

    # ── Chinese Companies ──
    {
        "company": "百度/文心",
        "rss": None,
        "blog": "https://yiyan.baidu.com/",
        "lang": "zh",
    },
    {
        "company": "阿里/通义",
        "rss": None,
        "blog": "https://tongyi.aliyun.com/",
        "lang": "zh",
    },
    {
        "company": "字节跳动/豆包",
        "rss": None,
        "blog": "https://www.doubao.com/blog",
        "lang": "zh",
    },
    {
        "company": "腾讯/混元",
        "rss": None,
        "blog": "https://hunyuan.tencent.com/",
        "lang": "zh",
    },
    {
        "company": "DeepSeek",
        "rss": None,
        "blog": "https://www.deepseek.com/",
        "lang": "zh",
    },
    {
        "company": "智谱AI",
        "rss": None,
        "blog": "https://open.bigmodel.cn/",
        "lang": "zh",
    },
    {
        "company": "月之暗面/Kimi",
        "rss": None,
        "blog": "https://kimi.moonshot.cn/",
        "lang": "zh",
    },
    {
        "company": "百川智能",
        "rss": None,
        "blog": "https://www.baichuan-ai.com/",
        "lang": "zh",
    },
    {
        "company": "零一万物",
        "rss": None,
        "blog": "https://www.01.ai/",
        "lang": "zh",
    },
    {
        "company": "科大讯飞",
        "rss": None,
        "blog": "https://xinghuo.xfyun.cn/",
        "lang": "zh",
    },
    {
        "company": "商汤科技",
        "rss": None,
        "blog": "https://www.sensetime.com/cn/news",
        "lang": "zh",
    },
    {
        "company": "MiniMax",
        "rss": None,
        "blog": "https://www.minimaxi.com/",
        "lang": "zh",
    },
    {
        "company": "华为",
        "rss": None,
        "blog": "https://www.huaweicloud.com/",
        "lang": "zh",
    },
    {
        "company": "面壁智能",
        "rss": None,
        "blog": "https://minicpm.com/",
        "lang": "zh",
    },
    {
        "company": "阶跃星辰",
        "rss": None,
        "blog": "https://www.stepfun.com/",
        "lang": "zh",
    },
]
