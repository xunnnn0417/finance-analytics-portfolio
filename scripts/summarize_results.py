"""Summarize selected CSV result artifacts.

The raw tick/minute data is not included in this repository, so this script
does not reproduce the full backtests. It summarizes the exported result
tables that are included in `data/`.
"""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def read_rows(filename: str) -> list[dict[str, str]]:
    with (DATA / filename).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def number(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def best_by(rows: list[dict[str, str]], key: str) -> dict[str, str]:
    return max(rows, key=lambda row: number(row.get(key, "0")))


def main() -> int:
    eth = read_rows("eth-hurst-hmm-top30.csv")
    us100 = read_rows("us100-walk-forward.csv")
    xauusd = read_rows("xauusd-top-stability.csv")

    best_eth = best_by(eth, "return_pct")
    best_xauusd = best_by(xauusd, "return_pct")

    us100_oos_returns = [number(row["oos_return_pct"]) for row in us100]
    us100_positive = sum(1 for value in us100_oos_returns if value > 0)
    us100_trades = sum(number(row["oos_trades"]) for row in us100)

    print("# Result Summary")
    print()
    print("## ETHUSDT")
    print(
        "- best variant: "
        f"{best_eth['filter']} {best_eth['htf']}->{best_eth['ltf']} RR{best_eth['rr']}"
    )
    print(
        "- result: "
        f"{number(best_eth['return_pct']):.2f}% return, "
        f"{number(best_eth['maxdd_pct']):.2f}% max drawdown, "
        f"{int(number(best_eth['trades']))} trades"
    )
    print()

    print("## US100 walk-forward sample")
    print(f"- segments: {len(us100)}")
    print(f"- positive OOS segments: {us100_positive}/{len(us100)}")
    print(f"- average OOS return: {mean(us100_oos_returns):.2f}%")
    print(f"- total OOS trades in sample: {int(us100_trades)}")
    print()

    print("## XAUUSD")
    print(
        "- best full-sample candidate: "
        f"{best_xauusd['parameter_set']}"
    )
    print(
        "- result: "
        f"{number(best_xauusd['return_pct']):.2f}% return, "
        f"{number(best_xauusd['maxdd_pct']):.2f}% max drawdown, "
        f"grade {best_xauusd['grade']}"
    )
    print()
    print("Note: these are exported result summaries, not a full backtest rerun.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
