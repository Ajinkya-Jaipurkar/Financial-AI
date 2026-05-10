# Market Data Pipeline - Your Summer Project

A complete, production-ready market data pipeline built **for learning**. Download, validate, compute metrics, visualize, and persist clean financial data.

---

## 📁 Project Structure

```
Financial AI/
├── Source/
│   └── data_pull.py              ← Main pipeline code (STUDY THIS!)
├── Data/
│   ├── SPY_clean.csv             ← Cleaned data outputs
│   ├── AAPL_clean.csv
│   ├── MSFT_clean.csv
│   ├── QQQ_clean.csv
│   └── analysis.png              ← Visualization
├── run_pipeline.py               ← Quick runner script
├── PROJECT_SUMMARY.md            ← What you accomplished
├── DATA_DICTIONARY.md            ← Column explanations
└── README.md                      ← This file
```

---

## 🚀 Quick Start

### Run the Pipeline
```bash
cd "E:\Financial AI"
python Source/data_pull.py
```

Output:
- 4 CSV files in `Data/` folder
- 1 PNG visualization (`analysis.png`)
- Console logs showing each step

### Experiment with Parameters
```bash
python run_pipeline.py  # Edit TICKERS, START_DATE, ROLLING_WINDOW at top
```

---

## 🎓 What You Built

### **Tasks Completed:**
✅ Pull data for SPY, AAPL, MSFT, QQQ using yfinance  
✅ Compute daily returns and cumulative returns  
✅ Compute rolling mean (20-day moving average)  
✅ Compute rolling volatility (20-day rolling std)  
✅ Plot all metrics in one figure (3 panels)  
✅ Save clean data to CSV files in `Data/` folder  

### **Data Quality:**
- ✅ Removed null prices
- ✅ Validated positive prices
- ✅ Validated non-negative volumes
- ✅ Proper date handling
- ✅ Clean CSV export

---

## 📊 Understanding the Pipeline

### Step-by-Step Flow

1. **Fetch** (yfinance)
   - Downloads 2 years of OHLCV data
   - Handles API errors gracefully
   - Logs download status

2. **Validate**
   - Checks for null/invalid values
   - Ensures price > 0, volume >= 0
   - Logs what was removed

3. **Compute**
   - Daily Return: `(Close_t - Close_t-1) / Close_t-1`
   - Cumulative Return: `(Close_t - Close_0) / Close_0 * 100`
   - Rolling Mean: 20-day average
   - Rolling Volatility: 20-day std of daily returns

4. **Visualize**
   - 3 subplots in one figure
   - Panel 1: Price over time
   - Panel 2: Cumulative returns
   - Panel 3: Rolling volatility

5. **Persist**
   - Save 4 CSV files (one per ticker)
   - Each with 501 rows × 7 columns

---

## 📖 Learning Resources in This Project

### **Code Organization** (`Source/data_pull.py`)
Each function is **modular** and has:
- Clear purpose
- Type hints for parameters
- Detailed docstring explaining WHY
- In-code comments for HOW
- Logging for observability

### **Key Code Sections to Study**

1. **Fetching**: `fetch_market_data()` — handles yfinance MultiIndex
2. **Validation**: `validate_and_clean_data()` — data quality checks
3. **Metrics**: `compute_returns()`, `compute_rolling_stats()` — financial formulas
4. **Visualization**: `plot_analysis()` — matplotlib best practices
5. **Persistence**: `save_data_to_csv()` — clean CSV export
6. **Orchestration**: `main()` — tying it all together

---

## 🔍 Understanding Your Data

### Column Reference
| Column | Type | Meaning | Notes |
|--------|------|---------|-------|
| Date | String | Trading date (YYYY-MM-DD) | Sorted ascending |
| Close | Float | Closing price in USD | Always > 0 |
| Volume | Integer | Shares traded | Always >= 0 |
| Daily_Return | Float | % change from yesterday | NaN on first row |
| Cumulative_Return | Float | % change from start | In percentage |
| Rolling_Mean | Float | 20-day moving average | NaN for first 19 rows |
| Rolling_Volatility | Float | 20-day annualized std | NaN for first 19 rows |

**See `DATA_DICTIONARY.md` for detailed explanations and examples.**

---

## 💡 How to Extend & Learn

### Easy Extensions (Try These!)
1. **Add more tickers**: `TICKERS = ['TSLA', 'NVDA', 'AMD']`
2. **Change date range**: `START_DATE = '2020-01-01'`
3. **Different rolling window**: `ROLLING_WINDOW = 50` (smoother) or `5` (noisier)
4. **Add a new metric**:
   ```python
   df['SMA_50'] = df['Close'].rolling(50).mean()  # 50-day average
   ```

### Medium Extensions
5. **Calculate Sharpe Ratio**: `daily_return_mean / daily_return_std * sqrt(252)`
6. **Find correlation**: Compare daily returns between tickers
7. **Identify support/resistance**: Where does price bounce off rolling mean?
8. **Custom visualization**: Box plot of returns by ticker

### Advanced Ideas (for later)
9. **Detect outliers**: Days with unusual volume or returns
10. **Backtest a strategy**: "Buy if Close > Rolling_Mean"
11. **Real-time streaming**: Simulate receiving data one day at a time
12. **Parquet output**: More efficient storage than CSV

---

## 🧪 Testing Your Understanding

### Questions to Answer:
1. Why do we have BOTH Daily_Return and Cumulative_Return?
2. What happens if you change `window=20` to `window=5`? Why?
3. Why are the first 19 rolling stats NaN?
4. Which ticker had the highest cumulative return?
5. Which ticker had the most volatility?

### Try It:

```python
import pandas as pd

df = pd.read_csv('../Data/SPY_clean.csv')

# What's the average daily return?
print(df['Daily_Return'].mean())

# Which day had the biggest move?
print(df.loc[df['Daily_Return'].abs().idxmax()])

# What's the final cumulative return?
print(df['Cumulative_Return'].iloc[-1])
```

---

## 🛠️ Technologies Used

- **yfinance**: Free market data from Yahoo Finance
- **pandas**: Data manipulation, analysis
- **numpy**: Numerical operations
- **matplotlib**: Static visualizations
- **logging**: Observability and debugging

All packages are in `requirements.txt`.

---

## 📋 Repository Contents

| File | Purpose |
|------|---------|
| `Source/data_pull.py` | Main pipeline — READ THIS FIRST |
| `run_pipeline.py` | Quick runner with parameters to modify |
| `PROJECT_SUMMARY.md` | What you built and learned |
| `DATA_DICTIONARY.md` | Detailed column reference |
| `requirements.txt` | Python dependencies |
| `Data/SPY_clean.csv` | Cleaned market data (example) |
| `Data/analysis.png` | Generated visualization |

---

## 🎯 Success Criteria

Your project is complete when:
- ✅ You can run `python Source/data_pull.py` without errors
- ✅ All 4 CSV files exist in `Data/` with ~501 rows each
- ✅ `analysis.png` is generated in `Data/`
- ✅ You understand what each column means
- ✅ You can modify and re-run with different parameters
- ✅ You can read and explain the code

---

## 🚨 Common Issues & Fixes

### Issue: "yfinance module not found"
```bash
pip install yfinance
```

### Issue: "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install -r requirements.txt
```

### Issue: No data returned for a ticker
- Check ticker is valid (e.g., not delisted)
- Check date range (avoid future dates)
- Check internet connection

### Issue: CSV file looks weird
- Re-run the pipeline: it regenerates files
- Check with: `python -c "import pandas as pd; print(pd.read_csv('Data/SPY_clean.csv').head())"`

---

## 📝 Next Steps

### This Week
- Run the pipeline successfully
- Read through `PROJECT_SUMMARY.md` and `DATA_DICTIONARY.md`
- Study the code comments in `Source/data_pull.py`

### Next Week
- Modify parameters and re-run with different tickers/dates
- Add 1-2 new metrics
- Create custom visualizations

### End of Summer
- Write a report on what you learned
- Implement a basic strategy backtest
- Present findings to mentors/peers

---

## 📚 Further Learning

**Market Data Concepts:**
- [Yahoo Finance Data Documentation](https://finance.yahoo.com/)
- [Pandas Time Series Docs](https://pandas.pydata.org/docs/user_guide/timeseries.html)

**Python Skills:**
- Logging best practices
- Function design and documentation
- Error handling (try/except)
- Data pipeline architecture

**Finance Concepts:**
- What are returns, volatility, rolling averages?
- Why these metrics matter for investing
- How traders use technical analysis

---

## 💬 Questions?

Look for answers in:
1. **Comments in `data_pull.py`** — Most concepts explained
2. **`DATA_DICTIONARY.md`** — Column meanings and examples
3. **`PROJECT_SUMMARY.md`** — High-level overview
4. **Code docstrings** — Learn by reading the code

---

## 🎓 Learning Outcomes

After this project, you'll understand:

✓ How to build an **end-to-end data pipeline**  
✓ **Data validation** and quality checks  
✓ **Financial metrics** (returns, volatility, moving averages)  
✓ **Modular code design** (separate, testable functions)  
✓ **Logging and observability** (track what's happening)  
✓ **Data persistence** (CSV storage)  
✓ **Reproducibility** (deterministic, version-controlled pipelines)  

These skills apply **far beyond finance** — to any data-driven project!

---

## 🚀 Good Luck with Your Summer Project!

You've built something real. Understand it. Extend it. Own it.

The best learning happens when you modify the code, break it, understand why, and fix it. **Experiment fearlessly!**

---

*Last Updated: May 10, 2026*

