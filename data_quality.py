"""Step 2c: how trustworthy is the T-24h price? Measures, doesn't filter.

Usage:  .venv/bin/python data_quality.py KXMLBGAME
Reads   data/<series>_markets.csv and data/<series>_snapshots.csv
Writes  results/<series>_data_quality.md  (also printed)

Reports (everything after the funnel is measured on the analyzed markets: each game's
favorite in two-team series, every priced market otherwise):
  - funnel: how many markets survive each step, and why the rest were dropped
  - lifetime volume: distribution, and how many markets each threshold (100 / 1k / 10k) keeps
  - stale: how old the last trade is at the snapshot
  - thin: how many contracts traded in the hour that set the price, and in the prior 24h
  - quotes: bid-ask spread at the snapshot, and how often the trade price sits outside it
"""

import sys
from pathlib import Path

import pandas as pd

INF = float("inf")


def pct(n, total):
    return f"{n:,} ({n / total:.1%})"


def distribution(values, bins, labels, right=True):
    """Bullet lines counting how many values fall in each bin."""
    counts = pd.cut(values, bins=bins, labels=labels, right=right,
                    include_lowest=True).value_counts(sort=False)
    return [f"  - {label}: {pct(n, len(values))}" for label, n in counts.items()]


def main():
    series = sys.argv[1] if len(sys.argv) > 1 else "KXMLBGAME"
    markets = pd.read_csv(f"data/{series}_markets.csv")
    snaps = pd.read_csv(f"data/{series}_snapshots.csv")  # one row per market
    snaps["drop_reason"] = snaps["drop_reason"].fillna("")  # empty string is read back as NaN
    usable = snaps[snaps["analyzed"]]
    n = len(usable)

    eligible = markets[markets["eligible"]]
    per_event = eligible.groupby("event_ticker").size().value_counts().sort_index()

    lines = [f"# {series}: data quality of the T-24h snapshot price", ""]

    lines += ["## Funnel",
              f"- Settled markets pulled: {len(markets):,} "
              f"(historical endpoint {(markets['source'] == 'historical').sum():,}, "
              f"live endpoint {(markets['source'] == 'live').sum():,})",
              f"- Binary and settled YES/NO: {len(eligible):,}",
              f"- Events: {eligible['event_ticker'].nunique():,}; markets per event: "
              + ", ".join(f"{k} -> {v:,} events" for k, v in per_event.items())]
    for reason, count in snaps["drop_reason"].value_counts().items():
        if reason:
            lines.append(f"- Markets dropped, {reason}: {pct(count, len(snaps))}")
    lines += [f"- **Analyzed: {n:,} markets in {usable['event_ticker'].nunique():,} events**",
              f"- Close dates covered: {usable['close_time'].min()[:10]} to {usable['close_time'].max()[:10]}",
              ""]

    # How long markets were open: if markets open less than 24h before close, there is no T-24h price
    opened = pd.to_datetime(eligible["open_time"], format="ISO8601")
    closed = pd.to_datetime(eligible["close_time"], format="ISO8601")
    hours_open = (closed - opened).dt.total_seconds() / 3600
    by_year = hours_open.groupby(closed.dt.year).agg(["median", "size"])
    lines += ["## Market lifespan (hours from open to close), by year of close",
              "- " + ", ".join(f"{year}: median {row['median']:,.0f}h ({int(row['size']):,} markets)"
                               for year, row in by_year.iterrows()),
              ""]

    q = usable["volume"].quantile([0, 0.1, 0.25, 0.5, 0.75, 0.9, 1])
    lines += ["## Lifetime volume (contracts), analyzed markets",
              "- Percentiles: " + ", ".join(f"p{int(k * 100)} {v:,.0f}" for k, v in q.items()),
              "- Markets kept at each minimum-volume threshold:"]
    lines += [f"  - >= {t:,}: {pct((usable['volume'] >= t).sum(), n)}" for t in [100, 1_000, 10_000]]
    lines.append("")

    lines += ["## Stale: hours between the last trade and the snapshot",
              "Measured from the end of the hourly candle containing the last trade, so the true",
              "age of the trade is up to 1 hour more than shown.",
              f"- Median: {usable['staleness_hours'].median():.1f}h"]
    lines += distribution(usable["staleness_hours"], [0, 1, 3, 6, 12, INF],
                          ["<= 1h", "1-3h", "3-6h", "6-12h", "> 12h"])
    lines.append("")

    volume_bins = [0, 10, 100, 1_000, 10_000, INF]
    volume_labels = ["< 10", "10-99", "100-999", "1,000-9,999", "10,000+"]
    lines += ["## Thin: contracts traded in the hour that set the price",
              f"- Median: {usable['price_hour_volume'].median():,.0f}"]
    lines += distribution(usable["price_hour_volume"], volume_bins, volume_labels, right=False)
    lines += ["", "## Activity: contracts traded in the 24h before the snapshot",
              f"- Median: {usable['volume_prior_24h'].median():,.0f}"]
    lines += distribution(usable["volume_prior_24h"], volume_bins, volume_labels, right=False)
    lines.append("")

    spread_cents = ((usable["ask"] - usable["bid"]) * 100).round()  # round away float noise
    outside = (usable["price"] < usable["bid"]) | (usable["price"] > usable["ask"])
    lines += ["## Quotes at the snapshot",
              f"- Median bid-ask spread: {spread_cents.median():.0f}¢"]
    lines += distribution(spread_cents, [0, 2, 5, 10, 100], ["<= 2¢", "3-5¢", "6-10¢", "> 10¢"])
    lines += [f"- Last trade price outside the bid-ask at the snapshot: {pct(outside.sum(), n)}",
              "  (a sign the trade price is out of date relative to current quotes)", ""]

    report = "\n".join(lines)
    print(report)
    Path("results").mkdir(exist_ok=True)
    Path(f"results/{series}_data_quality.md").write_text(report)


if __name__ == "__main__":
    main()
