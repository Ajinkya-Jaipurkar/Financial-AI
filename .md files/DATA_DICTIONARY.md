# Data Dictionary - Cleaned Market Data

## File Format
- **Filename**: `{TICKER}_clean.csv`
- **Format**: Comma-separated values
- **Encoding**: UTF-8
- **Rows**: ~501 (2 years of trading days)
- **Columns**: 7

---

## Column Descriptions

### 1. **Date**
- **Type**: String (YYYY-MM-DD format)
- **Meaning**: Trading date
- **Example**: `2023-01-03`
- **Notes**: 
  - US market holidays excluded (no data for those days)
  - US market weekends excluded
  - Sorted in ascending order (oldest → newest)

### 2. **Close**
- **Type**: Float (decimal)
- **Meaning**: Closing price on that trading day in USD
- **Example**: `365.07208251953125`
- **Notes**:
  - Price at market close (4:00 PM ET)
  - Unadjusted for dividends/splits (raw price)
  - Always > 0 (validated)
  - Decimal precision varies (price depends on historical data source)

### 3. **Volume**
- **Type**: Integer
- **Meaning**: Total shares traded during the day
- **Example**: `74850700`
- **Notes**:
  - In number of shares (not dollars)
  - Higher volume = more trading activity/liquidity
  - Always >= 0 (validated)
  - Can use as a "confidence" signal (low volume = less reliable data)

### 4. **Daily_Return**
- **Type**: Float (decimal)
- **Meaning**: Percentage change in price from previous day
- **Formula**: `(Close_today - Close_yesterday) / Close_yesterday`
- **Example**: `0.0077201751246083195` = +0.77% gain that day
- **Notes**:
  - **NaN (empty) for first row** — no previous day to compare
  - Positive = price went up
  - Negative = price went down
  - Typical range: -10% to +10% on any given day
  - Multiply by 100 to get percentage: 0.00772 * 100 = 0.772%

### 5. **Cumulative_Return**
- **Type**: Float (decimal)
- **Meaning**: Total percentage gain/loss from the START of the period
- **Formula**: `(Close_today - Close_first) / Close_first * 100`
- **Example**: `0.772017512460832` = +0.77% above the starting price
- **Notes**:
  - **First row is always 0.0** (can't have return on first day)
  - Increases over time if stock is going up
  - Negative if stock has declined since start
  - Easier to compare performance: which ticker did best?
  - **Already in percentage** (no need to multiply by 100)
  - Shows **total 2-year performance** in the last row

### 6. **Rolling_Mean**
- **Type**: Float (decimal)
- **Meaning**: 20-day moving average of the closing price
- **Formula**: `Average of last 20 Close prices`
- **Example**: `374.4` = average Close over the past 20 trading days
- **Notes**:
  - **First 19 rows are NaN** (need 20 values to start)
  - Smooths out daily noise
  - Shows the TREND
    - If Close > Rolling_Mean: price is ABOVE trend (uptrend)
    - If Close < Rolling_Mean: price is BELOW trend (downtrend)
  - Investors often use this as a "support/resistance" level
  - Helps identify trend reversals

### 7. **Rolling_Volatility**
- **Type**: Float (decimal)
- **Meaning**: 20-day standard deviation of daily returns (annualized)
- **Formula**: `std(Daily_Returns[-20:]) * sqrt(252) * 100`
  - Takes past 20 daily returns
  - Calculates standard deviation
  - Annualizes it (252 trading days/year)
  - Converts to percentage
- **Example**: `12.5` = 12.5% annualized volatility
- **Notes**:
  - **First 19 rows are NaN** (need 20 values to start)
  - **Higher value = more volatile/risky**
  - Typical range: 10% - 40% (can spike during market crisis)
  - Used in risk management: "How risky is this stock today?"
  - Inverse relationship to daily volatility when markets are calm
  - Conversely, volatility spikes during market shocks (e.g., earnings, recession fears)

---

## Quick Data Quality Checks

### Expected Patterns
```
✓ Date column: Continuously increasing (no duplicates)
✓ Close column: Usually small percentage changes day-to-day
✓ Volume: Large numbers (millions to billions of shares)
✓ Daily_Return: Usually between -5% and +5%
✓ Cumulative_Return: Gradually increasing or decreasing
✓ Rolling_Mean: Smooth curve, lags behind actual Close
✓ Rolling_Volatility: Spiky but bounded (rarely > 50%)
```

### Red Flags (would indicate a problem)
```
✗ Prices going negative (should never happen)
✗ Duplicate dates
✗ Volume = 0 (usually means market was closed)
✗ Daily_Return > 50% (extreme, rare)
✗ Cumulative_Return decreasing (only if stock crashed)
```

---

## Usage Examples

### 1. Find the Best Performing Ticker
Look at the **Cumulative_Return** in the last row of each file.
```
SPY:  58.82% ← market average
AAPL: 45.32%
MSFT: 60.15%  ← best performer
QQQ:  72.10%  ← tech index (more volatile)
```

### 2. Identify Volatile vs Stable Days
Look at **Daily_Return** and **Rolling_Volatility**:
```
Low volatility day: Daily_Return close to 0.1-0.2%, Rolling_Volatility ~ 10%
High volatility day: Daily_Return jumps to ±3-5%, Rolling_Volatility ~ 25%
```

### 3. Identify Trend Direction
Compare **Close** vs **Rolling_Mean**:
```
Close > Rolling_Mean: Stock trending UP
Close < Rolling_Mean: Stock trending DOWN
Close = Rolling_Mean: Stock at equilibrium
```

### 4. Assess Risk
Look at **Rolling_Volatility**:
```
Rolling_Volatility 10-15%: Low risk (defensive stock)
Rolling_Volatility 15-25%: Moderate risk (most stocks)
Rolling_Volatility 25-50%: High risk (growth stocks, biotech)
```

---

## Reading the CSV in Python

```python
import pandas as pd

# Load the data
df = pd.read_csv('../Data/SPY_clean.csv')

# Basic info
print(df.shape)  # Number of rows and columns
print(df.dtypes)  # Data types
print(df.head())  # First 5 rows
print(df.tail())  # Last 5 rows

# Quick stats
print(df['Close'].describe())  # Mean, std, min, max
print(df['Daily_Return'].mean())  # Average daily return

# Filter data
recent = df[df['Date'] > '2024-01-01']  # Data after Jan 1, 2024
high_volume = df[df['Volume'] > 100000000]  # Days with 100M+ shares traded
```

---

## Important Notes for Analysis

1. **Survivorship Bias**: Data is only for tickers that still exist. Delisted companies are NOT included.

2. **Dividend & Split Adjustments**: Close prices are UNADJUSTED.
   - If a stock split 2:1, Close will drop by ~50% (but this is expected).
   - Dividends are NOT subtracted from Close (you see the full market data).

3. **Time Zones**: All times are market hours (US Eastern Time).

4. **Trading Halts**: If markets are halted (emergency, etc.), there's no data for that day.

5. **Limitations**:
   - This is **daily** data only (no intra-day / minute-level data).
   - No bid/ask spreads or order book data.
   - No news/sentiment data.

---

## Next Steps

1. **Load a CSV and explore**: Use pandas to read and analyze the data
2. **Create new visualizations**: Plot moving averages, volatility heatmaps, etc.
3. **Calculate new metrics**: Sharpe ratio, max drawdown, correlation between stocks
4. **Backtest a strategy**: "Buy when price > 20-day MA, sell when < 20-day MA"
5. **Compare time periods**: How does 2023 performance differ from 2024?

Good luck! 🚀

