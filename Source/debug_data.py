"""Debug the data structure from yfinance"""
import yfinance as yf

df = yf.download('SPY', start='2023-01-01', end='2024-12-31', progress=False)
print("DataFrame structure:")
print(f"Index: {df.index.name}")
print(f"Columns: {df.columns.tolist()}")
print(f"Index type: {type(df.index)}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nAfter reset_index():")
df_reset = df.reset_index()
print(df_reset.head())
print(f"Reset columns: {df_reset.columns.tolist()}")

