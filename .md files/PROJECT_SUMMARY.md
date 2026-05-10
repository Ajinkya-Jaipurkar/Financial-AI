# Market Data Pipeline - Project Summary

## ✅ Completed Tasks

### 1. **Data Fetching** (yfinance)
- Downloaded 4 years of historical data (2023-2024) for: **SPY, AAPL, MSFT, QQQ**
- Each ticker: ~501 trading days of OHLCV data
- Handled yfinance's MultiIndex structure correctly

### 2. **Data Validation & Cleaning**
- ✓ Removed null prices
- ✓ Validated positive prices
- ✓ Validated non-negative volumes
- ✓ Result: 0 invalid records (data quality was excellent)

### 3. **Financial Metrics Computed**
- **Daily Return**: `(Close_t - Close_t-1) / Close_t-1`
  - Shows day-to-day % change
  - Used in volatility calculations
  
- **Cumulative Return**: `(Close_t - Close_0) / Close_0 * 100`
  - Shows total performance from start date
  - Easier to compare across tickers
  
- **Rolling Mean**: 20-day moving average of Close price
  - First 19 rows are NaN (need 20 data points)
  
- **Rolling Volatility**: 20-day std dev of daily returns, annualized
  - Measure of risk/volatility
  - Also NaN for first 19 rows

### 4. **Visualization**
**Single figure with 3 panels:**
- **Panel 1**: Closing prices over time (all 4 tickers)
- **Panel 2**: Cumulative returns (% gain from start)
- **Panel 3**: 20-day rolling volatility (annualized std of daily returns)
- Saved to: `Data/analysis.png`

### 5. **Data Persistence**
**Clean CSV files created:**
- `Data/SPY_clean.csv`
- `Data/AAPL_clean.csv`
- `Data/MSFT_clean.csv`
- `Data/QQQ_clean.csv`

Each file contains:
- Date | Close | Volume | Daily_Return | Cumulative_Return | Rolling_Mean | Rolling_Volatility

---

## 📊 Sample Data Insights

### SPY (from the CSV):
```
Date: 2023-01-03 to 2024-12-31 (501 rows)
Close Price Range: $365.07 - $585+
Cumulative Return (2-year): ~50%+
Daily Returns (mean): ~0.10%, std: ~0.80%
```

---

## 🎓 Key Learning Concepts Implemented

### 1. **Pipeline Architecture**
```
Fetch Raw → Validate → Compute Metrics → Visualize → Persist
```
Each step is **modular** and **reusable** — you can swap out data sources, add new metrics, or change visualization without breaking other parts.

### 2. **Data Quality** 
- Always validate EARLY (at ingestion)
- Define clear validation rules (price > 0, volume >= 0, no nulls)
- Log what you remove so you can audit later

### 3. **Why Multiple Calculations?**
- **Daily Returns**: Needed for risk models, volatility calculations
- **Cumulative Returns**: For high-level performance comparisons
- **Rolling Stats**: Track trends (is the market calm or volatile today?)

### 4. **Timestamps Matter**
- Store dates explicitly (not just indices)
- Use DatetimeIndex for fast time-series operations
- Multiple rows per day possible in real tick data (here we have daily bars)

### 5. **Reproducibility**
- All transformations are deterministic (same input → same output)
- Code is version-controlled (git-friendly format)
- Data is immutable once written to CSV

---

## 🚀 What You Can Extend

1. **Add More Tickers**: Just add to the `tickers` list
2. **Different Date Ranges**: Modify `start_date` and `end_date`
3. **New Metrics**:
   - Bollinger Bands (moving mean ± n*std)
   - RSI (Relative Strength Index)
   - MACD (Moving Average Convergence Divergence)
4. **Different Aggregations**:
   - Weekly or monthly instead of daily
   - Hourly if you had tick data
5. **Statistical Impact**:
   - Correlation between tickers
   - Risk-adjusted returns (Sharpe ratio)
   - Backtesting simple strategies

---

## 🔍 Code Structure (data_pull.py)

**Functions organized by step:**

1. `fetch_market_data()` — Downloads from yfinance
2. `validate_and_clean_data()` — Data quality checks
3. `compute_returns()` — Daily + cumulative returns
4. `compute_rolling_stats()` — Moving average + volatility
5. `plot_analysis()` — Matplotlib visualization
6. `save_data_to_csv()` — Persistence to CSV
7. `main()` — Orchestrates the entire pipeline

Each function has:
- **Docstring** explaining what/why
- **Type hints** for clarity
- **Comments** in the code for learning
- **Logging** for observability

---

## 💡 Next Steps for Your Summer Project

**Phase 1 (Week 1-2)**: ✅ YOU ARE HERE
- Understand how the pipeline works
- Read through all the comments
- Modify `tickers`, dates, and window sizes
- Regenerate CSVs and plots

**Phase 2 (Week 3-4)**: Add Your Own Features
- Implement a new metric (e.g., Sharpe ratio)
- Add correlation analysis between tickers
- Create a summary statistics report

**Phase 3 (Week 5-6)**: Real-Time/Streaming Ideas
- Instead of downloading all at once, simulate receiving 1 day at a time
- Understand the concepts of **state** (rolling window) and **incremental updates**

**Phase 4 (Week 7-8)**: Refinement
- Add error handling (what if API fails?)
- Create a config file for parameters
- Write tests for your validation logic
- Document your schema

---

## 🛠️ Technologies Used

- **yfinance**: Download market data from Yahoo Finance
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Create visualizations
- **logging**: Track what the code is doing

---

## 📝 Questions to Ask Yourself (for deeper learning)

1. Why do we need BOTH daily returns and cumulative returns?
2. What would happen if you changed `window=20` to `window=5` or `window=50`?
3. Why are the first 19 rolling statistics NaN?
4. How would you handle stock splits or dividends adjustments?
5. What if data arrives out-of-order (tick data from a real exchange)?
6. How would you validate that the CSV saved correctly without reading it back?

---

## 🎯 Success Checklist

- ✅ Code runs without errors
- ✅ All 4 CSV files created in `Data/` folder
- ✅ `analysis.png` plot generated
- ✅ Data is validated (no neg prices, no nulls)
- ✅ Returns calculated correctly
- ✅ Rolling statistics computed
- ✅ Each function is modular and documented
- ✅ Logging shows what's happening at each step

---

Good luck with your summer project! 🚀

