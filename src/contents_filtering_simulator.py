import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


@dataclass
class FilterBubbleSimulator:
    weights: Dict[str, float]
    """カテゴリと重みづけをまとめた辞書."""

    history: Dict[str, List[float]]
    """カテゴリをキーに、重みづけの変化をリストとして記録した辞書."""

    fetcher: Callable[[str, int], List[Dict[str, Any]]]
    """カテゴリを受け取り、記事のリストを返す関数."""

    selected_categories: List[str]
    """選択されたカテゴリの履歴を保持するリスト."""

    def __init__(
        self,
        initial_weights: Dict[str, float],
        fetcher: Callable[[str, int], List[Dict[str, Any]]],
    ):
        self.weights = initial_weights.copy()
        self.history = {cat: [weight] for cat, weight in initial_weights.items()}
        self.fetcher = fetcher
        self.selected_categories = []

    def fetch(self, category: str, count: int = 1) -> List[Dict[str, Any]]:
        """指定カテゴリの記事を取得し記事リストを返すメソッド."""
        return self.fetcher(category, count)

    def step(self, num_articles: int = 10) -> List[Dict[str, Any]]:
        """
        1ステップ分の記事リストを重みに基づいて取得して返す.
        返す記事はdictに 'category' キーが必ず入っている.
        """
        categories = list(self.weights.keys())
        sampled_categories = random.choices(
            categories, weights=self.weights.values(), k=num_articles
        )

        articles = []
        for cat in sampled_categories:
            fetched_articles = self.fetch(cat, 1)
            if fetched_articles:
                article = fetched_articles[0].copy()
                article["category"] = cat
            else:
                article = {"title": "No article", "content": "", "category": cat}
            articles.append(article)
        return articles

    def select(self, chosen_category: str, boost: float = 0.1, decay: float = 0.9):
        """
        ユーザー選択したカテゴリをもとに重みを更新し履歴に追加.
        """
        for cat in self.weights:
            if cat == chosen_category:
                self.weights[cat] += boost
            else:
                self.weights[cat] *= decay
        # 正規化
        total = sum(self.weights.values())
        for cat in self.weights:
            self.weights[cat] /= total
            self.history[cat].append(self.weights[cat])

        self.selected_categories.append(chosen_category)

    def plot(self, save_path: str | None = None) -> Figure | None:
        plt.figure(figsize=(12, 7))

        categories = list(self.weights.keys())
        num_iters = len(self.history[categories[0]])
        ind = np.arange(num_iters)
        reversed_categories = list(reversed(categories))
        data = np.array([self.history[cat] for cat in reversed_categories])
        bottom = np.zeros(num_iters)
        bar_colors = plt.cm.tab10.colors
        color_map = {
            cat: bar_colors[i % 10] for i, cat in enumerate(reversed_categories)
        }

        fig, ax = plt.subplots(figsize=(12, 7))
        for i, cat in enumerate(reversed_categories):
            ax.bar(
                ind + 1,
                data[i],
                bottom=bottom,
                label=cat,
                width=0.8,
                color=color_map[cat],
            )
            bottom += data[i]

        if self.selected_categories:
            for t, cat in enumerate(self.selected_categories):
                ax.scatter(
                    t + 1,
                    1.02,
                    color=color_map[cat],
                    s=120,
                    marker="o",
                    edgecolor="black",
                    zorder=5,
                    label=f"Selected: {cat}" if t == 0 else None,
                )

        ax.set_xlabel("Iteration")
        ax.set_ylabel("Weight")
        ax.set_title("Filter Bubble Evolution (Stacked Bar Chart) + Selected Category")
        ax.set_xticks(np.arange(0, num_iters + 1, max(1, num_iters // 10)))
        ax.set_ylim(0, 1.1)

        handles, labels = ax.get_legend_handles_labels()
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
        others.reverse()
        handles_ordered = [h for h, _ in selected] + [h for h, _ in others]
        labels_ordered = [label for _, label in selected] + [
            label for _, label in others
        ]

        ax.legend(handles_ordered, labels_ordered, loc="upper left")
        ax.grid(axis="y", linestyle="--")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            plt.close(fig)
            print(f"グラフを '{save_path}' に保存しました。")
            return None
        else:
            # ファイル保存しない場合は Figure を返す（閉じない）
            return fig
