import os
from typing import Any

import requests

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = os.getenv("NEWS_API_URL")


def fetch_from_newsapi(category: str, count: int) -> list[dict[str, Any]]:
    """NewsAPIから指定したカテゴリのニュース記事を取得する関数"""
    params = {
        "category": category,
        "country": "us",
        "pageSize": count,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("articles", [])


def fetch_dummy(category: str, count: int) -> list[dict[str, Any]]:
    """fetch_from_newsapi のダミー実装 (実行可能にするため)"""
    return [
        {
            "title": f"[Dummy] Article about {category} {i}",
            "url": f"http://example.com/{category}/{i}",
        }
        for i in range(count)
    ]
