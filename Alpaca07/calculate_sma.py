# calculate_sma.py
# Tutorial 7: Calculating Simple Moving Average (SMA)

# 1. Imports
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
import config

# 2. Constants
SYMBOL = "AAPL"
DAYS_OF_HISTORY = 100
SHORT_SMA_WINDOW = 20
LONG_SMA_WINDOW = 50
NUMBER_OF_ROWS_TO_DISPLAY = 10

# 3. API Connection
# Using paper trading environment by default (defined in config.BASE_URL)
api = tradeapi.REST(
    config.API_KEY,
    config.SECRET_KEY,
    base_url=config.BASE_URL,
    api_version='v2'
)

# 4. Helper functions
def get_historical_data(symbol, days_of_history):
    """
    Fetches historical market data for a given symbol.
    
    Args:
        symbol: The stock symbol to fetch data for (e.g., "AAPL")
        days_of_history: Number of days of historical data to retrieve
    
    Returns:
        A pandas DataFrame containing the historical price data
    """
    # Calculate start and end dates
    # We use New York timezone because US markets operate in EST/EDT
    end_date = pd.Timestamp.now(tz='America/New_York').isoformat()
    start_date = (pd.Timestamp.now(tz='America/New_York') - pd.Timedelta(days=days_of_history)).isoformat()
    
    # Fetch bars from Alpaca API
    barset = api.get_bars(
        symbol,
        TimeFrame.Day,
        start=start_date,
        end=end_date,
        adjustment='raw'  # Use raw prices without adjustments
    )
    
    # Convert barset to DataFrame for easier manipulation
    historical_data_df = barset.df
    return historical_data_df


def calculate_sma(dataframe, closing_prices_column, window_size):
    """
    Calculates Simple Moving Average for a given window size.
    
    Args:
        dataframe: The pandas DataFrame containing price data
        closing_prices_column: Name of the column with closing prices (usually 'close')
        window_size: Number of periods to average (e.g., 20 for 20-day SMA)
    
    Returns:
        A pandas Series containing the SMA values
    """
    # .rolling(window=window_size) creates a rolling window of the specified size
    # For each row, it includes the current row and the previous (window_size-1) rows
    # .mean() calculates the average of all values in that window
    # This is the mathematical definition of Simple Moving Average
    sma_values = dataframe[closing_prices_column].rolling(window=window_size).mean()
    return sma_values


# 5. Main logic
def main():
    """
    Main function that orchestrates data fetching and SMA calculation.
    """
    try:
        # Fetch historical data
        # We need at least 100 days to properly calculate a 50-day SMA
        print(f"Fetching {DAYS_OF_HISTORY} days of historical data for {SYMBOL}...")
        price_dataframe = get_historical_data(SYMBOL, DAYS_OF_HISTORY)
        print(f"Successfully fetched {len(price_dataframe)} days of data for {SYMBOL}.\n")
        
        # Calculate Simple Moving Averages
        # Short-term SMA helps identify recent trend direction
        price_dataframe['sma_20'] = calculate_sma(price_dataframe, 'close', SHORT_SMA_WINDOW)
        
        # Long-term SMA helps identify the overall trend
        price_dataframe['sma_50'] = calculate_sma(price_dataframe, 'close', LONG_SMA_WINDOW)
        
        # Display results
        # Show the last N rows to see the most recent data with calculated SMAs
        print(f"--- Price data for {SYMBOL} with {SHORT_SMA_WINDOW}-day and {LONG_SMA_WINDOW}-day SMA ---")
        print(price_dataframe.tail(NUMBER_OF_ROWS_TO_DISPLAY))
        
        # Educational note about NaN values
        print(f"\nNote: The first {LONG_SMA_WINDOW-1} rows will have NaN (Not a Number) values")
        print(f"for the {LONG_SMA_WINDOW}-day SMA because there isn't enough historical data")
        print(f"to calculate the average yet.")
        
    except Exception as error:
        # All API calls must be in try-except blocks for reliability
        print(f"An error occurred: {error}")


# 6. Run
if __name__ == "__main__":
    main()

