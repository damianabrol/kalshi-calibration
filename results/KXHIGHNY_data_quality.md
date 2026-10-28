# KXHIGHNY: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 9,784 (historical endpoint 9,418, live endpoint 366)
- Binary and settled YES/NO: 9,784
- Events: 1,899; markets per event: 1 -> 108 events, 2 -> 153 events, 4 -> 227 events, 5 -> 4 events, 6 -> 1,407 events
- Markets dropped, no trade by T-24h: 1,069 (10.9%)
- Markets dropped, not open at T-24h: 30 (0.3%)
- **Analyzed: 8,685 markets in 1,887 events**
- Close dates covered: 2021-08-07 to 2026-10-22

## Market lifespan (hours from open to close), by year of close
- 2021: median 38h (197 markets), 2022: median 38h (1,250 markets), 2023: median 38h (2,181 markets), 2024: median 38h (2,196 markets), 2025: median 38h (2,190 markets), 2026: median 39h (1,770 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 1, p10 386, p25 1,130, p50 3,161, p75 18,400, p90 49,414, p100 1,873,207
- Markets kept at each minimum-volume threshold:
  - >= 100: 8,284 (95.4%)
  - >= 1,000: 6,748 (77.7%)
  - >= 10,000: 2,943 (33.9%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 1.0h
  - <= 1h: 4,710 (54.2%)
  - 1-3h: 2,215 (25.5%)
  - 3-6h: 1,049 (12.1%)
  - 6-12h: 627 (7.2%)
  - > 12h: 84 (1.0%)

## Thin: contracts traded in the hour that set the price
- Median: 100
  - < 10: 1,233 (14.2%)
  - 10-99: 3,042 (35.0%)
  - 100-999: 3,958 (45.6%)
  - 1,000-9,999: 444 (5.1%)
  - 10,000+: 8 (0.1%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 842
  - < 10: 333 (3.8%)
  - 10-99: 843 (9.7%)
  - 100-999: 3,551 (40.9%)
  - 1,000-9,999: 3,836 (44.2%)
  - 10,000+: 122 (1.4%)

## Quotes at the snapshot
- Median bid-ask spread: 4¢
  - <= 2¢: 3,021 (34.8%)
  - 3-5¢: 2,958 (34.1%)
  - 6-10¢: 1,414 (16.3%)
  - > 10¢: 1,292 (14.9%)
- Last trade price outside the bid-ask at the snapshot: 1,802 (20.7%)
  (a sign the trade price is out of date relative to current quotes)
