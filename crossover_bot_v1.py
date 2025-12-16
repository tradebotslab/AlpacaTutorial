# crossover_bot_v1.py
# Tutorial 9: Simple Exit Logic - Selling on a Reversal Signal
# This bot implements a complete moving average crossover strategy with entry and exit logic.

# 1. Imports
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import config
import time
import pandas as pd
from datetime import datetime

# 2. Constants
SYMBOL = "AAPL"
QTY_TO_TRADE = 1
SHORT_SMA_WINDOW = 20
LONG_SMA_WINDOW = 50
BARS_LIMIT = 51
SLEEP_INTERVAL_SECONDS = 300  # 5 minutes
ERROR_SLEEP_SECONDS = 60  # 1 minute on error

# 3. API Connection
# Using paper trading environment by default (configured in config.py)
api = tradeapi.REST(
    config.API_KEY,
    config.SECRET_KEY,
    base_url=config.BASE_URL,
    api_version='v2'
)

# 4. Helper functions
def check_position_exists(symbol):
    """
    Check if we currently own a position in the given symbol.
    
    Returns:
        tuple: (position_exists: bool, position_qty: int or None)
    """
    try:
        position = api.get_position(symbol)
        position_exists = True
        position_qty = position.qty
        return position_exists, position_qty
    except Exception:
        # get_position throws an exception if position does not exist
        position_exists = False
        position_qty = None
        return position_exists, position_qty


def fetch_historical_data(symbol, limit):
    """
    Fetch historical bar data for the given symbol.
    
    Args:
        symbol: Stock symbol to fetch data for
        limit: Number of bars to fetch
        
    Returns:
        pandas.DataFrame: DataFrame with OHLCV data
    """
    barset = api.get_bars(
        symbol,
        TimeFrame.Day,
        limit=limit,
        adjustment='raw'
    )
    dataframe = barset.df
    return dataframe


def calculate_moving_averages(dataframe, short_window, long_window):
    """
    Calculate short and long period moving averages.
    
    Args:
        dataframe: DataFrame with price data
        short_window: Period for short SMA
        long_window: Period for long SMA
        
    Returns:
        pandas.DataFrame: DataFrame with added SMA columns
    """
    dataframe['sma_short'] = dataframe['close'].rolling(window=short_window).mean()
    dataframe['sma_long'] = dataframe['close'].rolling(window=long_window).mean()
    return dataframe


def detect_golden_cross(previous_day, current_day):
    """
    Detect if a Golden Cross has occurred (short SMA crosses above long SMA).
    This is our entry signal indicating an uptrend.
    
    Args:
        previous_day: Series with previous day's data
        current_day: Series with current day's data
        
    Returns:
        bool: True if Golden Cross detected
    """
    short_was_below = previous_day['sma_short'] < previous_day['sma_long']
    short_is_above = current_day['sma_short'] > current_day['sma_long']
    golden_cross_detected = short_was_below and short_is_above
    return golden_cross_detected


def detect_death_cross(previous_day, current_day):
    """
    Detect if a Death Cross has occurred (short SMA crosses below long SMA).
    This is our exit signal indicating a downtrend.
    
    Args:
        previous_day: Series with previous day's data
        current_day: Series with current day's data
        
    Returns:
        bool: True if Death Cross detected
    """
    short_was_above = previous_day['sma_short'] > previous_day['sma_long']
    short_is_below = current_day['sma_short'] < current_day['sma_long']
    death_cross_detected = short_was_above and short_is_below
    return death_cross_detected


def place_buy_order(symbol, quantity):
    """
    Place a market buy order.
    
    Args:
        symbol: Stock symbol to buy
        quantity: Number of shares to buy
    """
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='day'
    )


def place_sell_order(symbol, quantity):
    """
    Place a market sell order.
    
    Args:
        symbol: Stock symbol to sell
        quantity: Number of shares to sell
    """
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='sell',
        type='market',
        time_in_force='day'
    )


# 5. Main logic
def run_bot():
    """
    Main bot loop that continuously checks for trading signals.
    The bot will:
    1. Check current position status
    2. Fetch market data and calculate indicators
    3. Execute trades based on Golden Cross (entry) or Death Cross (exit) signals
    """
    print("Bot is starting...")
    print(f"Trading symbol: {SYMBOL}")
    print(f"Using paper trading environment: {config.BASE_URL}")
    
    # Main Loop
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {current_time} ---")

            # 1. Check if we already have a position
            position_exists, position_qty = check_position_exists(SYMBOL)
            if position_exists:
                print(f"Position exists: {position_qty} shares of {SYMBOL}.")
            else:
                print("No position exists.")

            # 2. Fetch Data and Calculate SMAs
            dataframe = fetch_historical_data(SYMBOL, BARS_LIMIT)
            dataframe = calculate_moving_averages(
                dataframe,
                SHORT_SMA_WINDOW,
                LONG_SMA_WINDOW
            )

            current_day = dataframe.iloc[-1]
            previous_day = dataframe.iloc[-2]

            # 3. Implement Trading Logic
            # Golden Cross (Entry Condition)
            # Only buy if we don't have a position AND a Golden Cross just occurred
            golden_cross_detected = detect_golden_cross(previous_day, current_day)
            if not position_exists and golden_cross_detected:
                print("Golden Cross Detected! Placing BUY order.")
                place_buy_order(SYMBOL, QTY_TO_TRADE)

            # Death Cross (Exit Condition)
            # Only sell if we have a position AND a Death Cross just occurred
            elif position_exists:
                death_cross_detected = detect_death_cross(previous_day, current_day)
                if death_cross_detected:
                    print("Death Cross Detected! Placing SELL order.")
                    place_sell_order(SYMBOL, QTY_TO_TRADE)
                else:
                    print("No exit signal. Holding position.")
            else:
                print("No entry signal. Waiting.")

            # Sleep until the next interval
            print(f"Action complete. Sleeping for {SLEEP_INTERVAL_SECONDS // 60} minutes...")
            time.sleep(SLEEP_INTERVAL_SECONDS)

        except Exception as error:
            # Catch any errors to prevent bot from crashing
            print(f"An error occurred: {error}")
            print("Continuing after error sleep...")
            time.sleep(ERROR_SLEEP_SECONDS)


# 6. Run
if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        # Allow graceful shutdown with Ctrl+C
        print("\nBot is shutting down. Goodbye!")

