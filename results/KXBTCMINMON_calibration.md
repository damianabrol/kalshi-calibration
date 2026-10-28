# KXBTCMINMON: calibration 24h before close

- Analyzed: 62 markets in 9 events (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, event bootstrap
- Close dates: 2026-01-31 to 2026-10-01
- Average price: 1.7¢ | Share resolved YES: 3.2% (95% CI 0.0% – 34.2%)
- Brier score: 0.0299 (reference, always predicting 3.2%: 0.0312; lower is better)
- Bins where the average price is inside the 95% CI: 2 of 2

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 0-9¢ | 61 | 9 | 1.5¢ | 3.3% | 0.0% – 34.3% | +1.8 |
| 10-19¢ | 1 | 1 | 11.0¢ | 0.0% | 0.0% – 79.3% | -11.0 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 18 (44 removed)
- Brier score: 0.0536 (main: 0.0299)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 0-9¢ | 61 | +1.8 | 17 | +3.7 |
| 10-19¢ | 1 | -11.0 | 1 | -11.0 |
