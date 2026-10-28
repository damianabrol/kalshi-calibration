# Kalshi Calibration Study

**Question:** When a Kalshi contract trades at X¢, does it resolve YES about X% of the time?
Does that hold across categories (sports, economics, politics, weather, crypto) and across
price ranges (e.g., are longshots overpriced)?

All data comes from Kalshi's public market-data API (no login or API key needed).

## Status

- [x] Step 1: Project setup + API exploration (`explore_api.py`, sample responses in `samples/`)
- [x] Step 2: Data pull for one series (MLB games, `KXMLBGAME`), plus a data-quality check of
      how often the 24h-before-close price comes from a thin or stale trade
      (report: `results/KXMLBGAME_data_quality.md`)
- [x] Step 3: Calibration analysis + chart for MLB
      (`results/KXMLBGAME_calibration.md`, `.csv`, `.png`)
- [x] Step 4: Expand to 4–6 series across categories
      (`results/comparison.md`, `.csv`, `.png`; per-series `results/<series>_calibration.md`)
- [x] Step 5: Memos for a Kalshi reader: `memo_1page.md` / `.pdf` and `memo_3page.md` / `.pdf`
      (every number checked against `results/` by `check_memo.py`)

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python explore_api.py              # step 1: sample responses into samples/
.venv/bin/python pull_data.py KXMLBGAME      # step 2: download (cached) -> data/
.venv/bin/python build_dataset.py KXMLBGAME  # step 2: T-24h price per market, favorite side marked
.venv/bin/python data_quality.py KXMLBGAME   # step 2: thin/stale/volume report -> results/
.venv/bin/python calibration.py KXMLBGAME    # step 3: calibration table, Brier, chart -> results/

# step 4: same pipeline for every series, then the cross-category comparison
for s in KXMLBGAME KXNBAGAME KXCPI KXHIGHNY KXAPRPOTUS KXBTCMAXMON KXBTCMINMON; do
  .venv/bin/python pull_data.py $s && .venv/bin/python build_dataset.py $s && .venv/bin/python data_quality.py $s
done
.venv/bin/python compare.py                  # -> results/comparison.md, .csv, .png
.venv/bin/python screen_series.py            # how the series were chosen -> results/series_screening.md

# step 5: memos (PDF export needs Google Chrome installed)
.venv/bin/python check_memo.py               # every number in the memos must appear in results/
.venv/bin/python export_pdf.py               # memo_1page.pdf, memo_3page.pdf (fails if length is off)
```

`pull_data.py` caches every API response under `data/raw/<series>/`, so re-runs make no API
calls. Delete that folder to re-download (e.g., to pick up newly settled markets).

## Project layout

| File | Purpose |
|---|---|
| `kalshi_api.py` | Tiny API client: `get()` with a polite delay + retries, `paginate()` to follow cursors |
| `explore_api.py` | Step 1: fetches and saves sample market + candlestick responses |
| `samples/` | Raw JSON responses from the API, kept so reviewers can see the data shape |
| `pull_data.py` | Step 2: lists settled markets (both endpoints), downloads hourly candles for both sides of every game |
| `build_dataset.py` | Step 2: computes the T-24h price per market and marks each game's favorite; unusable markets kept with a `drop_reason` |
| `data_quality.py` | Step 2: measures how thin/stale the T-24h prices are and what each volume cutoff removes |
| `calibration.py` | Step 3: 10¢-bin calibration table with Wilson or event-bootstrap CIs, Brier score, robustness check, chart |
| `compare.py` | Step 4: every category side by side: summary table, longshots vs. heavy favorites, overround, small-multiples charts |
| `screen_series.py` | Step 4: screens candidate series on market metadata (how the lineup was chosen) |
| `memo_1page.md`, `memo_3page.md` | Step 5: the memos (Markdown source; PDFs alongside) |
| `check_memo.py` | Step 5: fails if a memo contains a number that isn't in the generated `results/` files |
| `export_pdf.py` | Step 5: Markdown → HTML → PDF via headless Chrome; checks each memo's page count |
| `data/` | `<series>_markets.csv`, `<series>_candles.csv` (raw), `<series>_snapshots.csv` (one row per market) |
| `data/raw/` | Cached API responses (JSON), git-ignored |
| `results/` | Reports and charts |

## Methodology

**Snapshot time.** We don't use the final price, because it converges to $0 or $1 at
settlement. We use the price **24 hours before the event closes**, where "event close" is the
`close_time` of the event's last market. Markets that weren't open yet at that point are dropped.
*Exception, added in step 4: markets that close the moment they resolve.* In the BTC "reaches /
falls to $X this month" series (`KXBTCMAXMON`, `KXBTCMINMON`), a market closes as soon as BTC
touches $X, always as YES; 17 of 89 markets checked closed early, all YES. Their `close_time`
therefore reveals the outcome, and "24h before close" would mean "24h before Bitcoin touched $X."
Even the event's last close can be early: in January 2026 BTC fell through every level, so all 8
markets closed early as YES. For these series the snapshot is anchored to Kalshi's **scheduled
end** for the event (`expected_expiration_time`, set in advance: the month's end), and markets
that had already closed by the snapshot are dropped ("closed before T-24h"); whether a market had
already resolved is known at snapshot time, so this doesn't leak the future. Events still in
progress when the data was pulled (October 2026) are dropped the same way. For every other
series, an event's markets close together at a time that doesn't depend on the outcome; MLB
results did not change.

**Snapshot price = last traded price at or before T-24h.** We take hourly candlesticks and use
the closing trade price of the most recent hour, at or before the snapshot, that had a trade.
Hours with no trades have no price, so the last trade carries forward. If a market hasn't traded
at all by T-24h, it's dropped. We record how stale the price is (hours between that trade and
the snapshot) so we can check whether staleness matters.
*Why:* the question is "when a contract trades at X¢", so a real trade price is the most
direct measure. The bid/ask midpoint was rejected because empty order books (bid 0¢ / ask 99¢)
produce a meaningless 50¢.

**One side per game: the favorite.** Each MLB game has two mirror markets ("Team A wins" /
"Team B wins") whose prices sum to about $1. We analyze **the side priced higher at T-24h**,
using its own traded price. Games where either side has no T-24h price are skipped (we can't
tell which side was favored); exact price ties are broken by a coin flip seeded with the event
ticker.
*Why one side:* both sides settle on the same outcome, so counting both would double-count each
game, make the chart symmetric by construction, and make confidence intervals too narrow.
*Why the favorite, not a random side (changed in step 3):* we first picked a random side. In a
two-team game a random side wins 50% of the time by definition, but our draw's chosen sides won
only 47.4% of 2,532 games (2.6 standard errors below 50%). That shortfall showed up as a
negative gap in every well-populated bin (30–69¢), which looked like across-the-board
"overpricing" but was really noise from the coin flip. The favorite rule uses every game once with no coin flip.
The underdog half of the chart (below 50¢) is the mirror image of the favorite half, so it adds
no information.
*Caveat:* picking the higher of two prices that each carry a little noise (e.g., a slightly stale
last trade) tilts the favorite's price slightly upward, which can make favorites look a bit
overpriced. With tight spreads this effect should be small, but it isn't zero, so a small
negative gap for favorites should be read with that in mind.

**Multi-market events: every market, resample whole events (step 4).** Outside two-team sports,
an event holds several linked markets: NYC temperature and RCP approval are split into ranges where
exactly one wins, and CPI and the BTC monthly series are "above X" / "reaches X" thresholds, so if
one is YES the lower ones are too. We analyze **every market with a T-24h price**, and build
confidence intervals with an **event bootstrap**: draw as many events as the series has, with
replacement, recompute each bin's YES rate, repeat 2,000 times, and keep the middle 95%.
*Why:* picking one market per event would leave CPI with ~64 data points and bring back
coin-flip noise; using every market but treating them as independent would make intervals too
narrow. A check with fake data where each event appears 5 times shows the bootstrap keeps the
honest width while a naive Wilson interval shrinks by more than half.
*Floor:* when YES (or NO) results in a bin are rare, the bootstrap can't produce resamples far
from the observed rate, so its interval is too narrow, and it has zero width if every result is
the same. On real data, CPI's 0–9¢ bin (1 YES in 125 markets) got a bootstrap interval narrower
than even a naive interval that ignores the linking. So each bin's interval is **never narrower
than a Wilson interval that counts each event in the bin once**, at the bin's YES rate.

**Calibration table and confidence intervals.** Prices are put in 10¢ bins by whole cents
(0–9¢, 10–19¢, …). For each bin we compare the average price (implied probability) with the
share that resolved YES, with a **95% Wilson score interval** on that share for two-team sports,
where every analyzed market is its own event, and the event bootstrap above for other series.
*Why Wilson:* the textbook normal interval (p ± 1.96·√(p(1−p)/n)) breaks down for small bins
and rates near 0% or 100%, where it can extend below 0% or have zero width. Clopper–Pearson
guarantees coverage but is wider than needed. Wilson is the standard middle ground and fits in
a few lines of code.

**Brier score** = average of (price − outcome)², where outcome is 1 for YES and 0 for NO; lower
is better. It's reported next to a **reference score**: always predicting the sample's overall
YES rate, base × (1 − base). A Brier score only means something compared with a baseline that
uses no price information.

**Minimum volume: 1,000 contracts.** Markets with less lifetime volume are excluded.
*Why:* with fewer than ~1,000 contracts traded (at most ~$1,000 notional), one or two traders can
set the price, so it isn't really a crowd forecast. For MLB, thresholds of 100, 1,000 and
10,000 all keep 99.7–99.8% of games; at 1,000 the only games removed are seven broken markets
(see Data notes).

**Only binary markets that settled YES or NO** (`market_type == "binary"`, `result` in yes/no).

**Thin or stale prices (measured in step 2 before deciding on a filter).** A market can trade
millions of contracts over its life and still have its T-24h price set by one small trade made
hours earlier, because most trading happens close to game time. A lifetime-volume filter doesn't
catch that, so `data_quality.py` measures, for each game:
- *staleness*: hours between the last trade and the snapshot
- *thinness*: contracts traded in the hour that set the price, and in the 24h before the snapshot
- *quotes*: the bid-ask spread at the snapshot, and whether the trade price sits outside it

*Decision (after step 2):* no thin/stale filter on the main results. For MLB (favorite side),
94.2% of T-24h prices are within 1 hour of the last trade and 97.4% of spreads are ≤ 2¢. As a
robustness check, `calibration.py` re-runs the calibration without (a) games whose last trade
sits outside the bid-ask at the snapshot and (b) games whose last trade is more than 3h stale.
*Result for MLB:* removing those 105 games moves the Brier score from 0.2441 to 0.2439 and each
bin's gap by at most 1.4 points (`results/KXMLBGAME_calibration.md`).
*Limitation (step 4):* the check is only informative for series that trade often. In
slow-trading series most markets haven't traded within 3 hours of the snapshot, so it removes
370 of 423 CPI markets and 390 of 1,019 approval markets.

**Overround (two-team sports, step 4).** Either side of a game can be bought, and at T-24h the
two sides' prices add up to slightly more than $1 on average (MLB 100.74¢, NBA 101.78¢). Part of
any gap between a favorite's price and its win rate is that extra, not a mispricing of the
outcome. `compare.py` reports the favorite's price divided by the sum of both sides ("net of
overround") next to the raw price.

**Horizon stays at 24h for every series**, so categories are compared at the same distance from
close. For MLB this means the sample is effectively the 2026 season plus the 2025 postseason
(see Data notes); that goes in the memo's limitations.

**Series compared (step 4)**, chosen by screening market metadata (counts, volume, how long
markets are open) for recurring series in each category:

| Category | Group | Series | Why this one |
|---|---|---|---|
| Sports | MLB games | `KXMLBGAME` | Steps 2–3 |
| Sports | NBA games | `KXNBAGAME` | Liquid (median ~2.6M contracts/market); lopsided favorites, which MLB lacks |
| Economics | CPI | `KXCPI` | Flagship economic release; monthly since 2021 |
| Weather | NYC daily high temp | `KXHIGHNY` | Largest sample (~1,900 days since 2021) |
| Politics | RCP approval | `KXAPRPOTUS` | Weekly since 2021; most events of the politics candidates |
| Crypto | BTC monthly high/low | `KXBTCMAXMON` + `KXBTCMINMON` | Only crypto series open 24h+ before close; pooled because each is small |

*Crypto caveat:* almost all Kalshi crypto trading is short-horizon. Hourly BTC/ETH markets live
about an hour, daily 5pm BTC markets open 25 hours before close (median volume 0), and the monthly
high/low series have only ~179 markets in 20 events, so crypto intervals will be wide.

## API notes (learned in step 1)

- Base URL: `https://api.elections.kalshi.com/trade-api/v2`
- `GET /historical/cutoff`: markets settled before `market_settled_ts` are only in
  `GET /historical/markets`; newer ones are in `GET /markets?status=settled`. Both filter by
  `series_ticker` and paginate with `cursor`.
- Candlesticks: live markets use `GET /series/{series}/markets/{ticker}/candlesticks`,
  archived markets use `GET /historical/markets/{ticker}/candlesticks`. Both need `start_ts`,
  `end_ts` (unix seconds), and `period_interval` (1, 60, or 1440 minutes).
- **The two candlestick endpoints name the same fields differently:**

  | Field | Live endpoint | Historical endpoint |
  |---|---|---|
  | Closing trade price | `price.close_dollars` | `price.close` |
  | Contracts traded | `volume_fp` | `volume` |
  | Open interest | `open_interest_fp` | `open_interest` |
  | Hour with no trades | `price: {}` | `price.close: null` (`price.previous` = last trade) |

- A candlestick request returns at most **5,000 candles**; a longer window gets a 400. `pull_data.py`
  splits long windows into 4,999-hour chunks.
- Some timestamps include fractional seconds (`2025-11-01T03:20:17.157302Z`); parse with
  `datetime.fromisoformat` or `pd.to_datetime(..., format="ISO8601")`.
- The historical and live market lists can overlap (138 MLB markets appeared in both), so
  `pull_data.py` de-duplicates by ticker.
- All prices are dollar strings (e.g., `"0.5700"` = 57¢); volumes are contract counts as strings.
- Rate limit is documented as ~20 reads/sec on the basic tier, but unauthenticated candlestick
  requests hit 429s at about 4 requests/sec total (seen when running 3 downloads in parallel).
  A 429 has no Retry-After header, so the client backs off exponentially (1s, 2s, 4s, … up to
  8 retries). Parallel downloads barely help; run series one or two at a time.
- The unfiltered historical feed is mostly multi-leg parlay markets (`KXMVE...` tickers),
  so all pulls are filtered by `series_ticker`.

## Data notes: MLB (`KXMLBGAME`)

- **2025 regular-season markets opened only ~11–14 hours before close** (median), so they have no
  T-24h price; 92–99% of games each month from April to September 2025 are dropped for "not open at T-24h".
  From the 2025 postseason on, markets open ~3 days (~74h) before close. The T-24h sample is
  therefore essentially the 2026 regular season plus the 2025 postseason.
- Seven markets for games on Apr 18, 2025 opened *after* the game was played, closed in March 2026,
  and traded 7–117 contracts. The 1,000-contract minimum removes them.
- Of 4,679 games, 4,675 have exactly one market that settled YES; 4 have both sides settled NO.
- At T-24h, MLB prices sit almost entirely between 30¢ and 70¢, so MLB alone can't test
  how longshots (< 20¢) or heavy favorites (> 80¢) are priced.
