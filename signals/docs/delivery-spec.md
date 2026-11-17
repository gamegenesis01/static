# Accel Signals delivery spec (draft v0.1)

This is the draft of what a future licensee would receive. **It is not an offer.** Accel Signals
will only be offered after the trading record is independently verified and the management
company's adviser setup is in place.

## What a licensee receives

| Item | When | Format |
| --- | --- | --- |
| Target weights per strategy | Every trading day by 9:00 am ET | JSON file and HTTPS API |
| Fingerprint of the day's file | Same time, also published publicly | SHA-256 hex string |
| Monthly report | First business day of the month | PDF + CSV |
| Model change notice | At least 5 trading days before a change trades | Email + API notice |

## Daily file

Exactly the canonical file the engine writes (`output/YYYY-MM-DD/signals.json`):

```json
{
  "trade_date": "2026-11-18",
  "generated_at": "2026-11-18T08:45:00-05:00",
  "model_versions": {"core": "1.0.0", "momentum": "1.0.0"},
  "signals": [
    {"strategy": "core", "instrument": "US_EQ", "target_weight": 0.35}
  ]
}
```

- `target_weight` is the fraction of the capital the licensee allocates to that strategy.
- Instruments the strategy doesn't hold that day are listed with weight 0, so every file is complete.
- The licensee checks the file by hashing its exact bytes with SHA-256 and comparing to the published fingerprint.

## Planned API (not built yet)

| Method | Path | Returns |
| --- | --- | --- |
| GET | `/v1/signals/{date}` | The day's file, byte for byte |
| GET | `/v1/commitments?from=&to=` | Commitment log entries |
| GET | `/v1/reports/{yyyy-mm}` | Monthly report |

Authentication by per-client API key; each client sees only the strategies it licenses.

## Capacity and terms (to confirm with counsel)

- Each license covers a maximum amount of capital following the signals.
- Total capital across the fund and all licensees stays under the measured capacity.
- No resale or redistribution; signals are confidential until 30 days after their trade date.
