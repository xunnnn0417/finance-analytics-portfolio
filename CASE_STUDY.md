# Case Study: Market Data Research and Robustness Testing

## Overview

This project is a collection of market-data research experiments I built with Python. I wanted the workflow to look closer to how an engineer or quantitative researcher would document a project: define the question, explain the data, show the method, present the results, and state the limits clearly.

The important part is not whether a backtest looks profitable. The important part is whether the result survives basic sanity checks: data quality, transaction costs, drawdown, out-of-sample behavior, and randomization stress.

## Project Goals

| Goal | Why It Matters |
|---|---|
| Build repeatable data pipelines | Market research is only useful if the input data can be checked and reproduced |
| Compare model variants | A result is more useful when it is compared against a baseline |
| Test downside risk | Returns without drawdown and cost checks are misleading |
| Keep failed results | Negative results help avoid overfitting and false confidence |

## Case 1: ETHUSDT Hurst / HMM Filter Research

### Question

Can a trend or regime filter improve a base ETHUSDT setup, or does it only make the backtest look more complicated?

### Setup

| Item | Value |
|---|---|
| Market | Bybit ETHUSDT perpetual |
| Window | 2024-05-26 to 2026-05-26 |
| Risk model | 1% per trade |
| Fee assumption | 0.055% per side |
| Filters | BASE, HURST_100_055, HURST_200_055, HMM_2STATE, HMM_3STATE |
| Search | HTF/LTF combinations with RR values from 2.0 to 4.0 |

### Top Results

| Rank | Filter | HTF | LTF | RR | Return | Max DD | Trades |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | HURST_200_055 | 12h | 4h | 4.0 | 24.65% | -8.10% | 31 |
| 2 | HURST_100_055 | 12h | 4h | 4.0 | 23.37% | -8.10% | 32 |
| 3 | BASE | 12h | 4h | 4.0 | 22.05% | -8.10% | 33 |
| 7 | HMM_3STATE | 12h | 5m | 4.0 | 14.70% | -4.07% | 15 |

![ETH Hurst/HMM equity curves](assets/eth-hurst-hmm-equity.svg)

### Takeaway

The Hurst filter improved the top result in this window, while the HMM proxy reduced trade frequency and drawdown in some variants. I would not treat this as proof that the filter works generally. It is a candidate result that should be tested across more markets and time periods.

## Case 2: US100 Data Pipeline and Strict Stress Testing

### Question

If a strategy candidate looks good in training, does it survive stricter costs, Monte Carlo checks, and walk-forward validation?

### Data Pipeline

I downloaded and converted Dukascopy tick data into one-minute OHLCV bars, then generated a quality report.

| Check | Result |
|---|---:|
| Date range | 2021-05-28 to 2026-05-27 |
| Total bars | 1,650,628 |
| Duplicate open times | 0 |
| Abnormal OHLC rows | 0 |
| Missing one-minute ratio | 37.23% |
| Gap segments | 1,452 |

### Stress Test Design

| Item | Value |
|---|---|
| Market | Dukascopy USATECH.IDX/USD |
| Test window | 2025-05-28 to 2026-05-28 |
| Grid size | 270 combinations |
| Selection method | 70/30 split using return, Calmar, and stability candidates |
| Stress checks | cost multipliers, Monte Carlo, walk-forward, loss streaks |

### Results

| Metric | Result |
|---|---:|
| Selected candidates | 8 |
| Strict-stress classification | 8 failed |
| Walk-forward segments | 6 |
| Positive OOS segments | 2 / 6 |
| Average OOS return | 0.30% |
| Worst OOS segment | -6.41% |

### Takeaway

This was a useful negative result. A weaker portfolio would hide it, but an engineering portfolio should show that the process can reject bad candidates. The failed stress test is evidence that the workflow is not only selecting the best historical curve.

## Case 3: XAUUSD Full-Sample vs Walk-Forward Robustness

### Question

When a full-sample backtest looks strong, how much confidence should I actually place in it?

### Setup

| Item | Value |
|---|---|
| Market | Dukascopy XAUUSD mid OHLC |
| Window | 2021-05-28 to 2026-05-28 |
| Strategy family | HTF Liquidity Sweep + LTF CISD 50% Limit Entry |
| Checks | Full sample, cost stress, Monte Carlo, walk-forward |

### Full-Sample Candidates

| HTF -> LTF | RR | Return | Max DD | Trades | Grade |
|---|---:|---:|---:|---:|---|
| 2h -> 5m | 4.0 | 477.56% | -29.48% | 806 | B |
| 2h -> 1m | 4.0 | 246.10% | -22.83% | 955 | C |
| 2h -> 5m | 3.5 | 260.19% | -26.74% | 819 | C |

![XAUUSD equity curves](assets/xauusd-cisd-equity.svg)

### Walk-Forward Reality Check

| Test | Result |
|---|---:|
| 3m train / 1m test segments | 57 |
| 3m/1m positive ratio | 45.61% |
| 3m/1m total sum | -8.64% |
| 6m train / 1m test segments | 54 |
| 6m/1m positive ratio | 57.41% |
| 6m/1m total sum | -14.78% |

### Takeaway

The full-sample numbers are strong, but the walk-forward results make the conclusion much less certain. This is exactly why I prefer documenting robustness checks alongside performance charts.

## What I Would Improve Next

| Improvement | Reason |
|---|---|
| Add a clean CLI runner | Make every experiment easier to reproduce |
| Export charts from scripts automatically | Reduce manual reporting work |
| Add config files for each experiment | Keep assumptions explicit |
| Separate raw data from result artifacts | Keep the GitHub repo lightweight |
| Add tests for backtest accounting | Reduce risk of incorrect PnL or drawdown calculations |

## Conclusion

The main outcome of this project is a repeatable research habit: collect data, validate data, test assumptions, compare variants, and document uncertainty. I treat strong results as candidates, not final answers, and I treat failed stress tests as useful information rather than something to hide.

That is the engineering value of this portfolio: it shows the workflow behind the result.
