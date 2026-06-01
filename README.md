# Finance Analytics Portfolio

Market data research projects built with Python. This repository documents how I collect raw market data, run strategy research, compare filters, and stress-test results instead of only showing the best-looking backtest.

## Why This Exists

I started this as a personal research workflow for understanding markets with data. The goal is not to present a trading signal or investment advice. The goal is to show the engineering process behind market research:

- collect and validate raw data
- define testable assumptions
- run parameter sweeps
- compare model variants
- check drawdown, costs, walk-forward behavior, and Monte Carlo risk
- document both good and bad results

## Projects

| Project | Question | Method | Key Finding |
|---|---|---|---|
| ETHUSDT Hurst/HMM filter research | Can trend/regime filters improve a base setup? | Python backtest, Hurst filters, lightweight HMM proxy | Best Hurst variant returned 24.65% with -8.10% max drawdown in this test window |
| US100 data and stress testing | Does a selected strategy survive stricter assumptions? | 1-minute data pipeline, 70/30 split, cost stress, Monte Carlo | Selected candidates failed strict stress checks, which helped reject weak setups |
| XAUUSD robustness check | Do strong full-sample results hold up out of sample? | 5-year backtest, walk-forward, cost stress | Full-sample results looked strong, but walk-forward behavior was unstable |

## Highlights

| Area | Evidence |
|---|---|
| Data engineering | Downloaded and validated 1.65M+ US100 one-minute bars |
| Backtesting | Multi-timeframe and RR grid tests across ETHUSDT, US100, and XAUUSD |
| Risk validation | Max drawdown, cost stress, Monte Carlo, walk-forward, and trade distribution checks |
| Documentation | Case study, summary tables, charts, and source-file index |

## Repository Structure

```text
.
├── index.html                 # visual portfolio page
├── styles.css                 # static page styling
├── CASE_STUDY.md              # full project write-up
├── source-files.md            # local source-file index
├── assets/                    # exported equity-curve charts
└── data/                      # selected result tables
```

## Results Snapshot

| Case | Result | Interpretation |
|---|---|---|
| ETHUSDT HURST_200_055 | 24.65% return, -8.10% max DD, 31 trades | Interesting candidate, but needs more validation |
| US100 strict stress test | 8 selected candidates, all failed | Useful negative result; prevents overfitting |
| XAUUSD 5-year full sample | 477.56% return, -29.48% max DD on top candidate | Strong historical result, but not reliable alone |

## Live Page

If GitHub Pages is enabled for this repository:

https://xunnnn0417.github.io/finance-analytics-portfolio/

## Notes

This is a research and engineering portfolio, not financial advice. The included results are historical tests and should not be interpreted as live trading recommendations.
