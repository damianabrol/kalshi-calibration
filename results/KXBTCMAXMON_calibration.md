# KXBTCMAXMON: calibration 24h before close

- Analyzed: 66 markets in 9 events (lifetime volume >= 1,000 contracts)
- Confidence intervals: 95%, event bootstrap
- Close dates: 2026-02-01 to 2026-10-01
- Average price: 1.1¢ | Share resolved YES: 0.0% (95% CI 0.0% – 29.9%)
- Brier score: 0.0001 (reference, always predicting 0.0%: 0.0000; lower is better)
- Bins where the average price is inside the 95% CI: 1 of 1

## By price bin

| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---:|---:|---:|---:|---|---:|
| 0-9¢ | 66 | 9 | 1.1¢ | 0.0% | 0.0% – 29.9% | -1.1 |

## Robustness: excluding prices outside the bid-ask or more than 3h stale

- Markets: 33 (33 removed)
- Brier score: 0.0002 (main: 0.0001)

| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |
|---|---:|---:|---:|---:|
| 0-9¢ | 66 | -1.1 | 33 | -1.2 |
