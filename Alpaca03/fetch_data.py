# fetch_data.py
# Tutorial 3: Fetching Market Data – Your First Candlestick

# 1. Imports
import os
from datetime import datetime
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import config

# 2. Constants
# No additional constants needed - we'll use config for API keys

# 3. API Connection
# Instantiate a Stock Historical Data Client
client = StockHistoricalDataClient(api_key=config.API_KEY, secret_key=config.SECRET_KEY)


# 4. Helper functions
def fetch_stock_bars(client, symbol, start_date, end_date, timeframe=TimeFrame.Day):
    """
    Fetches historical OHLCV (Open, High, Low, Close, Volume) data for a given stock.
    
    Args:
        client: The initialized Alpaca StockHistoricalDataClient object
        symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
        start_date: Start date as datetime object
        end_date: End date as datetime object
        timeframe: TimeFrame enum (e.g., TimeFrame.Day, TimeFrame.Hour, TimeFrame.Minute)
    
    Returns:
        pandas DataFrame containing OHLCV data, or None if an error occurs
    """
    try:
        # Define the request parameters
        request_params = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=timeframe,
            start=start_date,
            end=end_date
        )
        
        # Fetch the data
        # The get_stock_bars() method returns a dictionary, with the symbol as the key
        # and a list of bar objects as the value. We can access the dataframe with .df
        bars = client.get_stock_bars(request_params)
        bars_df = bars.df
        
        return bars_df
    except Exception as error:
        print(f"Error fetching stock data: {error}")
        return None


def display_candlestick_data(bars_df, symbol):
    """
    Displays the fetched candlestick data in a formatted way.
    
    Args:
        bars_df: pandas DataFrame containing OHLCV data
        symbol: Stock ticker symbol for display purposes
    """
    if bars_df is None or bars_df.empty:
        print(f"No data available for {symbol}")
        return
    
    print(f"\n{'='*70}")
    print(f"HISTORICAL CANDLESTICK DATA FOR {symbol}")
    print(f"{'='*70}")
    print(bars_df)
    print(f"\n{'='*70}")
    print(f"Total bars retrieved: {len(bars_df)}")
    print(f"{'='*70}\n")


def display_candlestick_summary(bars_df, symbol):
    """
    Displays a summary of the candlestick data including key statistics.
    
    Args:
        bars_df: pandas DataFrame containing OHLCV data
        symbol: Stock ticker symbol for display purposes
    """
    if bars_df is None or bars_df.empty:
        return
    
    # Handle MultiIndex (when fetching multiple symbols) or regular index
    if isinstance(bars_df.index, pd.MultiIndex):
        # MultiIndex has 'symbol' and 'timestamp' levels
        timestamps = bars_df.index.get_level_values('timestamp')
        close_prices = bars_df['close']
    else:
        # Regular index (single symbol, timestamp as index)
        timestamps = bars_df.index
        close_prices = bars_df['close']
    
    print(f"\n{'='*70}")
    print(f"SUMMARY STATISTICS FOR {symbol}")
    print(f"{'='*70}")
    print(f"Date Range: {timestamps.min()} to {timestamps.max()}")
    print(f"Highest Price: ${bars_df['high'].max():.2f}")
    print(f"Lowest Price: ${bars_df['low'].min():.2f}")
    print(f"First Close: ${close_prices.iloc[0]:.2f}")
    print(f"Last Close: ${close_prices.iloc[-1]:.2f}")
    print(f"Average Volume: {bars_df['volume'].mean():,.0f} shares")
    print(f"{'='*70}\n")


# 5. Main logic
def main():
    """
    Main function that orchestrates fetching and displaying historical stock data.
    This demonstrates how to retrieve OHLCV candlestick data from Alpaca.
    """
    print("Fetching historical market data from Alpaca API...")
    
    # Define the parameters for our data request
    symbol = "AAPL"  # Apple Inc.
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 10)
    timeframe = TimeFrame.Day  # Daily candlesticks
    
    # Fetch the data
    bars_df = fetch_stock_bars(client, symbol, start_date, end_date, timeframe)
    
    # Display the data if we successfully retrieved it
    if bars_df is not None and not bars_df.empty:
        display_candlestick_data(bars_df, symbol)
        display_candlestick_summary(bars_df, symbol)
        print("Successfully fetched historical data! Each row represents one candlestick.")
        print("\nKey columns explained:")
        print("  - open: Price at the beginning of the period")
        print("  - high: Highest price during the period")
        print("  - low: Lowest price during the period")
        print("  - close: Price at the end of the period")
        print("  - volume: Total shares traded during the period")
        print("  - vwap: Volume-Weighted Average Price")
    else:
        print("Failed to fetch data. Please check your API keys in config.py and your internet connection.")


# 6. Run
if __name__ == "__main__":
    main()

