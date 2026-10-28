"""Step 2a: download every settled market in one series, plus hourly price history.

Usage:  .venv/bin/python pull_data.py KXMLBGAME

What it does:
  1. Lists all settled markets in the series from BOTH endpoints (historical archive + live).
  2. Marks binary markets that settled YES or NO as `eligible`.
  3. Downloads hourly candlesticks for every eligible market (both sides of each game).
  4. Writes data/<series>_markets.csv and data/<series>_candles.csv

Every API response is cached as JSON under data/raw/<series>/, so re-running the script
reads from disk instead of calling the API. Delete that folder to re-download
(e.g., to pick up markets that settled since the last run).
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

import kalshi_api

DATA_DIR = Path("data")
MAX_CANDLE_HOURS = 4999  # API limit is 5,000 candles; a 4,999h window holds at most 5,000 hourly candles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("pull_data")


def to_unix(iso_string):
    # API timestamps look like "2026-10-20T03:05:22Z"
    return int(datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp())


def cached(path, fetch):
    """Return the JSON saved at `path`. If it isn't there yet, call fetch(), save, and return it."""
    if path.exists():
        return json.loads(path.read_text()), False
    data = fetch()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))
    return data, True


def list_settled_markets(series, raw_dir):
    """One row per settled market in the series, from both the historical and live endpoints."""
    historical, _ = cached(raw_dir / "markets_historical.json", lambda: list(kalshi_api.paginate(
        "/historical/markets", {"series_ticker": series, "limit": 1000}, "markets")))
    live, _ = cached(raw_dir / "markets_live.json", lambda: list(kalshi_api.paginate(
        "/markets", {"series_ticker": series, "status": "settled", "limit": 1000}, "markets")))
    log.info("settled markets: %d historical + %d live", len(historical), len(live))

    rows, seen = [], set()
    for source, batch in [("historical", historical), ("live", live)]:
        for m in batch:
            if m["ticker"] in seen:  # guard against a market appearing in both lists
                continue
            seen.add(m["ticker"])
            rows.append({
                "ticker": m["ticker"],
                "event_ticker": m["event_ticker"],
                "title": m.get("title"),
                "market_type": m.get("market_type"),
                "result": m.get("result"),
                "open_time": m["open_time"],
                "close_time": m["close_time"],
                "scheduled_end": m.get("expected_expiration_time"),  # set in advance by Kalshi
                "volume": float(m.get("volume_fp") or 0),
                "source": source,  # tells us which candlestick endpoint to use
            })
    return pd.DataFrame(rows)


def fetch_candles(series, market):
    """Hourly candlesticks over the market's whole life (open -> close).

    The API returns at most 5,000 candles per request (a 5,001-hour window gets a 400),
    so a market open longer than that is fetched in 5,000-hour chunks.
    """
    if market.source == "historical":
        path = f"/historical/markets/{market.ticker}/candlesticks"
    else:
        path = f"/series/{series}/markets/{market.ticker}/candlesticks"

    start, end = to_unix(market.open_time), to_unix(market.close_time)
    candles = []
    while start <= end:
        chunk_end = min(end, start + MAX_CANDLE_HOURS * 3600)
        params = {"start_ts": start, "end_ts": chunk_end, "period_interval": 60}
        candles += kalshi_api.get(path, params)["candlesticks"]
        start = chunk_end + 1  # next chunk starts right after this one, so no overlap
    return candles


def dollars(candle, group, name):
    """Read e.g. price.close as a float, or None if nothing traded.

    The live endpoint names it close_dollars, the historical endpoint names it close.
    """
    values = candle.get(group) or {}
    value = values.get(f"{name}_dollars", values.get(name))
    return float(value) if value is not None else None


def flatten_candle(ticker, candle):
    volume = candle.get("volume_fp", candle.get("volume"))  # live vs historical name
    return {
        "ticker": ticker,
        "end_period_ts": candle["end_period_ts"],
        "price_close": dollars(candle, "price", "close"),  # last trade in the hour (None = no trades)
        "yes_bid_close": dollars(candle, "yes_bid", "close"),  # best bid at the end of the hour
        "yes_ask_close": dollars(candle, "yes_ask", "close"),  # best ask at the end of the hour
        "volume": float(volume or 0),  # contracts traded in the hour
    }


def main():
    series = sys.argv[1] if len(sys.argv) > 1 else "KXMLBGAME"
    raw_dir = DATA_DIR / "raw" / series

    markets = list_settled_markets(series, raw_dir)
    markets["eligible"] = markets["market_type"].eq("binary") & markets["result"].isin(["yes", "no"])
    eligible = markets[markets["eligible"]]
    log.info("%d markets, %d binary and settled YES/NO", len(markets), len(eligible))

    candle_rows, downloaded = [], 0
    for i, market in enumerate(eligible.itertuples(), start=1):
        candles, was_downloaded = cached(raw_dir / "candles" / f"{market.ticker}.json",
                                         lambda: fetch_candles(series, market))
        downloaded += was_downloaded
        candle_rows += [flatten_candle(market.ticker, c) for c in candles]
        if i % 250 == 0 or i == len(eligible):
            log.info("candles: %d/%d markets (%d downloaded, %d from cache)",
                     i, len(eligible), downloaded, i - downloaded)

    markets.to_csv(DATA_DIR / f"{series}_markets.csv", index=False)
    pd.DataFrame(candle_rows).to_csv(DATA_DIR / f"{series}_candles.csv", index=False)
    log.info("wrote %s_markets.csv (%d rows) and %s_candles.csv (%d rows) to %s/",
             series, len(markets), series, len(candle_rows), DATA_DIR)


if __name__ == "__main__":
    main()
