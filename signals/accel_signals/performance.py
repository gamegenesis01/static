"""Score committed signals against prices that arrived afterwards (a paper record).

Simplification: a signal for day D is held from the close of the previous trading
day to the close of D, with no trading costs. Real fills will differ; the live
trading record at Accel Trading is the one that counts for money.
"""

from __future__ import annotations

import json
import math
from datetime import date
from pathlib import Path

from .data import Prices


def daily_returns(out_dir: Path, prices: Prices, strategy: str) -> list[tuple[date, float]]:
    closes = {inst: dict(series) for inst, series in prices.items()}
    results = []
    for path in sorted(out_dir.glob("*/signals.json")):
        batch = json.loads(path.read_text())
        d = date.fromisoformat(batch["trade_date"])
        r, complete = 0.0, True
        for s in batch["signals"]:
            if s["strategy"] != strategy or s["target_weight"] == 0:
                continue
            series = closes.get(s["instrument"], {})
            prev = [x for x in series if x < d]
            if d not in series or not prev:
                complete = False
                break
            r += s["target_weight"] * (series[d] / series[max(prev)] - 1)
        if complete:
            results.append((d, r))
    return results


def summary(rets: list[tuple[date, float]]) -> dict:
    if not rets:
        return {"days": 0}
    values = [r for _, r in rets]
    equity, peak, max_dd = 1.0, 1.0, 0.0
    for r in values:
        equity *= 1 + r
        peak = max(peak, equity)
        max_dd = min(max_dd, equity / peak - 1)
    mean = sum(values) / len(values)
    sd = math.sqrt(sum((v - mean) ** 2 for v in values) / (len(values) - 1)) if len(values) > 1 else 0.0
    return {
        "days": len(values),
        "first": rets[0][0].isoformat(),
        "last": rets[-1][0].isoformat(),
        "total_return": round(equity - 1, 6),
        "annualised_vol": round(sd * math.sqrt(252), 6),
        "sharpe": round(mean / sd * math.sqrt(252), 3) if sd else None,
        "max_drawdown": round(max_dd, 6),
    }
