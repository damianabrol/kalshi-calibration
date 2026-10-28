# KXBTCMAXMON: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 93 (historical endpoint 62, live endpoint 31)
- Binary and settled YES/NO: 93
- Events: 10; markets per event: 1 -> 1 events, 8 -> 8 events, 28 -> 1 events
- Markets dropped, closed before T-24h: 23 (24.7%)
- **Analyzed: 70 markets in 9 events**
- Close dates covered: 2026-02-01 to 2026-10-01

## Market lifespan (hours from open to close), by year of close
- 2026: median 607h (93 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 231, p10 2,393, p25 38,462, p50 124,233, p75 372,387, p90 776,753, p100 1,799,444
- Markets kept at each minimum-volume threshold:
  - >= 100: 70 (100.0%)
  - >= 1,000: 66 (94.3%)
  - >= 10,000: 59 (84.3%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 4.0h
  - <= 1h: 14 (20.0%)
  - 1-3h: 19 (27.1%)
  - 3-6h: 8 (11.4%)
  - 6-12h: 3 (4.3%)
  - > 12h: 26 (37.1%)

## Thin: contracts traded in the hour that set the price
- Median: 149
  - < 10: 3 (4.3%)
  - 10-99: 28 (40.0%)
  - 100-999: 27 (38.6%)
  - 1,000-9,999: 12 (17.1%)
  - 10,000+: 0 (0.0%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 1,340
  - < 10: 13 (18.6%)
  - 10-99: 8 (11.4%)
  - 100-999: 12 (17.1%)
  - 1,000-9,999: 25 (35.7%)
  - 10,000+: 12 (17.1%)

## Quotes at the snapshot
- Median bid-ask spread: 1¢
  - <= 2¢: 70 (100.0%)
  - 3-5¢: 0 (0.0%)
  - 6-10¢: 0 (0.0%)
  - > 10¢: 0 (0.0%)
- Last trade price outside the bid-ask at the snapshot: 0 (0.0%)
  (a sign the trade price is out of date relative to current quotes)
