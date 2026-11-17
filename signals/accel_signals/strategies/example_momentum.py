"""EXAMPLE strategy: simple long-only momentum with volatility scaling.

This is a placeholder that shows the shape of a strategy. It is not one of the
Accel models and has no claimed edge.
"""

from __future__ import annotations

import math
from datetime import date

from ..data import Prices, up_to
from ..model import Signal


class ExampleMomentum:
    name = "example_momentum"
    version = "0.1.0"

    lookback = 60      # trading days of past return used to rank
    vol_window = 20    # trading days used to estimate volatility
    top_n = 3          # how many instruments to hold
    max_weight = 0.40  # cap per position, matches the default risk limit

    def generate(self, asof: date, prices: Prices) -> list[Signal]:
        hist = up_to(prices, asof)
        scores = {}
        for inst, series in hist.items():
            closes = [p for _, p in series]
            if len(closes) <= max(self.lookback, self.vol_window):
                continue
            momentum = closes[-1] / closes[-1 - self.lookback] - 1
            rets = [math.log(closes[i] / closes[i - 1]) for i in range(len(closes) - self.vol_window, len(closes))]
            mean = sum(rets) / len(rets)
            vol = math.sqrt(sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)) * math.sqrt(252)
            if momentum > 0 and vol > 0:
                scores[inst] = (momentum, vol)

        chosen = sorted(scores, key=lambda k: scores[k][0], reverse=True)[: self.top_n]
        inv_vol = {k: 1 / scores[k][1] for k in chosen}
        total = sum(inv_vol.values())
        weights = {k: min(self.max_weight, v / total) for k, v in inv_vol.items()} if total else {}

        return [
            Signal(self.name, inst, round(weights.get(inst, 0.0), 6))
            for inst in sorted(hist)
        ]
