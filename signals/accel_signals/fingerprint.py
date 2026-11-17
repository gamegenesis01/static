"""Canonical serialisation, SHA-256 fingerprints and the append-only commitment log."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .model import SignalBatch

WEIGHT_DECIMALS = 6


def _round_weights(obj):
    if isinstance(obj, dict):
        return {k: (round(v, WEIGHT_DECIMALS) if k == "target_weight" else _round_weights(v))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round_weights(v) for v in obj]
    return obj


def canonical_bytes(batch: SignalBatch) -> bytes:
    """The exact bytes that get fingerprinted.

    Sorted keys, no extra whitespace, signals sorted by strategy then instrument,
    weights rounded to 6 decimals. The same batch always gives the same bytes.
    """
    payload = _round_weights(batch.as_dict())
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def fingerprint(batch: SignalBatch) -> str:
    return hashlib.sha256(canonical_bytes(batch)).hexdigest()


def batch_path(out_dir: Path, batch: SignalBatch) -> Path:
    return out_dir / batch.trade_date.isoformat() / "signals.json"


def write_batch(out_dir: Path, batch: SignalBatch) -> Path:
    """Write the canonical file. Refuses to overwrite a day that already exists."""
    path = batch_path(out_dir, batch)
    if path.exists():
        raise FileExistsError(
            f"Signals for {batch.trade_date} already exist at {path}. "
            "A committed day is never rewritten; investigate instead."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(batch))
    return path


def append_commitment(log_path: Path, batch: SignalBatch, digest: str) -> dict:
    """Append one line to the commitment log (JSON Lines). Earlier lines are never edited."""
    record = {
        "trade_date": batch.trade_date.isoformat(),
        "committed_at": batch.generated_at,
        "sha256": digest,
        "signal_count": len(batch.signals),
        "strategies": sorted(batch.model_versions),
    }
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            if line.strip() and json.loads(line)["trade_date"] == record["trade_date"]:
                raise ValueError(f"{record['trade_date']} is already in the commitment log.")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def verify_day(out_dir: Path, log_path: Path, trade_date: str) -> tuple[bool, str]:
    """Re-hash a stored day and compare it with the published commitment."""
    path = out_dir / trade_date / "signals.json"
    if not path.exists():
        return False, f"No signal file for {trade_date}."
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    for line in log_path.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if rec["trade_date"] == trade_date:
            if rec["sha256"] == actual:
                return True, f"{trade_date}: match ({actual[:12]}…)"
            return False, f"{trade_date}: MISMATCH, published {rec['sha256'][:12]}… but file hashes to {actual[:12]}…"
    return False, f"{trade_date}: no commitment found in the log."
