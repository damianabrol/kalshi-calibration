# KXMLBGAME: calibration 24h before close

- Analyzed: favorite side of 2,529 games (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, Wilson
- Close dates: 2025-04-25 to 2026-10-20
- Average price: 57.0¢ | Share resolved YES: 55.9% (95% CI 54.0% – 57.8%)
- Brier score: 0.2441 (reference, always predicting 55.9%: 0.2465; lower is better)
- Bins where the average price is inside the 95% CI: 4 of 4

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 40-49¢ | 4 | 4 | 49.0¢ | 75.0% | 30.1% – 95.4% | +26.0 |
| 50-59¢ | 1,864 | 1,864 | 54.6¢ | 53.6% | 51.4% – 55.9% | -1.0 |
| 60-69¢ | 603 | 603 | 62.9¢ | 60.9% | 56.9% – 64.7% | -2.0 |
| 70-79¢ | 58 | 58 | 72.4¢ | 75.9% | 63.5% – 85.0% | +3.4 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 2,424 (105 removed)
- Brier score: 0.2439 (main: 0.2441)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 40-49¢ | 4 | +26.0 | 4 | +26.0 |
| 50-59¢ | 1,864 | -1.0 | 1,776 | -0.8 |
| 60-69¢ | 603 | -2.0 | 587 | -2.2 |
| 70-79¢ | 58 | +3.4 | 57 | +4.8 |
