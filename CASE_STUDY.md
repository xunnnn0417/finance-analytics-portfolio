# Case Study｜金融市場資料研究與穩健性測試

## Overview

這個 project 是我用 Python 做金融市場資料研究的整理。  
我希望它看起來不是單純的交易截圖，而是像一個工程專案：先定義問題，再說資料怎麼來、方法怎麼做、結果是什麼、限制在哪裡。

對我來說，重點不是某一條 equity curve 看起來多漂亮，而是這個結果有沒有經過基本檢查：data quality、transaction costs、drawdown、out-of-sample behavior、Monte Carlo risk。

## Project Goals

| Goal | Why It Matters |
|---|---|
| 建立可重複的 data pipeline | 沒有乾淨資料，後面的分析都不可靠 |
| 比較不同 model variants | 不能只看單一策略，要知道它比 baseline 好在哪 |
| 測 downside risk | return 沒有搭配 drawdown 和 cost checks 會很容易誤判 |
| 保留 failed results | 失敗結果可以幫助排除 overfitting 和 false confidence |

## Case 1：ETHUSDT Hurst / HMM Filter Research

### Question

我想知道：如果在 base setup 上加入 trend / regime filter，結果會不會更穩？  
還是只是讓 backtest 變複雜，但實際上沒有增加價值？

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

Hurst filter 在這個測試區間有改善 top result，HMM proxy 則讓交易次數變少，也降低部分回撤。  
但我不會直接把這個結果解讀成「filter 一定有效」。它比較像是一個 candidate，需要放到更多市場、更多時間區間繼續測。

## Case 2：US100 Data Pipeline and Strict Stress Testing

### Question

如果一個 strategy candidate 在 training period 看起來不錯，那它遇到更嚴格的 costs、Monte Carlo、walk-forward 後還站得住腳嗎？

### Data Pipeline

我用 Python 從 Dukascopy 下載 tick data，轉成 one-minute OHLCV bars，然後產生 data quality report。

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

這個 case 的重點不是找到一個看起來很強的策略，而是它最後能淘汰不穩定的 candidates。  
如果 portfolio 只放漂亮的結果，其實很容易變成 cherry-picking。這個 failed stress test 反而可以證明：我不是只挑最好的 historical curve，而是有做 rejection process。

## Case 3：XAUUSD Full-Sample vs Walk-Forward Robustness

### Question

如果 full-sample backtest 看起來很強，我到底該相信多少？

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

Full-sample numbers 很強，但 walk-forward 結果讓我沒辦法直接下結論。  
這也是我覺得 documenting robustness checks 很重要的原因：它可以提醒自己不要只被漂亮的 historical performance 影響。

## What I Would Improve Next

| Improvement | Reason |
|---|---|
| Add a clean CLI runner | 讓每個 experiment 可以更容易重跑 |
| Export charts from scripts automatically | 減少手動整理報告的時間 |
| Add config files for each experiment | 讓 assumptions 更清楚 |
| Separate raw data from result artifacts | 保持 GitHub repo 輕量 |
| Add tests for backtest accounting | 降低 PnL 或 drawdown 算錯的風險 |

## Conclusion

這個 project 最有價值的地方不是單一 return number，而是一套研究習慣：collect data、validate data、define assumptions、compare variants、stress-test results，最後把限制也寫下來。

Strong backtests 對我來說只是 candidates。Failed stress tests 也不是浪費，因為它們可以幫我排除不穩定的想法。  
這就是我想在這個 portfolio 裡呈現的 engineering value。
