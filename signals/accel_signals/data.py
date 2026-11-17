"""Price data: a CSV loader for real data and a synthetic generator for testing the pipeline.

CSV format (one row per instrument per day, closing prices):
    date,instrument,close
    2026-11-14,SPY,601.25
"""

from __future__ import annotations

import csv
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

Prices = dict[str, list[tuple[date, float]]]  # instrument -> [(date, close)] oldest first


def load_csv(path: Path) -> Prices:
    series: dict[str, list[tuple[date, float]]] = defaultdict(list)
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            series[row["instrument"]].append((date.fromisoformat(row["date"]), float(row["close"])))
    return {k: sorted(v) for k, v in series.items()}


def up_to(prices: Prices, asof: date) -> Prices:
    """Only data strictly before the trade date, so a strategy can never see the future."""
    return {k: [(d, p) for d, p in v if d < asof] for k, v in prices.items()}


def trading_days(start: date, end: date) -> list[date]:
    days, d = [], start
    while d <= end:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return days


def synthetic(start: date, end: date, seed: int = 7) -> Prices:
    """Deterministic random-walk prices. FOR TESTING ONLY: not market data."""
    rng = random.Random(seed)
    spec = {  # instrument: (start price, yearly drift, yearly volatility)
        "US_EQ": (100.0, 0.08, 0.18),
        "INTL_EQ": (100.0, 0.05, 0.20),
        "BONDS": (100.0, 0.03, 0.07),
        "GOLD": (100.0, 0.04, 0.15),
        "CASH": (100.0, 0.04, 0.005),
    }
    days = trading_days(start, end)
    out: Prices = {}
    for name, (p0, mu, vol) in spec.items():
        p, series = p0, []
        for d in days:
            shock = rng.gauss(0, 1)
            p *= math.exp((mu - 0.5 * vol * vol) / 252 + vol / math.sqrt(252) * shock)
            series.append((d, round(p, 4)))
        out[name] = series
    return out
