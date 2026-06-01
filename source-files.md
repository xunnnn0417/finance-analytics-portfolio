# Data and Artifact Notes

This repository intentionally includes selected result artifacts instead of large raw market datasets.

## Included

| Path | Description |
|---|---|
| `data/eth-hurst-hmm-top30.csv` | Top ETHUSDT Hurst/HMM backtest variants |
| `data/us100-walk-forward.csv` | US100 walk-forward result sample |
| `data/xauusd-top-stability.csv` | XAUUSD stability-ranked candidates |
| `assets/eth-hurst-hmm-equity.svg` | ETHUSDT equity-curve comparison |
| `assets/btc-filter-suite-equity.svg` | BTC filter-suite equity-curve export |
| `assets/xauusd-cisd-equity.svg` | XAUUSD equity-curve comparison |

## Not Included

| Artifact | Reason |
|---|---|
| Full raw one-minute/tick datasets | Too large for a lightweight portfolio repo |
| Local cache folders and Python environments | Not part of the deliverable |
| Exchange credentials or API secrets | Not used or committed |

## Original Data Sources

| Market | Source Type |
|---|---|
| ETHUSDT / BTCUSDT | Exchange market data used for historical research |
| US100 / XAUUSD | Dukascopy historical market data exports |

## Reproducibility Notes

The repository is structured as a portfolio artifact, not a full production research package. The next engineering step would be to add a clean CLI runner, config files for each experiment, and unit tests for PnL accounting.
