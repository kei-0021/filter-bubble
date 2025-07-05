import json
from typing import Any

from dotenv import load_dotenv

from server.contents_fetcher import fetch_dummy
from server.contents_filtering_simulator import FilterBubbleSimulator

load_dotenv(dotenv_path="config/.env")

ITERATION = 100


def save_articles_to_json(
    articles: list[dict[str, Any]], filename="output/articles.json"
):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[INFO] 記事データを '{filename}' に保存しました")


if __name__ == "__main__":
    sim = FilterBubbleSimulator(
        initial_weights={
            "general": 0.2,
            "entertainment": 0.2,
            "sports": 0.2,
            "technology": 0.2,
            "science": 0.1,
            "business": 0.1,
        },
        fetcher=fetch_dummy,
    )

    # 自動選択モードでシミュレーションを実行
    sim.run_simulation(num_iterations=ITERATION, auto=True)
    sim.plot(save_path="output/weights_plot.png")
    # 必要なら記事データ保存も可能
    # save_articles_to_json(all_articles)
