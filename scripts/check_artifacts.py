"""Check that the portfolio's expected data and chart artifacts exist.

This script is intentionally small and dependency-free. It validates the
published portfolio artifacts, not the original raw market-data pipeline.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    "README.md",
    "CASE_STUDY.md",
    "source-files.md",
    "data/summary.csv",
    "data/eth-hurst-hmm-top30.csv",
    "data/us100-walk-forward.csv",
    "data/xauusd-top-stability.csv",
    "assets/eth-hurst-hmm-equity.svg",
    "assets/xauusd-cisd-equity.svg",
]

EXPECTED_COLUMNS = {
    "data/summary.csv": {"case", "period", "method", "key_result", "portfolio_value"},
    "data/eth-hurst-hmm-top30.csv": {
        "symbol",
        "market",
        "filter",
        "htf",
        "ltf",
        "rr",
        "return_pct",
        "maxdd_pct",
        "trades",
    },
    "data/us100-walk-forward.csv": {
        "train_start",
        "train_end",
        "test_start",
        "test_end",
        "train_return_pct",
        "oos_return_pct",
        "oos_maxdd_pct",
        "oos_trades",
    },
    "data/xauusd-top-stability.csv": {
        "symbol",
        "market",
        "strategy_name",
        "htf",
        "ltf",
        "rr",
        "return_pct",
        "maxdd_pct",
        "trades",
        "stability_score",
        "grade",
    },
}


def read_header(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        return set(next(reader))


def main() -> int:
    failures: list[str] = []

    for rel_path in EXPECTED_FILES:
        path = ROOT / rel_path
        if not path.exists():
            failures.append(f"missing file: {rel_path}")

    for rel_path, expected in EXPECTED_COLUMNS.items():
        path = ROOT / rel_path
        if not path.exists():
            continue
        actual = read_header(path)
        missing = expected - actual
        if missing:
            failures.append(f"{rel_path} missing columns: {', '.join(sorted(missing))}")

    if failures:
        print("Artifact check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Artifact check passed.")
    print(f"Checked {len(EXPECTED_FILES)} files and {len(EXPECTED_COLUMNS)} CSV schemas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
