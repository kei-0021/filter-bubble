from typing import Any
import os
import json
from dotenv import load_dotenv
from contents_filtering_simulator import FilterBubbleSimulator

load_dotenv(dotenv_path="config/.env")

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
ITERATION = 20

category_weights: dict[str, float] = {
    "general": 0.5,
    "entertainment": 0.5,
}


# def fetch_top_headlines(category: str, page_size: int = 1) -> list[dict[str, Any]]:
#     params = {
#         "category": category,
#         "country": "us",
#         "pageSize": page_size,
#         "apiKey": NEWS_API_KEY,
#     }
#     response = requests.get(NEWS_API_URL, params=params)
#     response.raise_for_status()
#     data = response.json()
#     return data.get("articles", [])


def fetch_top_headlines(category: str, count: int):
    """fetch_top_headlines のダミー実装 (実行可能にするため)"""
    return [
        {
            "title": f"Article about {category} {i}",
            "url": f"http://example.com/{category}/{i}",
        }
        for i in range(count)
    ]


def save_articles_to_json(
    articles: list[dict[str, Any]], filename="output/articles.json"
):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 記事データを '{filename}' に保存しました")


if __name__ == "__main__":
    sim = FilterBubbleSimulator(
        {
            "general": 0.2,
            "entertainment": 0.2,
            "sports": 0.2,
            "technology": 0.2,
            "science": 0.1,
            "business": 0.1,
        }
    )

    all_articles = []

    for i in range(ITERATION):
        cat = sim.sample()
        print(f"[{i + 1}] 選ばれたカテゴリ: {cat}（重み: {sim.weights[cat]:.3f}）")

        articles = fetch_top_headlines(cat, 1)
        if not articles:
            raise ValueError

        article = articles[0]
        article["category"] = cat
        article["weight"] = sim.weights[cat]
        all_articles.append(article)

        sim.update(clicked_category=cat)

    sim.plot()
    # save_articles_to_json(all_articles)
