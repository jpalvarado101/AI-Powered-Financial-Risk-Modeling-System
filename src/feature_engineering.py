import pandas as pd
import ta  # Technical Analysis Library

# Load data
df = pd.read_csv("J:\John Alvarado\Documents\projects\AI-Powered Financial Risk Modeling System\AI-Powered-Financial-Risk-Modeling-System\data\stock_data.csv")

# If your CSV has extra rows (like "Ticker", "Date" as data), try adjusting skiprows:
# df = pd.read_csv("data/stock_data.csv", skiprows=1)

# Ensure numeric columns to avoid "No numeric types to aggregate" errors
for col in ["Open", "High", "Low", "Close", "Adj Close", "Volume"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Calculate moving averages
df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)
df["SMA_200"] = ta.trend.sma_indicator(df["Close"], window=200)

# Compute Relative Strength Index (RSI)
df["RSI"] = ta.momentum.rsi(df["Close"], window=14)

# Compute MACD
df["MACD"] = ta.trend.macd(df["Close"])

# Save processed data
df.to_csv("J:\John Alvarado\Documents\projects\AI-Powered Financial Risk Modeling System\AI-Powered-Financial-Risk-Modeling-System\data\processed_data.csv", index=False)
