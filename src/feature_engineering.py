import os
import pandas as pd
import ta  # Technical Analysis Library

# Ensure the "data" folder exists
data_folder = r""
os.makedirs(data_folder, exist_ok=True)

# Load stock data.
# Skip extra header rows (assumed to be at row indices 1 and 2).
stock_csv = os.path.join(data_folder, "stock_data.csv")
try:
    df = pd.read_csv(stock_csv, skiprows=[1, 2])
except FileNotFoundError:
    raise Exception("File 'stock_data.csv' not found. Run data_ingestion.py first.")

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Convert expected numeric columns to numeric types.
numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate technical indicators only if "Close" exists.
if "Close" in df.columns:
    df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
    df["SMA_200"] = ta.trend.sma_indicator(df["Close"], window=200)
    df["RSI"] = ta.momentum.rsi(df["Close"], window=14)
    df["MACD"] = ta.trend.macd(df["Close"])
else:
    raise Exception("Column 'Close' not found in the dataset. Please check your CSV file.")

# Save the processed data.
processed_csv = os.path.join(data_folder, "processed_data.csv")
df.to_csv(processed_csv, index=False)
print(f"Feature engineering complete. Processed data saved as '{processed_csv}'.")
