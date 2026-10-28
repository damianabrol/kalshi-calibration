"""Step 4: compare calibration across categories.

Usage:  .venv/bin/python compare.py
Reads   data/<series>_snapshots.csv for every series in GROUPS
        (run pull_data.py and build_dataset.py for each series first)
Writes  results/comparison.md   summary per group, longshots vs. favorites, notes
        results/comparison.csv  every bin of every group (the chart's table view)
        results/comparison.png  small multiples: one calibration panel per group
"""

from math import ceil
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from calibration import (INK, INK_SECONDARY, MIN_VOLUME, MUTED, N_BOOTSTRAP, SERIES_COLOR, SURFACE,
                         brier_score, calibration_table, describe, load_games,
                         overall_interval, style_axes)

# (name, category, series tickers). Crypto pools the monthly high and low series,
# which are each too small on their own.
GROUPS = [
    ("MLB games", "Sports", ["KXMLBGAME"]),
    ("NBA games", "Sports", ["KXNBAGAME"]),
    ("NFL games", "Sports", ["KXNFLGAME"]),
    ("CPI", "Economics", ["KXCPI"]),
    ("NYC daily high temp", "Weather", ["KXHIGHNY"]),
    ("RCP approval", "Politics", ["KXAPRPOTUS"]),
    ("BTC monthly high/low", "Crypto", ["KXBTCMAXMON", "KXBTCMINMON"]),
]
LONGSHOT_MAX = 0.20   # priced below 20¢
FAVORITE_MIN = 0.80   # priced at 80¢ or more


def price_band_row(name, games, label):
    """Average price vs. share resolved YES for one price band, with a 95% interval."""
    if games.empty:
        return f"| {name} | {label} | 0 | – | – | – | – |"
    low, high = overall_interval(games)
    avg_price, yes_rate = games["price"].mean(), games["resolved_yes"].mean()
    return (f"| {name} | {label} | {len(games):,} | {avg_price * 100:.1f}¢ | {yes_rate:.1%} | "
            f"{low:.1%} – {high:.1%} | {(yes_rate - avg_price) * 100:+.1f} |")


def overround_row(name, tickers, games):
    """Two-team series: how far both sides' T-24h prices sum above $1, and the favorite net of it.

    Either side of a game can be bought, so the two prices usually add up to a bit more than
    $1. Dividing the favorite's price by that sum ("normalizing") removes the extra, giving a
    fair-odds price to compare with how often favorites actually won.
    """
    snaps = pd.concat([pd.read_csv(f"data/{t}_snapshots.csv") for t in tickers])
    both_sides = snaps.groupby("event_ticker")["price"].sum()
    total = games["event_ticker"].map(both_sides)
    low, high = overall_interval(games)
    return (f"| {name} | {total.mean() * 100:.2f}¢ | {games['price'].mean() * 100:.1f}¢ | "
            f"{(games['price'] / total).mean() * 100:.1f}¢ | {games['resolved_yes'].mean():.1%} "
            f"({low:.1%} – {high:.1%}) |")


def plot_small_multiples(results, path, strip=False):
    """One calibration panel per group: a two-row grid, or (strip=True) a single row sized for a
    one-page memo, where the memo's table carries the sample sizes and Brier scores."""
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
    n = len(results)
    nrows, ncols, figsize = (1, n, (11, 2.1)) if strip else (2, ceil(n / 2), (14.5, 8.2))
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize, facecolor=SURFACE, squeeze=False,
                             gridspec_kw={"hspace": 0.42, "wspace": 0.25 if strip else 0.18})
    for ax in axes.flat[n:]:  # an odd number of groups leaves an empty slot in the grid
        ax.set_visible(False)
    for ax, (name, category, games, table) in zip(axes.flat, results):
        style_axes(ax)
        ax.set_aspect("equal")  # square panels so the 45° line is a true 45°
        ax.plot([0, 100], [0, 100], color=MUTED, linewidth=1, zorder=1)
        x, y = (table["avg_price"] * 100).to_numpy(), (table["yes_rate"] * 100).to_numpy()
        ax.errorbar(x, y, yerr=[y - table["ci_low"].to_numpy() * 100, table["ci_high"].to_numpy() * 100 - y],
                    fmt="o", color=SERIES_COLOR, elinewidth=1.3, capsize=0, markersize=6,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3, clip_on=False)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        if strip:
            ax.set_xticks([0, 50, 100])
            ax.set_yticks([0, 50, 100])
            ax.tick_params(labelsize=8)
            ax.set_title(name, loc="left", color=INK, fontsize=9, fontweight="semibold")
        else:
            ax.set_xticks(range(0, 101, 20))
            ax.set_yticks(range(0, 101, 20))
            ax.set_title(f"{name} · {category}", loc="left", color=INK, fontsize=11,
                         fontweight="semibold", pad=20)
            ax.text(0, 1.03, f"{describe(games)} · Brier {brier_score(games):.3f}",
                    transform=ax.transAxes, color=INK_SECONDARY, fontsize=8)
    label_size = 8 if strip else 9
    for i, ax in enumerate(axes.flat[:n]):
        if i + ncols >= n:  # no panel below this one, so it carries the x-axis label
            ax.set_xlabel("Price 24h before close (¢)" if not strip else "Price (¢)",
                          color=INK_SECONDARY, fontsize=label_size)
    for ax in axes[:, 0]:
        ax.set_ylabel("Resolved YES (%)", color=INK_SECONDARY, fontsize=label_size)

    if not strip:  # the memo puts its own caption under the strip
        fig.text(0.06, 0.965, "Kalshi calibration by category, 24h before close", color=INK,
                 fontsize=14, fontweight="semibold")
        fig.text(0.06, 0.937, "Each point is a 10¢ price bin; bars are 95% intervals; gray line = perfect "
                 "calibration. Sports panels show each game's favorite side.", color=INK_SECONDARY, fontsize=9)
    fig.savefig(path, dpi=200, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)


def main():
    results, bins = [], []
    for name, category, tickers in GROUPS:
        games = pd.concat([load_games(t) for t in tickers], ignore_index=True)
        table = calibration_table(games)
        results.append((name, category, games, table))
        bins.append(table.assign(group=name, category=category))

    Path("results").mkdir(exist_ok=True)
    pd.concat(bins).to_csv("results/comparison.csv", index=False)

    lines = ["# Calibration by category, 24h before close", "",
             f"Lifetime volume >= {MIN_VOLUME:,} contracts. Two-team sports: favorite side of each game, "
             f"Wilson intervals. All other series: every market, event-bootstrap intervals "
             f"({N_BOOTSTRAP:,} resamples).", "",
             "| Group | Category | Analyzed | Close dates | Avg price | Resolved YES (95% CI) | Gap (pts) | "
             "Brier | Reference | Bins with avg price inside CI |",
             "|---|---|---|---|---:|---|---:|---:|---:|---|"]
    for name, category, games, table in results:
        low, high = overall_interval(games)
        base = games["resolved_yes"].mean()
        lines.append(
            f"| {name} | {category} | {describe(games)} | {games['close_time'].min()[:10]} to "
            f"{games['close_time'].max()[:10]} | {games['price'].mean() * 100:.1f}¢ | "
            f"{base:.1%} ({low:.1%} – {high:.1%}) | {(base - games['price'].mean()) * 100:+.1f} | "
            f"{brier_score(games):.4f} | {base * (1 - base):.4f} | {table['price_in_ci'].sum()} of {len(table)} |")
    all_games = pd.concat([games for _, _, games, _ in results])
    all_tables = pd.concat([table for _, _, _, table in results])
    lines += ["", f"Total: {len(all_games):,} markets in {all_games['event_ticker'].nunique():,} events. "
              f"Average price inside the bin's 95% CI in {all_tables['price_in_ci'].sum()} of "
              f"{len(all_tables)} bins."]

    lines += ["", "## Longshots and heavy favorites", "",
              f"Longshots: priced below {LONGSHOT_MAX * 100:.0f}¢. Heavy favorites: priced at "
              f"{FAVORITE_MIN * 100:.0f}¢ or more. For two-team sports only the favorite side is analyzed, "
              "so a favorite at 85¢ is the same bet as its opponent's 15¢ longshot.", "",
              "| Group | Band | Markets | Avg price | Resolved YES | 95% CI | Gap (pts) |",
              "|---|---|---:|---:|---:|---|---:|"]
    for name, category, games, table in results:
        lines.append(price_band_row(name, games[games["price"] < LONGSHOT_MAX], "longshots"))
        lines.append(price_band_row(name, games[games["price"] >= FAVORITE_MIN], "heavy favorites"))

    lines += ["", "## Two-team sports: the overround", "",
              "Both sides of a game can be bought, and their prices usually add up to a bit more than $1. "
              "Dividing the favorite's price by the sum of both sides removes that extra.", "",
              "| Group | Both sides sum to (avg) | Favorite's price (avg) | Net of overround (avg) | "
              "Favorite won (95% CI) |",
              "|---|---:|---:|---:|---|"]
    for (name, category, tickers), (_, _, games, _) in zip(GROUPS, results):
        if games["event_ticker"].is_unique:  # two-team series: one analyzed market per game
            lines.append(overround_row(name, tickers, games))

    report = "\n".join(lines) + "\n"
    Path("results/comparison.md").write_text(report)
    print(report)
    plot_small_multiples(results, "results/comparison.png")
    plot_small_multiples(results, "results/comparison_strip.png", strip=True)
    print("wrote results/comparison.md, .csv, .png, comparison_strip.png")


if __name__ == "__main__":
    main()
