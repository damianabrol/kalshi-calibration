# KXNBAGAME: calibration 24h before close

- Analyzed: favorite side of 1,498 games (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, Wilson
- Close dates: 2025-04-16 to 2026-10-23
- Average price: 69.4¢ | Share resolved YES: 66.4% (95% CI 63.9% – 68.7%)
- Brier score: 0.2058 (reference, always predicting 66.4%: 0.2233; lower is better)
- Bins where the average price is inside the 95% CI: 3 of 5

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 50-59¢ | 362 | 362 | 55.1¢ | 49.4% | 44.3% – 54.6% | -5.6 |
| 60-69¢ | 453 | 453 | 64.5¢ | 60.0% | 55.5% – 64.5% | -4.5 |
| 70-79¢ | 341 | 341 | 74.2¢ | 74.8% | 69.9% – 79.1% | +0.6 |
| 80-89¢ | 260 | 260 | 84.4¢ | 80.8% | 75.5% – 85.1% | -3.7 |
| 90-99¢ | 82 | 82 | 91.8¢ | 95.1% | 88.1% – 98.1% | +3.3 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 1,410 (88 removed)
- Brier score: 0.2049 (main: 0.2058)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 50-59¢ | 362 | -5.6 | 343 | -6.4 |
| 60-69¢ | 453 | -4.5 | 427 | -4.6 |
| 70-79¢ | 341 | +0.6 | 317 | +0.8 |
| 80-89¢ | 260 | -3.7 | 243 | -3.5 |
| 90-99¢ | 82 | +3.3 | 80 | +4.4 |
