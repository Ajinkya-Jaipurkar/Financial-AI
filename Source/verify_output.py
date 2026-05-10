"""Verification script - check the clean data output"""
import pandas as pd

# Display data from each ticker
for ticker in ['SPY', 'AAPL', 'MSFT', 'QQQ']:
    df = pd.read_csv(f'Data/{ticker}_clean.csv')
    print(f"\n{'='*70}")
    print(f"{ticker} Clean Data - Shape: {df.shape}")
    print(f"{'='*70}")
    print(df.head(10).to_string(index=False))
    print(f"\nBasic Statistics:")
    print(f"  Daily Return (mean): {df['Daily_Return'].mean():.6f}")
    print(f"  Daily Return (std):  {df['Daily_Return'].std():.6f}")
    print(f"  Cumulative Return:   {df['Cumulative_Return'].iloc[-1]:.2f}%")
    print(f"  Final Price:         ${df['Close'].iloc[-1]:.2f}")

