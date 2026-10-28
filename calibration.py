"""Step 3: calibration analysis for one series.

Usage:  .venv/bin/python calibration.py KXMLBGAME
Reads   data/<series>_snapshots.csv  (from build_dataset.py)
Writes  results/<series>_calibration.csv   bin table (the chart's table view)
        results/<series>_calibration.md    summary, Brier score, robustness check
        results/<series>_calibration.png   calibration chart

The question: among contracts priced at X¢ 24h before close, what share resolved YES?
If the market is calibrated, that share is about X%.
"""

import sys
from math import sqrt
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # draw straight to a file, no window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

MIN_VOLUME = 1_000        # lifetime contracts (decided after step 2)
MAX_STALENESS_HOURS = 3   # robustness check only
N_BOOTSTRAP = 2_000       # resamples for event-bootstrap intervals
SEED = 42

SERIES_NAMES = {
    "KXMLBGAME": "MLB games",
    "KXNBAGAME": "NBA games",
    "KXCPI": "CPI",
    "KXHIGHNY": "NYC daily high temperature",
    "KXAPRPOTUS": "RCP presidential approval",
    "KXBTCMAXMON": "BTC monthly high",
    "KXBTCMINMON": "BTC monthly low",
}

# Chart colors: dataviz reference palette, light mode
SURFACE = "#fcfcfb"
SERIES_COLOR = "#2a78d6"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"


def load_games(series):
    """Analyzed markets with enough lifetime volume.

    (Named for the MLB case; for multi-market series each row is a market, not a game.)
    """
    games = pd.read_csv(f"data/{series}_snapshots.csv")
    return games[games["analyzed"] & (games["volume"] >= MIN_VOLUME)]


def one_market_per_event(games):
    """True for two-team series (favorite side only): every row is an independent event."""
    return games["event_ticker"].is_unique


def describe(games):
    events = games["event_ticker"].nunique()
    if one_market_per_event(games):
        return f"favorite side of {events:,} games"
    return f"{len(games):,} markets in {events:,} events"


def wilson_interval(yes, n, z=1.96):
    """95% Wilson score interval for the proportion yes / n.

    Unlike the textbook p ± 1.96·sqrt(p(1-p)/n), it never leaves [0, 1] and stays
    accurate for small n and for rates near 0% or 100%. It pulls the center slightly
    toward 50% and widens the interval, by amounts that shrink as n grows.
    """
    p = yes / n
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    half_width = z * sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return center - half_width, center + half_width


def event_bootstrap_intervals(games, group_col):
    """95% interval for the YES rate of each group (e.g., price bin), resampling whole events.

    Markets in the same event are linked (exactly one range wins; "above X" thresholds are
    nested), so treating them as independent would make intervals too narrow. Instead we
    redraw the events themselves: draw as many events as we have, with replacement,
    recompute each group's YES rate, repeat N_BOOTSTRAP times, and keep the middle 95%.

    Floor: when YES (or NO) results in a group are rare, the bootstrap can't produce resamples
    far from the observed rate, so its interval comes out too narrow (zero width if every
    result is the same). So the interval is never narrower than a Wilson interval that counts
    each event in the group once, at the group's YES rate.
    """
    # Rows = events, columns = groups: how many markets / YES results each event adds to each group
    table = games.pivot_table(index="event_ticker", columns=group_col, values="resolved_yes",
                              aggfunc=["count", "sum"], fill_value=0)
    n, yes = table["count"].to_numpy(), table["sum"].to_numpy()
    events = len(n)
    rng = np.random.default_rng(SEED)
    # Each row of `draws`: how many times each event was picked in one resample
    draws = rng.multinomial(events, np.full(events, 1 / events), size=N_BOOTSTRAP)
    with np.errstate(invalid="ignore", divide="ignore"):  # a group can be empty in a resample
        rates = (draws @ yes) / (draws @ n)
    low, high = np.nanpercentile(rates, [2.5, 97.5], axis=0)

    intervals = {}
    for i, group in enumerate(table["count"].columns):
        total, total_yes = n[:, i].sum(), yes[:, i].sum()
        events_in_group = (n[:, i] > 0).sum()
        floor_low, floor_high = wilson_interval(events_in_group * total_yes / total, events_in_group)
        intervals[group] = (min(low[i], floor_low), max(high[i], floor_high))
    return intervals


def add_bins(games):
    cents = (games["price"] * 100).round().astype(int)  # round first: 0.57 * 100 = 56.999...
    return games.assign(bin_low=cents // 10 * 10)


def overall_interval(games):
    """95% interval for the overall YES rate, using the same method as the bins."""
    if one_market_per_event(games):
        return wilson_interval(games["resolved_yes"].sum(), len(games))
    return event_bootstrap_intervals(games.assign(everything=0), "everything")[0]


def calibration_table(games):
    """One row per non-empty 10¢ bin: average price vs. share that resolved YES.

    Intervals: Wilson when each event contributes one market (two-team series),
    otherwise an event bootstrap (see event_bootstrap_intervals).
    """
    games = add_bins(games)
    bootstrap = None if one_market_per_event(games) else event_bootstrap_intervals(games, "bin_low")

    rows = []
    for bin_low, group in games.groupby("bin_low"):
        n, yes = len(group), int(group["resolved_yes"].sum())
        avg_price, yes_rate = group["price"].mean(), yes / n
        ci_low, ci_high = bootstrap[bin_low] if bootstrap else wilson_interval(yes, n)
        rows.append({
            "bin": f"{bin_low}-{bin_low + 9}¢",
            "bin_low": bin_low,
            "n": n,
            "events": group["event_ticker"].nunique(),
            "yes": yes,
            "avg_price": avg_price,                     # average implied probability
            "yes_rate": yes_rate,                       # actual frequency
            "ci_low": ci_low,
            "ci_high": ci_high,
            "gap_pts": (yes_rate - avg_price) * 100,    # + means YES happened more than priced
            "price_in_ci": ci_low <= avg_price <= ci_high,
        })
    return pd.DataFrame(rows)


def brier_score(games):
    """Mean squared error of the price as a forecast of the 0/1 outcome. Lower is better."""
    return ((games["price"] - games["resolved_yes"]) ** 2).mean()


def robust_subset(games):
    """Drop prices that may be out of date: last trade outside the bid-ask, or > 3h stale."""
    in_spread = (games["price"] >= games["bid"]) & (games["price"] <= games["ask"])
    fresh = games["staleness_hours"] <= MAX_STALENESS_HOURS
    return games[in_spread & fresh]


def report(series, games, table, robust, robust_table):
    base_rate = games["resolved_yes"].mean()
    overall_low, overall_high = overall_interval(games)
    method = "Wilson" if one_market_per_event(games) else "event bootstrap"
    lines = [
        f"# {series}: calibration 24h before close", "",
        f"- Analyzed: {describe(games)} (lifetime volume >= {MIN_VOLUME:,} contracts)",
        f"- Confidence intervals: 95%, {method}",
        f"- Close dates: {games['close_time'].min()[:10]} to {games['close_time'].max()[:10]}",
        f"- Average price: {games['price'].mean() * 100:.1f}¢ | Share resolved YES: {base_rate:.1%} "
        f"(95% CI {overall_low:.1%} – {overall_high:.1%})",
        f"- Brier score: {brier_score(games):.4f} (reference, always predicting {base_rate:.1%}: "
        f"{base_rate * (1 - base_rate):.4f}; lower is better)",
        f"- Bins where the average price is inside the 95% CI: {table['price_in_ci'].sum()} of {len(table)}",
        "", "## By price bin", "",
        "| Bin | Markets | Events | Avg price | Resolved YES | 95% CI | Gap (pts) |",
        "|---|---:|---:|---:|---:|---|---:|",
    ]
    for r in table.itertuples():
        lines.append(f"| {r.bin} | {r.n:,} | {r.events:,} | {r.avg_price * 100:.1f}¢ | {r.yes_rate:.1%} | "
                     f"{r.ci_low:.1%} – {r.ci_high:.1%} | {r.gap_pts:+.1f} |")

    lines += [
        "", f"## Robustness: excluding prices outside the bid-ask or more than {MAX_STALENESS_HOURS}h stale", "",
        f"- Markets: {len(robust):,} ({len(games) - len(robust):,} removed)",
        f"- Brier score: {brier_score(robust):.4f} (main: {brier_score(games):.4f})", "",
        "| Bin | Markets (main) | Gap (main) | Markets (robust) | Gap (robust) |",
        "|---|---:|---:|---:|---:|",
    ]
    merged = table.merge(robust_table, on="bin", how="left", suffixes=("", "_robust"))
    for r in merged.itertuples():
        if pd.isna(r.n_robust):
            lines.append(f"| {r.bin} | {r.n:,} | {r.gap_pts:+.1f} | 0 | – |")
        else:
            lines.append(f"| {r.bin} | {r.n:,} | {r.gap_pts:+.1f} | {int(r.n_robust):,} | {r.gap_pts_robust:+.1f} |")
    return "\n".join(lines) + "\n"


def style_axes(ax):
    """Recessive chrome: hairline solid grid, no top/right frame, muted tick labels."""
    ax.set_facecolor(SURFACE)
    ax.grid(color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    for side in ["left", "bottom"]:
        ax.spines[side].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelcolor=INK_SECONDARY, length=0, labelsize=9)


def plot_calibration(table, title, subtitle, path):
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
    fig = plt.figure(figsize=(6.4, 8.4), facecolor=SURFACE)

    # Axes placed by hand so the top panel is exactly square (0.78 * 6.4in wide = 0.594 * 8.4in tall).
    # That makes the perfect-calibration line a true 45° line.
    top = fig.add_axes([0.13, 0.30, 0.78, 0.594])
    bottom = fig.add_axes([0.13, 0.08, 0.78, 0.15], sharex=top)

    # Top: average price vs. share resolved YES, with 95% Wilson CIs
    style_axes(top)
    top.plot([0, 100], [0, 100], color=MUTED, linewidth=1, zorder=1)
    top.text(25, 27, "Perfect calibration", rotation=45, rotation_mode="anchor",
             color=MUTED, fontsize=9, ha="center", va="bottom")
    x, y = (table["avg_price"] * 100).to_numpy(), (table["yes_rate"] * 100).to_numpy()
    top.errorbar(x, y, yerr=[y - table["ci_low"].to_numpy() * 100, table["ci_high"].to_numpy() * 100 - y],
                 fmt="o", color=SERIES_COLOR, elinewidth=1.5, capsize=0, markersize=8,
                 markeredgecolor=SURFACE, markeredgewidth=2, zorder=3,
                 clip_on=False)  # a point at 0% or 100% stays whole instead of cut in half
    top.set_xlim(0, 100)
    top.set_ylim(0, 100)
    top.set_xticks(range(0, 101, 10))
    top.set_yticks(range(0, 101, 10))
    top.set_ylabel("Resolved YES (%)", color=INK_SECONDARY, fontsize=10)
    top.tick_params(labelbottom=False)

    # Bottom: how many games stand behind each point
    style_axes(bottom)
    bottom.grid(False)
    bottom.bar(table["bin_low"] + 5, table["n"], width=5, color=SERIES_COLOR)
    for r in table.itertuples():
        bottom.text(r.bin_low + 5, r.n, f"{r.n:,}", ha="center", va="bottom",
                    color=INK_SECONDARY, fontsize=8)
    bottom.set_ylim(0, table["n"].max() * 1.35)
    bottom.set_yticks([])  # every bar is labeled, so the axis would repeat the labels
    bottom.set_ylabel("Games", color=INK_SECONDARY, fontsize=10)
    bottom.set_xlabel("Price 24h before close (¢) = implied probability of YES",
                      color=INK_SECONDARY, fontsize=10)

    fig.text(0.13, 0.965, title, color=INK, fontsize=13, fontweight="semibold")
    fig.text(0.13, 0.94, subtitle, color=INK_SECONDARY, fontsize=9)
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)


def main():
    series = sys.argv[1] if len(sys.argv) > 1 else "KXMLBGAME"
    games = load_games(series)
    table = calibration_table(games)
    robust = robust_subset(games)

    Path("results").mkdir(exist_ok=True)
    table.to_csv(f"results/{series}_calibration.csv", index=False)
    text = report(series, games, table, robust, calibration_table(robust))
    Path(f"results/{series}_calibration.md").write_text(text)
    print(text)

    name = SERIES_NAMES.get(series, series)
    method = "Wilson" if one_market_per_event(games) else "event-bootstrap"
    subtitle = (f"{describe(games).capitalize()}, closing {games['close_time'].min()[:10]} to "
                f"{games['close_time'].max()[:10]} · 95% {method} intervals")
    plot_calibration(table, f"Kalshi {name}: price 24h before close vs. outcome",
                     subtitle, f"results/{series}_calibration.png")
    print(f"wrote results/{series}_calibration.csv, .md, .png")


if __name__ == "__main__":
    main()
