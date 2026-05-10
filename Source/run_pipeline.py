"""
Quick Runner - Experiment with Different Parameters
=====================================================
Use this to try different tickers, date ranges, rolling windows, etc.
"""

from Source.data_pull import (
    fetch_market_data, validate_and_clean_data, compute_returns,
    compute_rolling_stats, plot_analysis, save_data_to_csv
)
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION - Modify these to experiment!
# ============================================================================

# Tickers to analyze
TICKERS = ['SPY', 'AAPL', 'MSFT', 'QQQ']  # Try: ['TSLA', 'NVDA', 'AMD']

# Date range
START_DATE = '2023-01-01'
END_DATE = '2024-12-31'

# Rolling window (in trading days)
ROLLING_WINDOW = 20  # Try: 5, 10, 20, 50

# Output directory
OUTPUT_PATH = Path(__file__).parent / 'Data'

# ============================================================================
# RUN
# ============================================================================

if __name__ == '__main__':
    logger.info(f"Configuration:")
    logger.info(f"  Tickers: {TICKERS}")
    logger.info(f"  Date Range: {START_DATE} to {END_DATE}")
    logger.info(f"  Rolling Window: {ROLLING_WINDOW} days")
    logger.info(f"  Output: {OUTPUT_PATH}")
    logger.info("")

    # Fetch
    logger.info("Fetching market data...")
    data_dict = fetch_market_data(TICKERS, START_DATE, END_DATE)

    if not data_dict:
        logger.error("No data fetched!")
        exit(1)

    # Validate
    logger.info("Validating data...")
    for ticker in data_dict:
        data_dict[ticker] = validate_and_clean_data(data_dict[ticker], ticker)

    # Compute
    logger.info("Computing metrics...")
    for ticker in data_dict:
        data_dict[ticker] = compute_returns(data_dict[ticker])
        data_dict[ticker] = compute_rolling_stats(data_dict[ticker], window=ROLLING_WINDOW)

    # Visualize
    logger.info("Creating visualization...")
    plot_analysis(data_dict, OUTPUT_PATH)

    # Save
    logger.info("Saving data...")
    save_data_to_csv(data_dict, OUTPUT_PATH)

    logger.info("\n✅ Done! Check 'Data/' folder for outputs.")

# ============================================================================
# EXPERIMENT IDEAS
# ============================================================================
# 1. Try different tickers:
#    TICKERS = ['GOOG', 'AMZN', 'META', 'NFLX']
#
# 2. Try different windows:
#    ROLLING_WINDOW = 5   # Very short-term volatility
#    ROLLING_WINDOW = 50  # Longer-term trend
#
# 3. Try different date ranges:
#    START_DATE = '2020-01-01'  # Include COVID crash
#    START_DATE = '2024-01-01'  # Just recent data
#
# 4. What you'll observe:
#    - Longer windows = smoother trends, less noise
#    - Shorter windows = more volatile, catch quick changes
#    - Tech stocks (AAPL, MSFT) often more volatile than SPY
#    - SPY = market average volatility

