import random

def sample_category(weights: dict[str, float]) -> str:
    categories = list(weights.keys())
    probs = list(weights.values())
    return random.choices(categories, weights=probs, k=1)[0]

def update_weights(weights: dict[str, float], clicked_category: str, boost: float = 0.1):
    for category in weights:
        if category == clicked_category:
            weights[category] += boost
        else:
            weights[category] *= 0.9  # 減衰
    total = sum(weights.values())
    for category in weights:
        weights[category] /= total
