# Finance Analytics Portfolio｜金融市場資料分析作品集

這是一個用 Python 做金融市場資料分析的作品集。內容不是要展示「我找到多會賺錢的策略」，而是記錄我怎麼蒐集資料、整理資料、做 backtesting、比較模型，最後用 risk validation 去檢查結果是不是站得住腳。

## 為什麼做這個

我一開始只是想更有系統地研究市場，不想只靠感覺看圖或只看單一績效數字。後來慢慢把流程整理成比較像工程專案的樣子：

- 把 raw market data 下載下來
- 檢查資料缺漏、重複、異常
- 寫 Python backtest
- 比較不同 filter / timeframe / RR
- 看 max drawdown、cost stress、Monte Carlo、walk-forward
- 把失敗結果也記錄下來，不只挑最好看的圖

## Projects

| Project | 我想回答的問題 | 方法 | 目前結果 |
|---|---|---|---|
| ETHUSDT Hurst / HMM filter research | 加上 trend / regime filter 會不會比 base setup 更穩？ | Python backtest、Hurst filter、lightweight HMM proxy | 最佳 Hurst variant 在測試區間報酬 24.65%，max drawdown -8.10% |
| US100 data + stress testing | 訓練期選出來的策略，遇到更嚴格成本和壓力測試還能不能過？ | 1-minute data pipeline、70/30 split、cost stress、Monte Carlo | 8 個候選在 strict stress 下都沒通過，作為淘汰弱策略的依據 |
| XAUUSD robustness check | full-sample 看起來很強的結果，walk-forward 後還穩不穩？ | 5-year backtest、walk-forward、cost stress | full-sample 很亮眼，但 walk-forward 不穩，不能直接當結論 |

## 技術重點

| Area | Evidence |
|---|---|
| Data engineering | 下載並檢查 165 萬筆以上 US100 one-minute bars |
| Backtesting | ETHUSDT、US100、XAUUSD 多市場回測與 grid search |
| Risk validation | max drawdown、cost stress、Monte Carlo、walk-forward、trade distribution |
| Documentation | 用 README、CASE_STUDY、表格與 SVG 圖表整理結果 |

## Repo Structure

```text
.
├── index.html                 # portfolio landing page
├── styles.css                 # static page styling
├── CASE_STUDY.md              # 完整 case study
├── source-files.md            # data / artifact 說明
├── assets/                    # equity curve charts
└── data/                      # selected result tables
```

## Results Snapshot

| Case | Result | 我的解讀 |
|---|---|---|
| ETHUSDT HURST_200_055 | 24.65% return, -8.10% max DD, 31 trades | 有研究價值，但還需要更多市場和期間驗證 |
| US100 strict stress test | 8 selected candidates, all failed | 這是 useful negative result，可以避免過度相信訓練期績效 |
| XAUUSD 5-year full sample | 477.56% return, -29.48% max DD on top candidate | 歷史結果很強，但 walk-forward 不穩，不能只看這個數字 |

## Live Page

如果 GitHub Pages 已啟用：

https://xunnnn0417.github.io/finance-analytics-portfolio/

## Notes

This is a research / engineering portfolio, not financial advice.  
所有結果都是 historical tests，不代表任何策略可以直接用在實盤交易。
