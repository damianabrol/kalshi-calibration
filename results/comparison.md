# Calibration by category, 24h before close

Lifetime volume >= 1,000 contracts. Two-team sports: favorite side of each game, Wilson intervals. All other series: every market, event-bootstrap intervals (2,000 resamples).

| Group | Category | Analyzed | Close dates | Avg price | Resolved YES (95% CI) | Gap (pts) | Brier | Reference | Bins with avg price inside CI |
|---|---|---|---|---:|---|---:|---:|---:|---|
| MLB games | Sports | favorite side of 2,529 games | 2025-04-25 to 2026-10-20 | 57.0¢ | 55.9% (54.0% – 57.8%) | -1.1 | 0.2441 | 0.2465 | 4 of 4 |
| NBA games | Sports | favorite side of 1,498 games | 2025-04-16 to 2026-10-23 | 69.4¢ | 66.4% (63.9% – 68.7%) | -3.0 | 0.2058 | 0.2233 | 3 of 5 |
| CPI | Economics | 423 markets in 64 events | 2021-07-12 to 2026-10-14 | 50.7¢ | 50.1% (38.2% – 62.0%) | -0.6 | 0.0787 | 0.2500 | 10 of 10 |
| NYC daily high temp | Weather | 6,748 markets in 1,778 events | 2021-08-07 to 2026-10-22 | 23.9¢ | 22.7% (20.8% – 24.7%) | -1.2 | 0.1387 | 0.1756 | 10 of 10 |
| RCP approval | Politics | 1,019 markets in 211 events | 2021-10-15 to 2026-10-16 | 18.8¢ | 17.7% (13.1% – 23.4%) | -1.2 | 0.0869 | 0.1454 | 10 of 10 |
| BTC monthly high/low | Crypto | 128 markets in 18 events | 2026-01-31 to 2026-10-01 | 1.4¢ | 1.6% (0.0% – 20.1%) | +0.2 | 0.0146 | 0.0154 | 2 of 2 |

Total: 12,345 markets in 6,098 events. Average price inside the bin's 95% CI in 39 of 41 bins.

## Longshots and heavy favorites

Longshots: priced below 20¢. Heavy favorites: priced at 80¢ or more. For two-team sports only the favorite side is analyzed, so a favorite at 85¢ is the same bet as its opponent's 15¢ longshot.

| Group | Band | Markets | Avg price | Resolved YES | 95% CI | Gap (pts) |
|---|---|---:|---:|---:|---|---:|
| MLB games | longshots | 0 | – | – | – | – |
| MLB games | heavy favorites | 0 | – | – | – | – |
| NBA games | longshots | 0 | – | – | – | – |
| NBA games | heavy favorites | 342 | 86.2¢ | 84.2% | 80.0% – 87.7% | -2.0 |
| CPI | longshots | 160 | 5.9¢ | 3.8% | 1.1% – 12.5% | -2.1 |
| CPI | heavy favorites | 162 | 94.8¢ | 95.1% | 86.3% – 98.4% | +0.3 |
| NYC daily high temp | longshots | 3,315 | 7.2¢ | 6.5% | 5.4% – 8.0% | -0.7 |
| NYC daily high temp | heavy favorites | 93 | 88.5¢ | 80.6% | 71.4% – 88.4% | -7.9 |
| RCP approval | longshots | 692 | 5.1¢ | 3.2% | 1.4% – 6.9% | -1.9 |
| RCP approval | heavy favorites | 41 | 90.5¢ | 90.2% | 75.6% – 97.7% | -0.3 |
| BTC monthly high/low | longshots | 128 | 1.4¢ | 1.6% | 0.0% – 20.1% | +0.2 |
| BTC monthly high/low | heavy favorites | 0 | – | – | – | – |

## Two-team sports: the overround

Both sides of a game can be bought, and their prices usually add up to a bit more than $1. Dividing the favorite's price by the sum of both sides removes that extra.

| Group | Both sides sum to (avg) | Favorite's price (avg) | Net of overround (avg) | Favorite won (95% CI) |
|---|---:|---:|---:|---|
| MLB games | 100.74¢ | 57.0¢ | 56.6¢ | 55.9% (54.0% – 57.8%) |
| NBA games | 101.78¢ | 69.4¢ | 68.2¢ | 66.4% (63.9% – 68.7%) |
