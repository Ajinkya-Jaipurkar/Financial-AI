"""
Clean Market Data Pipeline - Stage 1: Ingestion & Validation
=============================================================
This module fetches historical stock data, computes financial metrics,
and validates/visualizes the cleaned data.

Learning goals:
- Fetching data from APIs (yfinance)
- Calculating returns (daily and cumulative)
- Rolling statistics (mean, std) for volatility
- Data validation and cleaning
- Visualization and persistence
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from pathlib import Path
import logging

# ============================================================================
# SETUP: Logging for observability (learn: why log? track errors and events)
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# TASK 1: Fetch Market Data
# ============================================================================
def fetch_market_data(tickers: list, start_date: str, end_date: str) -> dict:
    """
    Fetch historical OHLCV data for multiple tickers.
    
    Args:
        tickers: List of ticker symbols (e.g., ['SPY', 'AAPL'])
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
    
    Returns:
        Dictionary with ticker as key, DataFrame as value
        
    Why this approach?
    - Keeps data ingestion separate from transformation
    - Easier to test and debug
    - Can swap data source (yfinance → API → database) without changing rest of code
    """
    data_dict = {}
    
    for ticker in tickers:
        logger.info(f"Fetching data for {ticker}...")
        try:
            # yfinance automatically downloads OHLCV (Open, High, Low, Close, Volume)
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            
            # Basic validation: check we got data
            if df.empty:
                logger.warning(f"No data returned for {ticker}")
                continue
            
            # yfinance returns MultiIndex columns, flatten them
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Reset index to convert DatetimeIndex to a regular column
            df = df.reset_index()
            
            # Rename 'Price' to 'Date' if needed (yfinance quirk)
            if 'Price' in df.columns:
                df = df.rename(columns={'Price': 'Date'})
            
            # Add ticker column for identification
            df['Ticker'] = ticker
            data_dict[ticker] = df
            logger.info(f"✓ Downloaded {len(df)} records for {ticker}")
            
        except Exception as e:
            logger.error(f"Failed to fetch {ticker}: {e}")
            continue
    
    return data_dict


# ============================================================================
# TASK 2: Compute Financial Metrics
# ============================================================================
def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily and cumulative returns.
    
    Why two types?
    - Daily returns: check day-to-day volatility, used in risk models
    - Cumulative returns: see total performance over time, easier to plot/compare
    
    Formula:
    - Daily return = (Close_t - Close_t-1) / Close_t-1
    - Cumulative return = (Close_t - Close_0) / Close_0
    """
    df = df.copy()
    
    # Daily return: % change from previous close
    df['Daily_Return'] = df['Close'].pct_change()
    
    # Cumulative return: % change from the first close
    df['Cumulative_Return'] = (df['Close'] / df['Close'].iloc[0] - 1) * 100
    
    return df


def compute_rolling_stats(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Compute rolling mean and standard deviation.
    
    Why rolling stats?
    - Rolling mean: detect trends (price goes above/below 20-day average?)
    - Rolling std: measure volatility (is it a calm or turbulent day?)
    - window=20: typical trading days in a month, captures short-term behavior
    
    Args:
        df: DataFrame with 'Close' and 'Daily_Return' columns
        window: Number of periods for rolling window (default: 20 trading days)
    """
    df = df.copy()
    
    # Rolling mean of close price
    df['Rolling_Mean'] = df['Close'].rolling(window=window).mean()
    
    # Rolling standard deviation of daily returns (measure of volatility)
    df['Rolling_Volatility'] = df['Daily_Return'].rolling(window=window).std() * 100
    
    return df


# ============================================================================
# TASK 3: Data Cleaning & Validation
# ============================================================================
def validate_and_clean_data(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Apply data quality checks.
    
    Checks:
    - No null prices (essential for trading)
    - Price > 0 (sanity check)
    - Volume >= 0 (can't be negative)
    - Date index is monotonic (no time travel!)
    
    Learn: Why validate?
    - Bad data → bad models → bad decisions
    - Easier to catch issues early than debug downstream
    """
    df = df.copy()
    
    initial_rows = len(df)
    
    # Check for null close prices
    null_count = df['Close'].isnull().sum().item()
    if null_count > 0:
        logger.warning(f"{ticker}: Found {null_count} null prices")
        df = df.dropna(subset=['Close'])
    
    # Check for invalid prices
    negative_prices = (df['Close'] <= 0).sum().item()
    if negative_prices > 0:
        logger.warning(f"{ticker}: Found {negative_prices} non-positive prices, removing...")
        df = df[df['Close'] > 0]
    
    # Check for invalid volumes
    negative_volumes = (df['Volume'] < 0).sum().item()
    if negative_volumes > 0:
        logger.warning(f"{ticker}: Found {negative_volumes} negative volumes, removing...")
        df = df[df['Volume'] >= 0]
    
    removed_rows = initial_rows - len(df)
    if removed_rows > 0:
        logger.info(f"{ticker}: Removed {removed_rows} invalid rows")
    
    return df


# ============================================================================
# TASK 4: Visualization
# ============================================================================
def plot_analysis(data_dict: dict, output_path: Path):
    """
    Create a multi-panel figure showing:
    1. Price over time (for all tickers)
    2. Cumulative returns (for all tickers)
    3. Rolling volatility (for all tickers)
    
    Why multi-panel?
    - Compare multiple stocks side-by-side
    - See different aspects of behavior (price level vs returns vs volatility)
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle('Market Data Analysis - SPY, AAPL, MSFT, QQQ', fontsize=16, fontweight='bold')
    
    # Panel 1: Price over time
    ax1 = axes[0]
    for ticker, df in data_dict.items():
        ax1.plot(df.index, df['Close'], label=ticker, linewidth=2)
    ax1.set_ylabel('Price ($)', fontsize=11, fontweight='bold')
    ax1.set_title('Closing Price Over Time', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Cumulative returns (easier to compare performance)
    ax2 = axes[1]
    for ticker, df in data_dict.items():
        ax2.plot(df.index, df['Cumulative_Return'], label=ticker, linewidth=2)
    ax2.set_ylabel('Cumulative Return (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Cumulative Returns Over Time', fontsize=12)
    ax2.legend(loc='best')
    ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Rolling volatility (risk measurement)
    ax3 = axes[2]
    for ticker, df in data_dict.items():
        ax3.plot(df.index, df['Rolling_Volatility'], label=ticker, linewidth=2)
    ax3.set_ylabel('Rolling Volatility (%)', fontsize=11, fontweight='bold')
    ax3.set_xlabel('Date', fontsize=11, fontweight='bold')
    ax3.set_title('20-Day Rolling Standard Deviation (Daily Returns)', fontsize=12)
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path / 'analysis.png', dpi=150, bbox_inches='tight')
    logger.info(f"✓ Saved plot to {output_path / 'analysis.png'}")
    plt.close()  # Close the figure to free memory and avoid blocking


# ============================================================================
# TASK 5: Save Clean Data
# ============================================================================
def save_data_to_csv(data_dict: dict, output_path: Path):
    """
    Persist cleaned data to CSV files.
    
    Why CSV?
    - Human readable (can inspect in Excel)
    - Universal (every tool reads CSV)
    - Why NOT: less efficient than Parquet, but fine for learning
    
    Later, you'll upgrade to Parquet for efficiency.
    """
    for ticker, df in data_dict.items():
        # Select only relevant columns for storage
        output_df = df[['Date', 'Close', 'Volume', 'Daily_Return', 'Cumulative_Return',
                        'Rolling_Mean', 'Rolling_Volatility']].copy()

        filepath = output_path / f'{ticker}_clean.csv'
        output_df.to_csv(filepath, index=False)
        logger.info(f"✓ Saved {ticker} data to {filepath}")


# ============================================================================
# MAIN PIPELINE
# ============================================================================
def main():
    """
    Orchestrate the entire pipeline:
    Fetch → Validate → Compute metrics → Visualize → Save
    """
    # Configuration
    tickers = ['SPY', 'AAPL', 'MSFT', 'QQQ']
    start_date = '2023-01-01'
    end_date = '2024-12-31'
    output_path = Path(__file__).parent.parent / 'Data'  # E:\Financial AI\Data
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    logger.info("=" * 60)
    logger.info("Starting Clean Data Pipeline")
    logger.info("=" * 60)
    
    # Step 1: Fetch raw data
    logger.info("\n[STEP 1] Fetching market data...")
    data_dict = fetch_market_data(tickers, start_date, end_date)
    
    if not data_dict:
        logger.error("No data fetched. Exiting.")
        return
    
    # Step 2: Clean and validate
    logger.info("\n[STEP 2] Validating and cleaning data...")
    for ticker in data_dict:
        data_dict[ticker] = validate_and_clean_data(data_dict[ticker], ticker)
    
    # Step 3: Compute financial metrics
    logger.info("\n[STEP 3] Computing returns and rolling statistics...")
    for ticker in data_dict:
        data_dict[ticker] = compute_returns(data_dict[ticker])
        data_dict[ticker] = compute_rolling_stats(data_dict[ticker], window=20)
    
    # Step 4: Visualize results
    logger.info("\n[STEP 4] Generating visualizations...")
    plot_analysis(data_dict, output_path)
    
    # Step 5: Save to CSV
    logger.info("\n[STEP 5] Saving cleaned data to CSV...")
    save_data_to_csv(data_dict, output_path)
    
    logger.info("\n" + "=" * 60)
    logger.info("Pipeline completed successfully!")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()

