import yfinance as yf
import pandas as pd
import requests
import io
import os

# Fetch stock data from Yahoo Finance
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.download(ticker, start=start_date, end=end_date)
    return stock

# Fetch macroeconomic data from Quandl
def fetch_macro_data(api_key):
    url = f"https://www.quandl.com/api/v3/datasets/FRED/GDP.csv?api_key={api_key}"
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df

if __name__ == "__main__":
    # Replace YOUR_QUANDL_API_KEY with your actual key.
    stock_data = fetch_stock_data("AAPL", "2020-03-01", "2025-01-01")
    macro_data = fetch_macro_data("YOUR_QUANDL_API_KEY")

    # Ensure the data folder exists
    data_folder = r""
    os.makedirs(data_folder, exist_ok=True)

    stock_csv = os.path.join(data_folder, "stock_data.csv")
    macro_csv = os.path.join(data_folder, "macro_data.csv")
    
    stock_data.to_csv(stock_csv)
    macro_data.to_csv(macro_csv)
    print("Data ingestion complete.")
