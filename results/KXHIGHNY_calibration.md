# KXHIGHNY: calibration 24h before close

- Analyzed: 6,748 markets in 1,778 events (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, event bootstrap
- Close dates: 2021-08-07 to 2026-10-22
- Average price: 23.9¢ | Share resolved YES: 22.7% (95% CI 20.8% – 24.7%)
- Brier score: 0.1387 (reference, always predicting 22.7%: 0.1756; lower is better)
- Bins where the average price is inside the 95% CI: 10 of 10

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 0-9¢ | 2,185 | 1,030 | 3.7¢ | 2.7% | 1.9% – 3.9% | -0.9 |
| 10-19¢ | 1,130 | 934 | 14.0¢ | 13.9% | 11.8% – 16.3% | -0.1 |
| 20-29¢ | 911 | 713 | 24.3¢ | 23.9% | 20.9% – 27.2% | -0.4 |
| 30-39¢ | 1,002 | 857 | 34.4¢ | 32.9% | 29.9% – 36.2% | -1.5 |
| 40-49¢ | 796 | 692 | 44.2¢ | 40.8% | 37.2% – 44.5% | -3.4 |
| 50-59¢ | 402 | 399 | 53.6¢ | 52.0% | 47.0% – 56.8% | -1.6 |
| 60-69¢ | 146 | 146 | 64.2¢ | 67.8% | 59.9% – 75.3% | +3.6 |
| 70-79¢ | 83 | 83 | 74.9¢ | 72.3% | 61.8% – 81.6% | -2.6 |
| 80-89¢ | 57 | 57 | 84.8¢ | 77.2% | 64.8% – 88.0% | -7.6 |
| 90-99¢ | 36 | 34 | 94.4¢ | 86.1% | 70.8% – 96.9% | -8.2 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 4,798 (1,950 removed)
- Brier score: 0.1335 (main: 0.1387)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 0-9¢ | 2,185 | -0.9 | 1,650 | -0.9 |
| 10-19¢ | 1,130 | -0.1 | 806 | -0.3 |
| 20-29¢ | 911 | -0.4 | 605 | +0.0 |
| 30-39¢ | 1,002 | -1.5 | 667 | -0.4 |
| 40-49¢ | 796 | -3.4 | 550 | -3.2 |
| 50-59¢ | 402 | -1.6 | 283 | +0.9 |
| 60-69¢ | 146 | +3.6 | 107 | +4.9 |
| 70-79¢ | 83 | -2.6 | 67 | -3.2 |
| 80-89¢ | 57 | -7.6 | 37 | +1.8 |
| 90-99¢ | 36 | -8.2 | 26 | +2.0 |
