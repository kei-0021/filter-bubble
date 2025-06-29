from typing import Any
import requests
import os
import json
from dotenv import load_dotenv
from contents_filtering import sample_category, update_weights

load_dotenv(dotenv_path="config/.env")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

category_weights: dict[str, float] = {
    "general": 0.5,
    "entertainment": 0.5,
}

def fetch_top_headlines(category: str, page_size: int = 1) -> list[dict[str, Any]]:
    params = {
        "category": category,
        "country": "us",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("articles", [])

def save_articles_to_json(articles: list[dict[str, Any]], filename="output/articles.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 記事データを '{filename}' に保存しました")

if __name__ == "__main__":
    all_articles = []

    for i in range(20):  # 20回記事を取得するフィルターバブル再現
        category = sample_category(category_weights)
        print(f"[{i+1}] 選ばれたカテゴリ: {category}（重み: {category_weights[category]:.3f}）")

        articles = fetch_top_headlines(category, page_size=1)
        if not articles:
            continue

        article = articles[0]
        article["category"] = category
        article["weight"] = category_weights[category]
        all_articles.append(article)

        update_weights(category_weights, clicked_category=category)

    print("\n[最終的なカテゴリ重み]")
    for cat, weight in category_weights.items():
        print(f"- {cat}: {weight:.3f}")

    save_articles_to_json(all_articles)
