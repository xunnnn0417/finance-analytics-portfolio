# Scripts

These scripts work with the result artifacts included in this repository.

They do not reproduce the full raw-data backtests because the raw tick/minute
datasets are intentionally not committed to GitHub.

## Commands

```bash
python scripts/check_artifacts.py
python scripts/summarize_results.py
```

## What they do

- `check_artifacts.py` verifies expected CSV/chart files and required CSV columns.
- `summarize_results.py` reads the included CSV exports and prints a short Markdown summary.

The next step would be to add raw-data loaders and backtest runners once the
data pipeline is cleaned up for public release.
