# KXAPRPOTUS: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 2,001 (historical endpoint 1,937, live endpoint 64)
- Binary and settled YES/NO: 2,001
- Events: 260; markets per event: 1 -> 16 events, 3 -> 10 events, 4 -> 1 events, 6 -> 31 events, 8 -> 55 events, 9 -> 145 events, 10 -> 2 events
- Markets dropped, no trade by T-24h: 145 (7.2%)
- **Analyzed: 1,856 markets in 259 events**
- Close dates covered: 2021-10-15 to 2026-10-16

## Market lifespan (hours from open to close), by year of close
- 2021: median 174h (12 markets), 2022: median 145h (381 markets), 2023: median 145h (468 markets), 2024: median 145h (468 markets), 2025: median 166h (344 markets), 2026: median 167h (328 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 1, p10 119, p25 409, p50 1,258, p75 4,672, p90 13,930, p100 132,730
- Markets kept at each minimum-volume threshold:
  - >= 100: 1,710 (92.1%)
  - >= 1,000: 1,019 (54.9%)
  - >= 10,000: 253 (13.6%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 2.0h
  - <= 1h: 873 (47.0%)
  - 1-3h: 215 (11.6%)
  - 3-6h: 24 (1.3%)
  - 6-12h: 100 (5.4%)
  - > 12h: 644 (34.7%)

## Thin: contracts traded in the hour that set the price
- Median: 56
  - < 10: 276 (14.9%)
  - 10-99: 832 (44.8%)
  - 100-999: 673 (36.3%)
  - 1,000-9,999: 74 (4.0%)
  - 10,000+: 1 (0.1%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 242
  - < 10: 431 (23.2%)
  - 10-99: 271 (14.6%)
  - 100-999: 663 (35.7%)
  - 1,000-9,999: 465 (25.1%)
  - 10,000+: 26 (1.4%)

## Quotes at the snapshot
- Median bid-ask spread: 3¢
  - <= 2¢: 778 (41.9%)
  - 3-5¢: 555 (29.9%)
  - 6-10¢: 256 (13.8%)
  - > 10¢: 267 (14.4%)
- Last trade price outside the bid-ask at the snapshot: 515 (27.7%)
  (a sign the trade price is out of date relative to current quotes)
