# KXNFLGAME: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 978 (historical endpoint 732, live endpoint 246)
- Binary and settled YES/NO: 964
- Events: 482; markets per event: 2 -> 482 events
- Markets dropped, preseason: 186 (19.3%)
- Markets dropped, no trade by T-24h: 4 (0.4%)
- **Analyzed: 387 markets in 387 events**
- Close dates covered: 2025-09-05 to 2026-10-27

## Market lifespan (hours from open to close), by year of close
- 2025: median 289h (602 markets), 2026: median 304h (362 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 541,845, p10 2,195,998, p25 3,674,657, p50 6,682,067, p75 13,210,644, p90 20,983,081, p100 51,836,141
- Markets kept at each minimum-volume threshold:
  - >= 100: 387 (100.0%)
  - >= 1,000: 387 (100.0%)
  - >= 10,000: 387 (100.0%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 0.3h
  - <= 1h: 387 (100.0%)
  - 1-3h: 0 (0.0%)
  - 3-6h: 0 (0.0%)
  - 6-12h: 0 (0.0%)
  - > 12h: 0 (0.0%)

## Thin: contracts traded in the hour that set the price
- Median: 2,585
  - < 10: 0 (0.0%)
  - 10-99: 6 (1.6%)
  - 100-999: 100 (25.8%)
  - 1,000-9,999: 198 (51.2%)
  - 10,000+: 83 (21.4%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 60,710
  - < 10: 0 (0.0%)
  - 10-99: 0 (0.0%)
  - 100-999: 0 (0.0%)
  - 1,000-9,999: 28 (7.2%)
  - 10,000+: 359 (92.8%)

## Quotes at the snapshot
- Median bid-ask spread: 1¢
  - <= 2¢: 386 (99.7%)
  - 3-5¢: 1 (0.3%)
  - 6-10¢: 0 (0.0%)
  - > 10¢: 0 (0.0%)
- Last trade price outside the bid-ask at the snapshot: 2 (0.5%)
  (a sign the trade price is out of date relative to current quotes)
