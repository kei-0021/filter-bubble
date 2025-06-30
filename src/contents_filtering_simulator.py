from dataclasses import dataclass
import random
import matplotlib.pyplot as plt
import numpy as np


@dataclass
class FilterBubbleSimulator:
    weights: dict[str, float]
    """カテゴリと重みづけをまとめた辞書."""

    history: dict[str, list[float]]
    """カテゴリをキーに、重みづけの変化をリストとして記録した辞書."""

    def __init__(self, initial_weights: dict[str, float]):
        self.weights = initial_weights.copy()
        self.history = {cat: [weight] for cat, weight in initial_weights.items()}

    def sample(self) -> str:
        """現在の重みづけに基づいてカテゴリを1つ選択するメソッド."""
        categories = list(self.weights.keys())
        probs = list(self.weights.values())
        return random.choices(categories, weights=probs, k=1)[0]

    def update(self, clicked_category: str, boost: float = 0.1, decay: float = 0.9):
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

    def plot(self):
        plt.figure(figsize=(12, 7))  # グラフのサイズを調整

        categories = list(self.weights.keys())
        num_iterations = len(self.history[categories[0]])  # イテレーション数

        # 棒グラフのX軸の位置 (0から始まるインデックス)
        ind = np.arange(num_iterations)

        # 各カテゴリのデータをNumPy配列に変換 (行がカテゴリ、列がイテレーション)
        data = np.array([self.history[cat] for cat in categories])

        # 積み上げ棒グラフを描画
        bottom_values = np.zeros(num_iterations)  # 各棒の「下限」を初期化
        for i, category in enumerate(categories):
            # plt.bar() を使用して積み上げ棒グラフを描画
            # x軸は1から始めるため、ind + 1 とします
            plt.bar(
                ind + 1, data[i], bottom=bottom_values, label=category, width=0.8
            )  # widthで棒の幅を調整
            bottom_values += data[i]  # 次のカテゴリの棒グラフの下限を更新

        plt.xlabel("Iteration")
        plt.ylabel("Weight")
        plt.title("Filter Bubble Evolution (Stacked Bar Chart)")

        # X軸の目盛りを整数にする
        tick_interval = 10
        plt.xticks(np.arange(0, num_iterations + 1, tick_interval))

        # Y軸の範囲を0から1にする（重みの合計は1なので）
        plt.ylim(0, 1)

        plt.legend(loc="upper left")  # 凡例の位置を調整
        plt.grid(axis="y", linestyle="--")  # Y軸にグリッド線を表示
        plt.tight_layout()  # レイアウトを調整
        plt.savefig("output/weight_progress_stacked_bar.png")  # ファイル名を変更
        plt.close()  # プロットを閉じる

        print("完了")
