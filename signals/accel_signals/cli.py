"""Command line: run a day, run a date range (for testing), verify, and show the log.

    python -m accel_signals run --date 2026-11-18 --prices data/prices.csv --strategies core momentum
    python -m accel_signals run --date 2026-11-18 --synthetic
    python -m accel_signals verify --date 2026-11-18
    python -m accel_signals log
    python -m accel_signals report --strategy core --prices data/prices.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from . import data, fingerprint, performance, risk, strategies
from .model import SignalBatch

ET = ZoneInfo("America/New_York")


def build_batch(trade_date: date, prices, names: list[str], limits: risk.Limits, now: datetime | None = None) -> SignalBatch:
    now = now or datetime.now(ET)
    strats = strategies.load(names)
    batch = SignalBatch(
        trade_date=trade_date,
        generated_at=now.astimezone(ET).isoformat(timespec="seconds"),
        model_versions={s.name: s.version for s in strats},
    )
    for s in strats:
        sigs = s.generate(trade_date, prices)
        risk.check(s.name, sigs, limits)
        batch.signals.extend(sigs)
    return batch


def publish(batch: SignalBatch, out_dir: Path, log_path: Path) -> dict:
    digest = fingerprint.fingerprint(batch)
    fingerprint.write_batch(out_dir, batch)
    return fingerprint.append_commitment(log_path, batch, digest)


def _prices(args, trade_date: date):
    if args.synthetic:
        return data.synthetic(trade_date - timedelta(days=400), trade_date)
    if not args.prices:
        sys.exit("Give --prices path/to/prices.csv, or --synthetic for a test run.")
    return data.load_csv(Path(args.prices))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="accel_signals", description="Accel Signals daily engine")
    p.add_argument("--out", default="output", help="where signal files and the commitment log live")
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="generate, check, write and commit one trading day")
    run.add_argument("--date", required=True, help="trade date the signals are for, YYYY-MM-DD")
    run.add_argument("--prices", help="CSV of closing prices (date,instrument,close)")
    run.add_argument("--synthetic", action="store_true", help="use synthetic test prices")
    run.add_argument("--strategies", nargs="+", default=["example_momentum"])
    run.add_argument("--allow-after-open", action="store_true",
                     help="only for back-filling tests: skip the before-9:30-ET check")

    ver = sub.add_parser("verify", help="re-hash a stored day and compare with its commitment")
    ver.add_argument("--date", required=True)

    sub.add_parser("log", help="print the commitment log")

    rep = sub.add_parser("report", help="score committed signals against later prices (paper record)")
    rep.add_argument("--strategy", default="example_momentum")
    rep.add_argument("--prices", help="CSV of closing prices")
    rep.add_argument("--synthetic", action="store_true")
    rep.add_argument("--date", default=date.today().isoformat(), help="price data end date for --synthetic")

    args = p.parse_args(argv)
    out_dir = Path(args.out)
    log_path = out_dir / "commitments.jsonl"

    if args.cmd == "run":
        trade_date = date.fromisoformat(args.date)
        now = datetime.now(ET)
        open_time = datetime.combine(trade_date, datetime.min.time(), ET).replace(hour=9, minute=30)
        if now >= open_time and not args.allow_after_open:
            sys.exit(f"Refusing: it is already past 9:30 ET on {trade_date}. "
                     "Signals must be committed before the open.")
        batch = build_batch(trade_date, _prices(args, trade_date), args.strategies, risk.Limits(), now)
        record = publish(batch, out_dir, log_path)
        print(json.dumps(record, indent=2))
        print("Publish this sha256 now, before the open.")
        return 0

    if args.cmd == "verify":
        ok, msg = fingerprint.verify_day(out_dir, log_path, args.date)
        print(msg)
        return 0 if ok else 1

    if args.cmd == "report":
        prices = _prices(args, date.fromisoformat(args.date))
        stats = performance.summary(performance.daily_returns(out_dir, prices, args.strategy))
        print(json.dumps(stats, indent=2))
        return 0

    if args.cmd == "log":
        print(log_path.read_text() if log_path.exists() else "(no commitments yet)")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
