"""Step 2b: turn raw markets + hourly candles into one row per market, priced 24h before close,
and mark which markets are analyzed (`analyzed` column):
  - two-team series (one market per team): only each game's favorite
  - every other series: every market with a T-24h price

Usage:  .venv/bin/python build_dataset.py KXMLBGAME
Reads   data/<series>_markets.csv and data/<series>_candles.csv  (from pull_data.py)
Writes  data/<series>_snapshots.csv

Snapshot rule (agreed in step 1): the price is the last traded price at or before
24h before the event closes:
  - normally, "event close" is the close of the event's last market (all of an event's
    markets close together at a time that doesn't depend on the outcome)
  - for series in CLOSES_ON_RESOLUTION, markets close the moment they resolve ("Will BTC
    reach $X this month?" closes when BTC touches $X, always as YES), so actual close times
    reveal outcomes. For these we use Kalshi's scheduled end for the event instead.
A market that already closed before the snapshot is dropped; that is known at snapshot
time, so it doesn't leak the future.

We only look at hourly candles that END at or before the snapshot time, so no trade made
after the snapshot can leak in. Unusable markets stay in the file with a drop_reason, so
every exclusion is visible. No volume or thin/stale filter is applied here;
data_quality.py measures those first.
"""

import random
import sys
from datetime import datetime, timezone

import pandas as pd

SNAPSHOT_HOURS_BEFORE_CLOSE = 24
SEED = 42

# Series whose events are two mirror markets, one per team. For these we analyze each game's
# favorite. For every other series (ranges, thresholds) every priced market is analyzed, and
# calibration.py accounts for markets in the same event being linked.
TWO_SIDED_SERIES = {"KXMLBGAME", "KXNBAGAME"}

# Series whose markets close as soon as they resolve, so the snapshot is anchored to the
# event's scheduled end. (In Jan 2026 BTC fell through every level of KXBTCMINMON, so all
# 8 markets closed early as YES; even the event's last close was outcome-dependent.)
CLOSES_ON_RESOLUTION = {"KXBTCMAXMON", "KXBTCMINMON"}


def to_unix(iso_string):
    return int(datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp())


def snapshot_row(market, candles, event_close_ts):
    snapshot_ts = event_close_ts - SNAPSHOT_HOURS_BEFORE_CLOSE * 3600
    row = {
        "ticker": market.ticker,
        "event_ticker": market.event_ticker,
        "title": market.title,
        "close_time": market.close_time,
        "snapshot_time": datetime.fromtimestamp(snapshot_ts, timezone.utc).isoformat(),
        "resolved_yes": 1 if market.result == "yes" else 0,
        "volume": market.volume,      # lifetime contracts traded
        "price": None,                # last trade at or before the snapshot ($0-$1 = implied probability)
        "staleness_hours": None,      # snapshot time minus the end of the hour of that last trade
        "price_hour_volume": None,    # contracts traded in the hour that set the price
        "volume_prior_24h": None,     # contracts traded in the 24h leading up to the snapshot
        "bid": None,                  # best YES bid at the snapshot (end of the latest full hour)
        "ask": None,                  # best YES ask at the snapshot
        "drop_reason": "",
    }

    if to_unix(market.open_time) > snapshot_ts:
        row["drop_reason"] = "not open at T-24h"
        return row
    if to_unix(market.close_time) <= snapshot_ts:
        row["drop_reason"] = "closed before T-24h"  # already resolved by then
        return row

    before = candles[candles["end_period_ts"] <= snapshot_ts]
    traded = before[before["price_close"].notna()]
    if traded.empty:
        row["drop_reason"] = "no trade by T-24h"
        return row

    last_trade = traded.iloc[-1]  # most recent hour with a trade -> carried-forward price
    latest = before.iloc[-1]      # most recent hour, traded or not -> current quotes
    prior_24h = before[before["end_period_ts"] > snapshot_ts - 24 * 3600]
    row.update({
        "price": last_trade["price_close"],
        "staleness_hours": (snapshot_ts - last_trade["end_period_ts"]) / 3600,
        "price_hour_volume": last_trade["volume"],
        "volume_prior_24h": prior_24h["volume"].sum(),
        "bid": latest["yes_bid_close"],
        "ask": latest["yes_ask_close"],
    })
    return row


def favorites(snapshots):
    """True for the side of each game we analyze in a two-team series: the favorite.

    Both markets of a game ("Team A wins" / "Team B wins") describe the same outcome, so
    we analyze one per game: the side priced higher 24h before close. (Step 3 showed that
    picking a side at random adds coin-flip noise that can look like mispricing.)
    A game is skipped if either side has no T-24h price, since then we can't tell which
    side was favored. Exact ties are broken by a coin flip seeded with the event ticker.
    """
    picks = set()
    for event, group in snapshots.groupby("event_ticker"):
        if (group["drop_reason"] != "").any():
            continue
        top = group[group["price"] == group["price"].max()]
        picks.add(random.Random(f"{SEED}:{event}").choice(sorted(top["ticker"])))
    return snapshots["ticker"].isin(picks)


def main():
    series = sys.argv[1] if len(sys.argv) > 1 else "KXMLBGAME"
    markets = pd.read_csv(f"data/{series}_markets.csv")
    candles = pd.read_csv(f"data/{series}_candles.csv").sort_values(["ticker", "end_period_ts"])

    candles_by_ticker = dict(tuple(candles.groupby("ticker")))
    no_candles = candles.iloc[0:0]  # empty table, for a market whose candle request came back empty

    eligible = markets[markets["eligible"]]
    end_column = "scheduled_end" if series in CLOSES_ON_RESOLUTION else "close_time"
    end_ts = eligible[end_column].map(to_unix)
    event_close_ts = end_ts.groupby(eligible["event_ticker"]).transform("max")  # one close time per event
    rows = [snapshot_row(m, candles_by_ticker.get(m.ticker, no_candles), event_close)
            for m, event_close in zip(eligible.itertuples(), event_close_ts)]
    snapshots = pd.DataFrame(rows)
    if series in TWO_SIDED_SERIES:
        snapshots["analyzed"] = favorites(snapshots)
    else:
        snapshots["analyzed"] = snapshots["drop_reason"] == ""
    snapshots.to_csv(f"data/{series}_snapshots.csv", index=False)

    analyzed = snapshots[snapshots["analyzed"]]
    print(f"wrote data/{series}_snapshots.csv: {len(snapshots):,} markets; analyzed "
          f"{len(analyzed):,} markets in {analyzed['event_ticker'].nunique():,} events")


if __name__ == "__main__":
    main()
