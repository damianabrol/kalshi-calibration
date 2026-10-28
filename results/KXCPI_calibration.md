# KXCPI: calibration 24h before close

- Analyzed: 423 markets in 64 events (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, event bootstrap
- Close dates: 2021-07-12 to 2026-10-14
- Average price: 50.7¢ | Share resolved YES: 50.1% (95% CI 38.2% – 62.0%)
- Brier score: 0.0787 (reference, always predicting 50.1%: 0.2500; lower is better)
- Bins where the average price is inside the 95% CI: 10 of 10

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 0-9¢ | 125 | 49 | 3.5¢ | 0.8% | 0.0% – 8.7% | -2.7 |
| 10-19¢ | 35 | 35 | 14.3¢ | 14.3% | 3.1% – 29.4% | -0.0 |
| 20-29¢ | 17 | 17 | 25.2¢ | 11.8% | 0.0% – 34.3% | -13.5 |
| 30-39¢ | 16 | 16 | 34.2¢ | 37.5% | 14.3% – 61.5% | +3.3 |
| 40-49¢ | 12 | 12 | 45.1¢ | 41.7% | 12.5% – 72.7% | -3.4 |
| 50-59¢ | 18 | 18 | 55.4¢ | 61.1% | 38.5% – 83.3% | +5.7 |
| 60-69¢ | 18 | 18 | 63.9¢ | 83.3% | 60.8% – 100.0% | +19.4 |
| 70-79¢ | 20 | 20 | 74.2¢ | 65.0% | 42.3% – 85.7% | -9.2 |
| 80-89¢ | 26 | 26 | 84.8¢ | 80.8% | 62.1% – 95.0% | -4.0 |
| 90-99¢ | 136 | 50 | 96.7¢ | 97.8% | 89.2% – 100.0% | +1.1 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 53 (370 removed)
- Brier score: 0.0802 (main: 0.0787)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 0-9¢ | 125 | -2.7 | 11 | -5.4 |
| 10-19¢ | 35 | -0.0 | 7 | -14.4 |
| 20-29¢ | 17 | -13.5 | 5 | -6.6 |
| 30-39¢ | 16 | +3.3 | 3 | -2.3 |
| 40-49¢ | 12 | -3.4 | 3 | -46.0 |
| 50-59¢ | 18 | +5.7 | 3 | +10.7 |
| 60-69¢ | 18 | +19.4 | 4 | +36.5 |
| 70-79¢ | 20 | -9.2 | 4 | +2.2 |
| 80-89¢ | 26 | -4.0 | 3 | +17.0 |
| 90-99¢ | 136 | +1.1 | 10 | +5.3 |
