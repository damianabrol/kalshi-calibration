# KXMLBGAME: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 9,380 (historical endpoint 8,324, live endpoint 1,056)
- Binary and settled YES/NO: 9,358
- Events: 4,679; markets per event: 2 -> 4,679 events
- Markets dropped, not open at T-24h: 4,254 (45.5%)
- Markets dropped, no trade by T-24h: 28 (0.3%)
- **Analyzed: 2,536 markets in 2,536 events**
- Close dates covered: 2025-04-25 to 2026-10-20

## Market lifespan (hours from open to close), by year of close
- 2025: median 14h (4,414 markets), 2026: median 75h (4,944 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 5, p10 618,008, p25 1,023,309, p50 1,688,215, p75 2,794,460, p90 4,314,804, p100 19,083,386
- Markets kept at each minimum-volume threshold:
  - >= 100: 2,532 (99.8%)
  - >= 1,000: 2,529 (99.7%)
  - >= 10,000: 2,529 (99.7%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 0.5h
  - <= 1h: 2,388 (94.2%)
  - 1-3h: 124 (4.9%)
  - 3-6h: 15 (0.6%)
  - 6-12h: 1 (0.0%)
  - > 12h: 8 (0.3%)

## Thin: contracts traded in the hour that set the price
- Median: 321
  - < 10: 187 (7.4%)
  - 10-99: 560 (22.1%)
  - 100-999: 1,055 (41.6%)
  - 1,000-9,999: 622 (24.5%)
  - 10,000+: 112 (4.4%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 3,099
  - < 10: 10 (0.4%)
  - 10-99: 22 (0.9%)
  - 100-999: 491 (19.4%)
  - 1,000-9,999: 1,485 (58.6%)
  - 10,000+: 528 (20.8%)

## Quotes at the snapshot
- Median bid-ask spread: 1¢
  - <= 2¢: 2,469 (97.4%)
  - 3-5¢: 51 (2.0%)
  - 6-10¢: 5 (0.2%)
  - > 10¢: 11 (0.4%)
- Last trade price outside the bid-ask at the snapshot: 93 (3.7%)
  (a sign the trade price is out of date relative to current quotes)
