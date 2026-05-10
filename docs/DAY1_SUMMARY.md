# Day 1 - Market Data Pipeline Learning Project

## 📌 What We Built
A **complete, production-ready market data pipeline** that fetches, validates, processes, visualizes, and persists clean financial data.

---

## ✅ Tasks Completed

| Task | Status | Output |
|------|--------|--------|
| Pull SPY, AAPL, MSFT, QQQ data | ✅ | 501 rows × ticker from yfinance |
| Compute daily returns | ✅ | Daily % change calculated |
| Compute cumulative returns | ✅ | Total % gain from start |
| Compute rolling mean (20-day) | ✅ | Moving average price |
| Compute rolling volatility (20-day) | ✅ | Annualized std of returns |
| Plot 3-panel visualization | ✅ | `Data/analysis.png` |
| Save clean data to CSV | ✅ | 4 files in `Data/` folder |

---

## 📁 Files Created

**Pipeline Code:**
- `Source/data_pull.py` — Main module (305 lines, fully commented)

**Documentation:**
- `README.md` — Full project guide
- `PROJECT_SUMMARY.md` — Learning outcomes
- `DATA_DICTIONARY.md` — Column reference
- `run_pipeline.py` — Parameter experimentation script

**Data Outputs:**
- `Data/SPY_clean.csv` — 502 rows, 7 columns
- `Data/AAPL_clean.csv`
- `Data/MSFT_clean.csv`
- `Data/QQQ_clean.csv`
- `Data/analysis.png` — 3-panel plot

---

## 🔧 Pipeline Architecture

```
Fetch (yfinance) 
    → Validate (nulls, prices > 0, volumes >= 0) 
    → Compute Metrics (returns, rolling stats) 
    → Visualize (3 subplots) 
    → Persist (CSV export)
```

**Key Features:**
- Modular design (5 functions)
- Type hints & docstrings
- Logging at each step
- Error handling
- Data quality checks

---

## 📊 Data Generated

**Each CSV contains:**
- `Date` — Trading date (YYYY-MM-DD)
- `Close` — Closing price ($)
- `Volume` — Shares traded
- `Daily_Return` — % change vs previous day
- `Cumulative_Return` — Total % gain from start
- `Rolling_Mean` — 20-day moving average
- `Rolling_Volatility` — Annualized std (%)

**Example (SPY):**
```
Date: 2023-01-03 to 2024-12-31 (501 trading days)
Start Price: $365.07
End Price: $585+
Cumulative Return: ~58.82%
Volatility Range: 10-25%
```

---

## 🎓 Key Concepts Learned

1. **Data Pipeline Design** — Separate concerns (fetch/validate/compute/visualize/persist)
2. **Data Validation** — Check quality early (nulls, ranges, consistency)
3. **Financial Metrics** — Returns, moving averages, volatility
4. **Clean Code** — Modular functions, type hints, logging
5. **Data Persistence** — CSV export, reproducibility
6. **Observability** — Logging shows what's happening at each step

---

## 🚀 How to Run

```bash
cd "E:\Financial AI"
python Source/data_pull.py          # Full pipeline
python run_pipeline.py               # Experiment with parameters
```

---

## 💡 Next Steps

1. **Read the code** — Study comments in `Source/data_pull.py`
2. **Experiment** — Change tickers, dates, rolling window in `run_pipeline.py`
3. **Extend** — Add new metrics (Sharpe ratio, correlation, RSI)
4. **Analyze** — Load CSVs, create custom visualizations
5. **Backtest** — Implement a simple trading strategy

---

## ✨ Key Takeaways

- ✅ Built a real, working data pipeline
- ✅ Understand all components (fetch → validate → compute → visualize → save)
- ✅ Clean, maintainable code with proper documentation
- ✅ 7 columns of meaningful financial data per ticker
- ✅ Ready to extend with new features

**Status: ✅ COMPLETE & WORKING**

---

*Day 1 Complete | May 10, 2026 | Ready for Day 2* 🚀

