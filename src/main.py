import requests
import os
import json
from dotenv import load_dotenv

def fetch_top_headlines(category, page_size=10):
    load_dotenv(dotenv_path="config/.env")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "country": "us",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("articles", [])

def save_articles_to_json(articles, filename="output/articles.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 記事データを '{filename}' に保存しました")

if __name__ == "__main__":
    general_articles = fetch_top_headlines("general", 10)
    entertainment_articles = fetch_top_headlines("entertainment", 10)

    all_articles = general_articles + entertainment_articles

    print(f"全体記事（フィルター前）: {len(all_articles)} 件")
    print(f"一般記事: {len(general_articles)} 件")
    print(f"エンタメ記事: {len(entertainment_articles)} 件")

    save_articles_to_json(all_articles)
