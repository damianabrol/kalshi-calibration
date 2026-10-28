"""Step 4 (selection): screen candidate series using market metadata only (no price history).

Usage:  .venv/bin/python screen_series.py [SERIES ...]
Writes  results/series_screening.md

For each series: settled binary YES/NO markets, events, markets per event, YES results per
event (1 = ranges where one wins; more = "above X" thresholds), median lifetime volume,
share of markets with >= 1,000 contracts, share open at least 24h before close (needed for a
T-24h price), and the median lifespan. Big series are capped at the most recent
MAX_MARKETS_PER_ENDPOINT markets per endpoint (marked *), which is enough for screening.
"""

import sys
from datetime import datetime
from itertools import islice
from pathlib import Path
from statistics import median

import kalshi_api

MAX_MARKETS_PER_ENDPOINT = 15_000
CANDIDATES = [
    "KXNFLGAME", "KXNBAGAME", "KXNHLGAME",                               # sports
    "KXCPI", "KXPAYROLLS", "KXJOBLESSCLAIMS", "KXFED", "KXFEDDECISION",  # economics
    "KXAAAGASD",
    "KXHIGHNY", "KXHIGHCHI", "KXHIGHAUS",                                # weather
    "KXAPRPOTUS", "KXTRUMPAPPROVE", "KX538APPROVE", "KXPOTUSTWEETS",     # politics
    "KXBTCD", "KXBTC", "KXETHD", "KXBTCMAXW", "KXBTCMAXM",               # crypto
    "KXBTCMAXMON", "KXBTCMINMON", "KXETHMAXM",
]


def to_unix(iso_string):
    return datetime.fromisoformat(iso_string.replace("Z", "+00:00")).timestamp()


def screen(series):
    markets = {}
    for path, params in [("/historical/markets", {"series_ticker": series, "limit": 1000}),
                         ("/markets", {"series_ticker": series, "status": "settled", "limit": 1000})]:
        for m in islice(kalshi_api.paginate(path, params, "markets"), MAX_MARKETS_PER_ENDPOINT):
            markets[m["ticker"]] = m
    ms = [m for m in markets.values() if m.get("market_type") == "binary" and m.get("result") in ("yes", "no")]
    if not ms:
        return f"| {series} | 0 | | | | | | | | |"

    events = {}
    for m in ms:
        events.setdefault(m["event_ticker"], []).append(m)
    volumes = [float(m.get("volume_fp") or 0) for m in ms]
    hours = [(to_unix(m["close_time"]) - to_unix(m["open_time"])) / 3600 for m in ms]
    closes = sorted(m["close_time"][:10] for m in ms)
    capped = "*" if len(markets) >= MAX_MARKETS_PER_ENDPOINT else ""
    return (f"| {series} | {len(ms):,}{capped} | {len(events):,} "
            f"| {median(len(e) for e in events.values()):.0f} "
            f"| {median(sum(m['result'] == 'yes' for m in e) for e in events.values()):.0f} "
            f"| {median(volumes):,.0f} | {sum(v >= 1000 for v in volumes) / len(ms):.0%} "
            f"| {sum(h >= 24 for h in hours) / len(ms):.0%} | {median(hours):,.0f}h "
            f"| {closes[0]} to {closes[-1]} |")


def main():
    candidates = sys.argv[1:] or CANDIDATES
    lines = ["# Series screening (market metadata only)", "",
             f"`*` = capped at the most recent {MAX_MARKETS_PER_ENDPOINT:,} markets per endpoint.", "",
             "| Series | Markets | Events | Markets/event | YES/event | Median volume | Volume >= 1k "
             "| Open >= 24h | Median lifespan | Close dates |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for series in candidates:
        lines.append(screen(series))
        print(lines[-1], flush=True)
    Path("results").mkdir(exist_ok=True)
    Path("results/series_screening.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
