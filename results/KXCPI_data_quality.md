# KXCPI: data quality of the T-24h snapshot price

## Funnel
- Settled markets pulled: 522 (historical endpoint 493, live endpoint 29)
- Binary and settled YES/NO: 522
- Events: 64; markets per event: 1 -> 4 events, 3 -> 2 events, 4 -> 3 events, 5 -> 2 events, 6 -> 8 events, 7 -> 8 events, 8 -> 11 events, 9 -> 7 events, 10 -> 2 events, 11 -> 4 events, 12 -> 6 events, 13 -> 2 events, 14 -> 2 events, 15 -> 3 events
- Markets dropped, no trade by T-24h: 32 (6.1%)
- **Analyzed: 490 markets in 64 events**
- Close dates covered: 2021-07-12 to 2026-10-14

## Market lifespan (hours from open to close), by year of close
- 2021: median 678h (10 markets), 2022: median 1,918h (111 markets), 2023: median 5,349h (125 markets), 2024: median 1,460h (92 markets), 2025: median 1,462h (77 markets), 2026: median 1,363h (107 markets)

## Lifetime volume (contracts), analyzed markets
- Percentiles: p0 1, p10 217, p25 4,805, p50 19,630, p75 44,933, p90 132,396, p100 785,062
- Markets kept at each minimum-volume threshold:
  - >= 100: 456 (93.1%)
  - >= 1,000: 423 (86.3%)
  - >= 10,000: 321 (65.5%)

## Stale: hours between the last trade and the snapshot
Measured from the end of the hourly candle containing the last trade, so the true
age of the trade is up to 1 hour more than shown.
- Median: 12.5h
  - <= 1h: 37 (7.6%)
  - 1-3h: 22 (4.5%)
  - 3-6h: 25 (5.1%)
  - 6-12h: 143 (29.2%)
  - > 12h: 263 (53.7%)

## Thin: contracts traded in the hour that set the price
- Median: 100
  - < 10: 92 (18.8%)
  - 10-99: 150 (30.6%)
  - 100-999: 190 (38.8%)
  - 1,000-9,999: 56 (11.4%)
  - 10,000+: 2 (0.4%)

## Activity: contracts traded in the 24h before the snapshot
- Median: 386
  - < 10: 171 (34.9%)
  - 10-99: 30 (6.1%)
  - 100-999: 96 (19.6%)
  - 1,000-9,999: 160 (32.7%)
  - 10,000+: 33 (6.7%)

## Quotes at the snapshot
- Median bid-ask spread: 2¢
  - <= 2¢: 257 (52.4%)
  - 3-5¢: 173 (35.3%)
  - 6-10¢: 42 (8.6%)
  - > 10¢: 18 (3.7%)
- Last trade price outside the bid-ask at the snapshot: 63 (12.9%)
  (a sign the trade price is out of date relative to current quotes)
