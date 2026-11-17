"""Strategy plug-ins.

A strategy is any object with:
    name: str               short id, e.g. "core"
    version: str            bump whenever the logic changes; a new version starts a new record
    generate(asof, prices)  -> list[Signal] using only prices before `asof`

Register real strategies in REGISTRY. The example below exists so the pipeline
runs end to end; replace it with the real Accel models.
"""

from __future__ import annotations

from .example_momentum import ExampleMomentum

REGISTRY = {
    "example_momentum": ExampleMomentum,
}


def load(names: list[str]):
    missing = [n for n in names if n not in REGISTRY]
    if missing:
        raise KeyError(f"Unknown strategies: {', '.join(missing)}. Known: {', '.join(REGISTRY)}")
    return [REGISTRY[n]() for n in names]
