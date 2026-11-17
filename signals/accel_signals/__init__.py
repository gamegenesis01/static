"""Accel Signals: daily signal generation with pre-open fingerprints.

Every trading day, before the market opens, the engine:
  1. runs each registered strategy to produce target portfolio weights,
  2. checks them against hard risk limits,
  3. writes them to a canonical JSON file, and
  4. records a SHA-256 fingerprint of that file in an append-only commitment log.

Publishing the fingerprint before the open lets anyone later prove the signals
were not changed after the fact.
"""

__version__ = "0.1.0"
