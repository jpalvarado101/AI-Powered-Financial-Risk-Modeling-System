import pandas as pd
import ta  # Technical Analysis Library

# Load data
df = pd.read_csv("data/stock_data.csv")

# Calculate moving averages
df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
df["SMA_200"] = ta.trend.sma_indicator(df["Close"], window=200)

# Compute Relative Strength Index (RSI)
df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

# Compute MACD
df["MACD"] = ta.trend.macd(df["Close"])

# Save processed data
df.to_csv("data/processed_data.csv", index=False)
