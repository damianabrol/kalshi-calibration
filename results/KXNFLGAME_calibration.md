# KXNFLGAME: calibration 24h before close

- Analyzed: favorite side of 387 games (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, Wilson
- Close dates: 2025-09-05 to 2026-10-27
- Average price: 67.2¢ | Share resolved YES: 65.1% (95% CI 60.2% – 69.7%)
- Brier score: 0.2189 (reference, always predicting 65.1%: 0.2271; lower is better)
- Bins where the average price is inside the 95% CI: 5 of 5

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 50-59¢ | 111 | 111 | 55.5¢ | 57.7% | 48.4% – 66.4% | +2.1 |
| 60-69¢ | 119 | 119 | 63.8¢ | 60.5% | 51.5% – 68.8% | -3.3 |
| 70-79¢ | 102 | 102 | 74.4¢ | 71.6% | 62.2% – 79.4% | -2.9 |
| 80-89¢ | 50 | 50 | 84.2¢ | 76.0% | 62.6% – 85.7% | -8.2 |
| 90-99¢ | 5 | 5 | 90.6¢ | 100.0% | 56.6% – 100.0% | +9.4 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 385 (2 removed)
- Brier score: 0.2180 (main: 0.2189)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 50-59¢ | 111 | +2.1 | 110 | +1.8 |
| 60-69¢ | 119 | -3.3 | 119 | -3.3 |
| 70-79¢ | 102 | -2.9 | 101 | -2.1 |
| 80-89¢ | 50 | -8.2 | 50 | -8.2 |
| 90-99¢ | 5 | +9.4 | 5 | +9.4 |
