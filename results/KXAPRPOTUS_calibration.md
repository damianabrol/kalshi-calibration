# KXAPRPOTUS: calibration 24h before close

- Analyzed: 1,019 markets in 211 events (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, event bootstrap
- Close dates: 2021-10-15 to 2026-10-16
- Average price: 18.8¢ | Share resolved YES: 17.7% (95% CI 13.1% – 23.4%)
- Brier score: 0.0869 (reference, always predicting 17.7%: 0.1454; lower is better)
- Bins where the average price is inside the 95% CI: 10 of 10

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 0-9¢ | 550 | 165 | 2.9¢ | 0.7% | 0.1% – 3.6% | -2.1 |
| 10-19¢ | 142 | 104 | 13.6¢ | 12.7% | 7.6% – 20.4% | -0.9 |
| 20-29¢ | 69 | 57 | 24.3¢ | 27.5% | 17.6% – 40.3% | +3.3 |
| 30-39¢ | 78 | 65 | 33.7¢ | 32.1% | 22.0% – 44.1% | -1.6 |
| 40-49¢ | 53 | 47 | 44.3¢ | 54.7% | 40.7% – 68.0% | +10.5 |
| 50-59¢ | 36 | 36 | 53.2¢ | 38.9% | 23.7% – 56.3% | -14.3 |
| 60-69¢ | 29 | 28 | 64.2¢ | 72.4% | 54.0% – 88.0% | +8.2 |
| 70-79¢ | 21 | 20 | 74.0¢ | 61.9% | 40.4% – 82.4% | -12.1 |
| 80-89¢ | 18 | 18 | 84.1¢ | 88.9% | 67.2% – 100.0% | +4.8 |
| 90-99¢ | 23 | 19 | 95.5¢ | 91.3% | 70.9% – 100.0% | -4.2 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 629 (390 removed)
- Brier score: 0.0909 (main: 0.0869)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 0-9¢ | 550 | -2.1 | 315 | -1.9 |
| 10-19¢ | 142 | -0.9 | 84 | -3.8 |
| 20-29¢ | 69 | +3.3 | 41 | +1.6 |
| 30-39¢ | 78 | -1.6 | 56 | +0.3 |
| 40-49¢ | 53 | +10.5 | 35 | +19.0 |
| 50-59¢ | 36 | -14.3 | 29 | -11.9 |
| 60-69¢ | 29 | +8.2 | 22 | +4.5 |
| 70-79¢ | 21 | -12.1 | 15 | -14.9 |
| 80-89¢ | 18 | +4.8 | 14 | +15.9 |
| 90-99¢ | 23 | -4.2 | 18 | +4.7 |
