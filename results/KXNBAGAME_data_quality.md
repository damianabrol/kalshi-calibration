# KXNBAGAME: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 3,062 (historical endpoint 2,898, live endpoint 164)
- Binary and settled YES/NO: 3,056
- Events: 1,528; markets per event: 2 -> 1,528 events
- Markets dropped, not open at T-24h: 30 (1.0%)
- Markets dropped, no trade by T-24h: 19 (0.6%)
- **Analyzed: 1,498 markets in 1,498 events**
- Close dates covered: 2025-04-16 to 2026-10-23

## Market lifespan (hours from open to close), by year of close
- 2025: median 58h (1,240 markets), 2026: median 59h (1,816 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 39,976, p10 593,973, p25 1,233,563, p50 2,524,192, p75 4,594,912, p90 7,876,661, p100 111,797,632
- Markets kept at each minimum-volume threshold:
  - >= 100: 1,498 (100.0%)
  - >= 1,000: 1,498 (100.0%)
  - >= 10,000: 1,498 (100.0%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 0.6h
  - <= 1h: 1,466 (97.9%)
  - 1-3h: 25 (1.7%)
  - 3-6h: 6 (0.4%)
  - 6-12h: 1 (0.1%)
  - > 12h: 0 (0.0%)

## Thin: contracts traded in the hour that set the price
- Median: 780
  - < 10: 41 (2.7%)
  - 10-99: 201 (13.4%)
  - 100-999: 586 (39.1%)
  - 1,000-9,999: 534 (35.6%)
  - 10,000+: 136 (9.1%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 9,944
  - < 10: 5 (0.3%)
  - 10-99: 11 (0.7%)
  - 100-999: 67 (4.5%)
  - 1,000-9,999: 669 (44.7%)
  - 10,000+: 746 (49.8%)

## Quotes at the snapshot
- Median bid-ask spread: 1¢
  - <= 2¢: 1,305 (87.1%)
  - 3-5¢: 163 (10.9%)
  - 6-10¢: 12 (0.8%)
  - > 10¢: 18 (1.2%)
- Last trade price outside the bid-ask at the snapshot: 85 (5.7%)
  (a sign the trade price is out of date relative to current quotes)
