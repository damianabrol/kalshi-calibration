"""Step 1: pull a few sample responses from the Kalshi API and save them to samples/.

The goal is to see the real shape of the data before writing the pipeline:
  - the historical cutoff (which endpoint holds which settled markets)
  - one settled MLB market from the live endpoint and one from the historical endpoint
  - hourly candlesticks for each of those markets

Run:  .venv/bin/python explore_api.py
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path

import kalshi_api

SERIES = "KXMLBGAME"
SAMPLES_DIR = Path("samples")
SNAPSHOT_HOURS_BEFORE_CLOSE = 24

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("explore_api")


def save(name, data):
    path = SAMPLES_DIR / name
    path.write_text(json.dumps(data, indent=2))
    log.info("saved %s", path)


def to_unix(iso_string):
    # API timestamps look like "2026-10-20T03:05:22Z"
    return int(datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp())


def trade_price(candle):
    """Closing trade price of an hourly candle, or None if nothing traded that hour.

    The live endpoint calls it price.close_dollars; the historical endpoint calls it price.close.
    """
    price = candle.get("price") or {}
    value = price.get("close_dollars", price.get("close"))
    return float(value) if value is not None else None


def summarize(label, market, candles):
    print(f"\n=== {label}: {market['ticker']} ===")
    for field in ["title", "event_ticker", "market_type", "status", "result",
                  "open_time", "close_time", "volume_fp", "last_price_dollars"]:
        print(f"  {field:20} {market.get(field)}")

    empty = sum(1 for c in candles if trade_price(c) is None)
    print(f"  hourly candles:      {len(candles)} ({empty} with no trades -> empty price)")

    # Preview of the step-2 rule: last traded price at or before close - 24h.
    snapshot_ts = to_unix(market["close_time"]) - SNAPSHOT_HOURS_BEFORE_CLOSE * 3600
    snapshot_time = datetime.fromtimestamp(snapshot_ts, timezone.utc)
    traded_before = [c for c in candles
                     if c["end_period_ts"] <= snapshot_ts and trade_price(c) is not None]
    print(f"  snapshot (T-24h):    {snapshot_time:%Y-%m-%d %H:%M} UTC")
    if traded_before:
        last = traded_before[-1]
        stale_hours = (snapshot_ts - last["end_period_ts"]) / 3600
        print(f"  last trade <= T-24h: ${trade_price(last):.2f} "
              f"(candle ending {stale_hours:.1f}h before snapshot)")
    else:
        print("  last trade <= T-24h: none -> this market would be dropped")


def main():
    SAMPLES_DIR.mkdir(exist_ok=True)

    cutoff = kalshi_api.get("/historical/cutoff")
    save("cutoff.json", cutoff)
    print(f"Historical cutoff (market_settled_ts): {cutoff['market_settled_ts']}")
    print("  settled before this -> /historical/markets; after -> /markets?status=settled")

    live_market = kalshi_api.get(
        "/markets", {"series_ticker": SERIES, "status": "settled", "limit": 1})["markets"][0]
    hist_market = kalshi_api.get(
        "/historical/markets", {"series_ticker": SERIES, "limit": 1})["markets"][0]
    save("market_live.json", live_market)
    save("market_historical.json", hist_market)

    # Hourly candles (period_interval=60) over each market's whole life, open -> close.
    def window(market):
        return {"start_ts": to_unix(market["open_time"]),
                "end_ts": to_unix(market["close_time"]),
                "period_interval": 60}

    live_candles = kalshi_api.get(
        f"/series/{SERIES}/markets/{live_market['ticker']}/candlesticks", window(live_market))
    hist_candles = kalshi_api.get(
        f"/historical/markets/{hist_market['ticker']}/candlesticks", window(hist_market))
    save("candles_live.json", live_candles)
    save("candles_historical.json", hist_candles)

    summarize("LIVE (settled after cutoff)", live_market, live_candles["candlesticks"])
    summarize("HISTORICAL (settled before cutoff)", hist_market, hist_candles["candlesticks"])


if __name__ == "__main__":
    main()
