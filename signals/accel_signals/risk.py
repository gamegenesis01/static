"""Hard pre-publication risk limits. A batch that breaks any limit is not published."""

from __future__ import annotations

from dataclasses import dataclass

from .model import Signal


@dataclass(frozen=True)
class Limits:
    max_abs_weight: float = 0.40   # largest single position, as a fraction of capital
    max_gross: float = 1.00        # sum of absolute weights (1.0 = no leverage)
    max_net: float = 1.00          # long minus short
    allow_short: bool = False


class LimitBreach(Exception):
    pass


def check(strategy: str, signals: list[Signal], limits: Limits) -> None:
    """Raise LimitBreach with every broken rule listed. Returns None when all pass."""
    problems = []
    gross = sum(abs(s.target_weight) for s in signals)
    net = sum(s.target_weight for s in signals)
    for s in signals:
        if abs(s.target_weight) > limits.max_abs_weight + 1e-9:
            problems.append(f"{s.instrument} weight {s.target_weight:.4f} exceeds {limits.max_abs_weight:.2f}")
        if s.target_weight < 0 and not limits.allow_short:
            problems.append(f"{s.instrument} is short ({s.target_weight:.4f}) but shorting is not allowed")
    if gross > limits.max_gross + 1e-9:
        problems.append(f"gross exposure {gross:.4f} exceeds {limits.max_gross:.2f}")
    if abs(net) > limits.max_net + 1e-9:
        problems.append(f"net exposure {net:.4f} exceeds {limits.max_net:.2f}")
    if problems:
        raise LimitBreach(f"{strategy}: " + "; ".join(problems))
