"""Core data types for a day's signals."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date


@dataclass(frozen=True)
class Signal:
    """One target position for one instrument, from one strategy, for one day.

    target_weight is the fraction of the strategy's capital to hold at the
    next open: +0.25 means 25% long, -0.10 means 10% short, 0 means flat.
    """

    strategy: str
    instrument: str
    target_weight: float

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class SignalBatch:
    """All signals for one trading day, plus the facts needed to audit them."""

    trade_date: date
    generated_at: str  # ISO 8601 timestamp with timezone, e.g. 2026-11-17T08:45:00-05:00
    model_versions: dict[str, str]
    signals: list[Signal] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "trade_date": self.trade_date.isoformat(),
            "generated_at": self.generated_at,
            "model_versions": dict(sorted(self.model_versions.items())),
            "signals": [
                s.as_dict()
                for s in sorted(self.signals, key=lambda s: (s.strategy, s.instrument))
            ],
        }

    def for_strategy(self, name: str) -> list[Signal]:
        return [s for s in self.signals if s.strategy == name]
