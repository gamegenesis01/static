import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from accel_signals import cli, data, fingerprint, performance, risk  # noqa: E402
from accel_signals.model import Signal, SignalBatch  # noqa: E402

ET = ZoneInfo("America/New_York")
PRICES = data.synthetic(date(2025, 6, 2), date(2026, 11, 13))


def batch_for(d: date) -> SignalBatch:
    now = datetime.combine(d, datetime.min.time(), ET).replace(hour=8, minute=45)
    return cli.build_batch(d, PRICES, ["example_momentum"], risk.Limits(), now)


class FingerprintTests(unittest.TestCase):
    def test_same_batch_same_hash(self):
        a, b = batch_for(date(2026, 11, 10)), batch_for(date(2026, 11, 10))
        self.assertEqual(fingerprint.fingerprint(a), fingerprint.fingerprint(b))

    def test_signal_order_does_not_change_hash(self):
        a = batch_for(date(2026, 11, 10))
        b = batch_for(date(2026, 11, 10))
        b.signals.reverse()
        self.assertEqual(fingerprint.fingerprint(a), fingerprint.fingerprint(b))

    def test_any_weight_change_changes_hash(self):
        a = batch_for(date(2026, 11, 10))
        b = batch_for(date(2026, 11, 10))
        s = b.signals[0]
        b.signals[0] = Signal(s.strategy, s.instrument, s.target_weight + 0.0001)
        self.assertNotEqual(fingerprint.fingerprint(a), fingerprint.fingerprint(b))

    def test_publish_verify_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, log = Path(tmp), Path(tmp) / "commitments.jsonl"
            cli.publish(batch_for(date(2026, 11, 10)), out, log)
            ok, _ = fingerprint.verify_day(out, log, "2026-11-10")
            self.assertTrue(ok)
            path = out / "2026-11-10" / "signals.json"
            doc = json.loads(path.read_text())
            doc["signals"][0]["target_weight"] = 0.123
            path.write_text(json.dumps(doc, sort_keys=True, separators=(",", ":")))
            ok, msg = fingerprint.verify_day(out, log, "2026-11-10")
            self.assertFalse(ok)
            self.assertIn("MISMATCH", msg)

    def test_a_committed_day_cannot_be_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, log = Path(tmp), Path(tmp) / "commitments.jsonl"
            cli.publish(batch_for(date(2026, 11, 10)), out, log)
            with self.assertRaises(FileExistsError):
                cli.publish(batch_for(date(2026, 11, 10)), out, log)


class NoLookaheadTests(unittest.TestCase):
    def test_strategy_ignores_prices_on_or_after_trade_date(self):
        d = date(2026, 11, 10)
        future = {k: v + [(d + timedelta(days=i), 1e9) for i in range(0, 5)] for k, v in data.up_to(PRICES, d).items()}
        normal = batch_for(d)
        poisoned = cli.build_batch(d, future, ["example_momentum"], risk.Limits(), datetime.fromisoformat(normal.generated_at))
        self.assertEqual(fingerprint.fingerprint(normal), fingerprint.fingerprint(poisoned))


class RiskTests(unittest.TestCase):
    def test_example_strategy_passes_limits(self):
        for d in data.trading_days(date(2026, 10, 1), date(2026, 11, 13)):
            batch_for(d)  # raises on any breach

    def test_breaches_are_reported(self):
        sigs = [Signal("x", "A", 0.6), Signal("x", "B", 0.6), Signal("x", "C", -0.1)]
        with self.assertRaises(risk.LimitBreach) as ctx:
            risk.check("x", sigs, risk.Limits())
        msg = str(ctx.exception)
        self.assertIn("A weight", msg)
        self.assertIn("gross exposure", msg)
        self.assertIn("short", msg)


class PerformanceTests(unittest.TestCase):
    def test_report_over_backfilled_days(self):
        with tempfile.TemporaryDirectory() as tmp:
            out, log = Path(tmp), Path(tmp) / "commitments.jsonl"
            for d in data.trading_days(date(2026, 9, 1), date(2026, 11, 13)):
                cli.publish(batch_for(d), out, log)
            stats = performance.summary(performance.daily_returns(out, PRICES, "example_momentum"))
            self.assertGreater(stats["days"], 40)
            self.assertLessEqual(stats["max_drawdown"], 0)
            for line in log.read_text().splitlines():
                ok, _ = fingerprint.verify_day(out, log, json.loads(line)["trade_date"])
                self.assertTrue(ok)


class CliGuardTests(unittest.TestCase):
    def test_refuses_after_the_open(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                cli.main(["--out", tmp, "run", "--date", "2020-01-02", "--synthetic"])


if __name__ == "__main__":
    unittest.main()
