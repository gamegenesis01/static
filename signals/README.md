# Accel Signals engine

Generates each trading day's signals before the market opens, checks them against hard risk limits,
writes them to a canonical file and records a SHA-256 fingerprint in an append-only log. Publishing
the fingerprint before the open builds a signal record anyone can check later.

Python 3.11+, standard library only.

## Daily use

Run before 9:30 am ET, with closing prices up to the previous trading day:

```bash
python -m accel_signals run --date 2026-11-18 --prices data/prices.csv --strategies example_momentum
```

It prints the fingerprint. Publish it straight away (website, public channel) with the date.

Check a stored day against its published fingerprint:

```bash
python -m accel_signals verify --date 2026-11-18
```

Score the record against prices that came in afterwards:

```bash
python -m accel_signals report --strategy example_momentum --prices data/prices.csv
```

Try the whole thing with synthetic test prices (not market data):

```bash
python -m accel_signals run --date 2026-11-18 --synthetic
```

## Price file

`date,instrument,close`, one row per instrument per trading day. The engine only lets a strategy see
prices from before the trade date.

## Adding the real strategies

Copy `accel_signals/strategies/example_momentum.py`, give it a `name`, a `version` and a
`generate(asof, prices)` method that returns one `Signal` per instrument, then add it to `REGISTRY`
in `accel_signals/strategies/__init__.py`. `example_momentum` is a placeholder with no claimed edge.

Bump `version` whenever the logic changes. A new version is treated as a new strategy with its own record.

## Rules the engine enforces

- Refuses to run after 9:30 am ET on the trade date.
- Refuses to overwrite a day that's already committed.
- Refuses to publish if any strategy breaks a limit: 40% per position, 100% gross, no shorts (edit `risk.Limits`).
- Strategies never see prices on or after the trade date.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Layout

```
accel_signals/model.py        Signal and SignalBatch
accel_signals/fingerprint.py  canonical JSON, SHA-256, commitment log, verify
accel_signals/risk.py         hard limits
accel_signals/data.py         CSV loader, synthetic test prices
accel_signals/strategies/     strategy plug-ins (example only for now)
accel_signals/performance.py  paper record: returns, Sharpe, drawdown
accel_signals/cli.py          run / verify / report / log
docs/delivery-spec.md         draft of what licensees would receive
```

`output/` holds the signal files and `commitments.jsonl`. Keep it in write-once storage; it's
git-ignored here so test runs never mix with the real record.
