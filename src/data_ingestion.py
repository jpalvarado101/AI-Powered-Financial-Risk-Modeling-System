import yfinance as yf
import pandas as pd
import requests
import io

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.download(ticker, start=start_date, end=end_date)
    return stock

# Fetch macroeconomic data from Quandl
def fetch_macro_data(api_key):
    url = f"https://www.quandl.com/api/v3/datasets/FRED/GDP.csv?api_key={api_key}"
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))  # Corrected line
    return df

if __name__ == "__main__":
    stock_data = fetch_stock_data("AAPL", "2020-01-01", "2025-01-01")
    macro_data = fetch_macro_data("YOUR_QUANDL_API_KEY")

    stock_data.to_csv("J:\John Alvarado\Documents\projects\AI-Powered Financial Risk Modeling System\AI-Powered-Financial-Risk-Modeling-System\data\stock_data.csv")
    macro_data.to_csv("J:\John Alvarado\Documents\projects\AI-Powered Financial Risk Modeling System\AI-Powered-Financial-Risk-Modeling-System\data\macro_data.csv")