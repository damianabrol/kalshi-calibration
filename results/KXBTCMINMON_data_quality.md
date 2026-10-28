# KXBTCMINMON: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 86 (historical endpoint 59, live endpoint 27)
- Binary and settled YES/NO: 86
- Events: 10; markets per event: 1 -> 1 events, 8 -> 7 events, 11 -> 1 events, 18 -> 1 events
- Markets dropped, closed before T-24h: 21 (24.4%)
- Markets dropped, no trade by T-24h: 3 (3.5%)
- **Analyzed: 62 markets in 9 events**
- Close dates covered: 2026-01-31 to 2026-10-01

## Market lifespan (hours from open to close), by year of close
- 2026: median 716h (86 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 2,106, p10 24,096, p25 43,088, p50 91,587, p75 181,189, p90 400,816, p100 1,142,304
- Markets kept at each minimum-volume threshold:
  - >= 100: 62 (100.0%)
  - >= 1,000: 62 (100.0%)
  - >= 10,000: 58 (93.5%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 7.5h
  - <= 1h: 15 (24.2%)
  - 1-3h: 5 (8.1%)
  - 3-6h: 9 (14.5%)
  - 6-12h: 13 (21.0%)
  - > 12h: 20 (32.3%)

## Thin: contracts traded in the hour that set the price
- Median: 294
  - < 10: 4 (6.5%)
  - 10-99: 17 (27.4%)
  - 100-999: 22 (35.5%)
  - 1,000-9,999: 19 (30.6%)
  - 10,000+: 0 (0.0%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 947
  - < 10: 16 (25.8%)
  - 10-99: 5 (8.1%)
  - 100-999: 10 (16.1%)
  - 1,000-9,999: 17 (27.4%)
  - 10,000+: 14 (22.6%)

## Quotes at the snapshot
- Median bid-ask spread: 1¢
  - <= 2¢: 62 (100.0%)
  - 3-5¢: 0 (0.0%)
  - 6-10¢: 0 (0.0%)
  - > 10¢: 0 (0.0%)
- Last trade price outside the bid-ask at the snapshot: 6 (9.7%)
  (a sign the trade price is out of date relative to current quotes)
