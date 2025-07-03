import random
from dataclasses import dataclass
from typing import Any, Callable

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class FilterBubbleSimulator:
    weights: dict[str, float]
    """カテゴリと重みづけをまとめた辞書."""

    history: dict[str, list[float]]
    """カテゴリをキーに、重みづけの変化をリストとして記録した辞書."""

    fetcher: Callable[[str], list[dict[str, Any]]]
    """カテゴリを受け取り、記事のリストを返す関数."""

    selected_categories: list[str]
    """選択されたカテゴリの履歴を保持するリスト."""

    def __init__(
        self,
        initial_weights: dict[str, float],
        fetcher: Callable[[str], list[dict[str, Any]]],
    ):
        self.weights = initial_weights.copy()
        self.history = {cat: [weight] for cat, weight in initial_weights.items()}
        self.fetcher = fetcher
        self.selected_categories = []  # 選択されたカテゴリの履歴

    def fetch(self, category: str, count: int = 1) -> tuple[str, list[dict[str, Any]]]:
        """指定カテゴリの記事を取得し、カテゴリと記事リストを返すメソッド."""
        articles = self.fetcher(category, count)
        return category, articles

    def run_simulation(self, num_iterations: int = 20, auto: bool = True):
        """
        シミュレーションを実行するメソッド。
        - 10件の記事を重みに基づいてカテゴリから取得し表示
        - auto=Trueなら自動選択、Falseならユーザー選択
        """
        categories = list(self.weights.keys())
        for i in range(num_iterations):
            # 10件の記事をカテゴリ重みに基づきサンプリング
            sampled_categories = random.choices(
                categories, weights=self.weights.values(), k=10
            )
            articles: list[dict[str, Any]] = []
            for cat in sampled_categories:
                _, fetched_articles = self.fetch(cat, 1)
                if fetched_articles:
                    articles.append({"category": cat, **fetched_articles[0]})
                else:
                    articles.append(
                        {"category": cat, "title": "No article", "content": ""}
                    )

            print(f"\nIteration {i + 1}")
            for idx, art in enumerate(articles):
                print(f"[{idx}] ({art['category']}) {art.get('title', '')}")

            if auto:
                # 重みからサンプリングして自動で選ぶ
                chosen_idx = random.choices(range(10), k=1)[0]
                print(f"[Auto] Chose index: {chosen_idx}")
            else:
                chosen_idx = int(input("Select article index (0-9): "))

            chosen_category = articles[chosen_idx]["category"]
            self._update(chosen_category)
            self.selected_categories.append(chosen_category)  # 選択履歴を記録

        print("Simulation finished.")

    def plot(self):
        """重みづけの変化を積み上げ棒グラフで可視化し、選択カテゴリの推移も色付きで描画するメソッド."""
        plt.figure(figsize=(12, 7))  # グラフのサイズを調整

        categories = list(self.weights.keys())
        num_iterations = len(self.history[categories[0]])  # イテレーション数
        ind = np.arange(num_iterations)
        # カテゴリを逆順で積み上げ
        reversed_categories = list(reversed(categories))
        data = np.array([self.history[cat] for cat in reversed_categories])
        bottom_values = np.zeros(num_iterations)
        bar_colors = plt.cm.tab10.colors  # 10色カラーマップ
        # reversed_categoriesの順で色を割り当てる
        color_map = {
            cat: bar_colors[i % 10] for i, cat in enumerate(reversed_categories)
        }
        for i, category in enumerate(reversed_categories):
            plt.bar(
                ind + 1,
                data[i],
                bottom=bottom_values,
                label=category,
                width=0.8,
                color=color_map[category],
            )
            bottom_values += data[i]

        # 選択カテゴリの推移をカテゴリごとの色で大きな点で描画
        if hasattr(self, "selected_categories") and self.selected_categories:
            for t, cat in enumerate(self.selected_categories):
                plt.scatter(
                    t + 1,
                    1.02,  # 棒グラフの上に点を描画
                    color=color_map[cat],
                    s=120,
                    marker="o",
                    edgecolor="black",
                    zorder=5,
                    label=f"Selected: {cat}" if t == 0 else None,  # 凡例は1回だけ
                )

        plt.xlabel("Iteration")
        plt.ylabel("Weight")
        plt.title("Filter Bubble Evolution (Stacked Bar Chart) + Selected Category")
        tick_interval = 10
        plt.xticks(np.arange(0, num_iterations + 1, tick_interval))
        plt.ylim(0, 1.1)
        handles, labels = plt.gca().get_legend_handles_labels()
        # "Selected:" で始まるラベルを一番上に、それ以外は逆順で並べる
        selected = [
            (h, label)
            for h, label in zip(handles, labels)
            if label.startswith("Selected:")
        ]
        others = [
            (h, label)
            for h, label in zip(handles, labels)
            if not label.startswith("Selected:")
        ]
        others = others[::-1]
        new_handles = [h for h, label in selected] + [h for h, label in others]
        new_labels = [label for h, label in selected] + [label for h, label in others]
        plt.legend(new_handles, new_labels, loc="upper left")
        plt.grid(axis="y", linestyle="--")
        plt.tight_layout()
        plt.savefig("output/weight_progress_stacked_bar.png")
        plt.close()

        print("グラフの描画が完了しました")

    def _sample(self) -> str:
        """現在の重みづけに基づいてカテゴリを1つ選択するメソッド."""
        categories = list(self.weights.keys())
        probs = list(self.weights.values())
        return random.choices(categories, weights=probs, k=1)[0]

    def _update(self, clicked_category: str, boost: float = 0.1, decay: float = 0.9):
        """選択したカテゴリの重みづけを増やし、そうでないカテゴリの重みづけを減らすメソッド."""
        for category in self.weights:
            if category == clicked_category:
                self.weights[category] += boost
            else:
                self.weights[category] *= decay
        # 正規化
        total = sum(self.weights.values())
        for category in self.weights:
            self.weights[category] /= total
            self.history[category].append(self.weights[category])  # 毎回記録
