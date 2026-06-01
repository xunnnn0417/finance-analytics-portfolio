# Finance Analytics Portfolio｜金融市場資料研究紀錄

這個 repo 是我整理金融市場資料研究的紀錄。重點不是證明某個策略一定能賺錢，而是記錄我怎麼取得資料、清理資料、設定假設、做 backtesting、比較不同版本，最後用風險檢查去判斷結果能不能站得住腳。

我後來發現，一個回測結果在某段期間看起來很好，不代表它真的可靠。只要加入交易成本、最大回撤、樣本外測試或 walk-forward 檢查，結果可能就會完全不一樣。所以這個 repo 比較像研究筆記和工程紀錄，而不是績效展示頁。

## 這個 repo 在做什麼

- 整理 historical market data
- 檢查資料缺漏、重複和異常
- 用 Python 做 backtesting 和參數比較
- 比較 filter / regime / timeframe 的差異
- 檢查 transaction cost、drawdown、Monte Carlo、walk-forward
- 保留 failed results，不只挑好看的結果

## 這個 repo 不主張什麼

- 不提供投資建議
- 不代表任何策略可以直接實盤使用
- 不宣稱歷史績效可以重複
- 不把 full-sample 漂亮數字當成結論

## Research Cases

| Case | Data | Method | Main result | Limitation |
|---|---|---|---|---|
| ETHUSDT Hurst / HMM filter comparison | Bybit ETHUSDT perpetual，2024-05-26 to 2026-05-26 | Python backtest、Hurst filters、lightweight HMM proxy | 最佳 Hurst variant 在測試區間 return 24.65%，max drawdown -8.10% | 還需要更多市場和更長的樣本外驗證 |
| US100 data pipeline and stress test | Dukascopy USATECH.IDX/USD one-minute bars，2021-05-28 to 2026-05-27 | data-quality checks、70/30 split、cost stress、Monte Carlo、walk-forward | 8 個候選在 strict stress 下都未通過 | 比較適合作為淘汰流程，不是可交易結論 |
| XAUUSD robustness check | Dukascopy XAUUSD mid OHLC，2021-05-28 to 2026-05-28 | full-sample backtest、cost stress、Monte Carlo、walk-forward | full-sample 結果很強，但 walk-forward 不穩 | 是 overfitting risk 的例子 |

## Data Quality Example

US100 是目前資料流程比較完整的案例：

| Check | Result |
|---|---:|
| Total one-minute bars checked | 1,650,628 |
| Duplicate open times | 0 |
| Abnormal OHLC rows | 0 |
| Missing one-minute ratio | 37.23% |
| Gap segments | 1,452 |
| Parameter / stress combinations | 270 |

我把 missing-minute ratio 和 gap segments 留在 README 裡，是因為這些問題會影響我對結果的信任程度。只放 equity curve，不說資料品質問題，容易讓結果看起來比實際更可靠。

## 為什麼保留失敗結果

US100 的 8 個候選是從 training period 選出來的，但在更嚴格的 cost stress、Monte Carlo 和 walk-forward 檢查下都沒有通過。

這種結果看起來不像「成果」，但對我來說反而很重要：

- 它提醒我不能只相信訓練期績效
- 它能避免看到漂亮曲線就過度自信
- 它讓篩選和淘汰流程變得透明

## Repo Structure

```text
.
├── README.md                  # overview and research summary
├── CASE_STUDY.md              # detailed notes for each case
├── source-files.md            # data/artifact notes
├── index.html                 # static portfolio page
├── styles.css                 # page styling
├── assets/                    # exported charts
└── data/                      # selected CSV result tables
```

## Selected Artifacts

| Path | Description |
|---|---|
| `CASE_STUDY.md` | 三個案例的完整設定、結果和限制 |
| `data/summary.csv` | 三個案例的摘要表 |
| `data/eth-hurst-hmm-top30.csv` | ETHUSDT filter variants |
| `data/us100-walk-forward.csv` | US100 walk-forward sample |
| `data/xauusd-top-stability.csv` | XAUUSD stability-ranked candidates |
| `assets/eth-hurst-hmm-equity.svg` | ETHUSDT equity curve comparison |
| `assets/xauusd-cisd-equity.svg` | XAUUSD equity curve comparison |

## Next Improvements

- 加一個 clean CLI runner，讓每個 experiment 更容易重跑
- 把每個 experiment 的設定移到 config files
- 加 PnL、drawdown、fee accounting 的測試
- 把 raw data handling 和 report artifacts 分開
- 讓 charts 可以從 scripts 自動輸出

## Notes

這是一份 research / documentation portfolio。所有結果都是 historical tests，只能用來說明研究流程和資料驗證方法，不代表任何交易建議。
