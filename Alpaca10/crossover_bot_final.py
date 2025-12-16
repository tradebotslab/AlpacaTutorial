# crossover_bot_final.py
# Tutorial 10: Complete Moving Average Crossover Trading Bot
# This bot implements a Golden Cross / Death Cross strategy using 20-day and 50-day SMAs

# 1. Imports
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import config
import time
import pandas as pd
from datetime import datetime

# 2. Constants
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 1  # The number of shares to buy/sell per trade
SMA_SHORT_WINDOW = 20  # Short-term moving average period (days)
SMA_LONG_WINDOW = 50  # Long-term moving average period (days)
LOOP_SLEEP_MINUTES = 5  # How often the bot's main loop should run (in minutes)

# 3. API Connection
# We use paper trading by default to avoid risking real money during development
api = tradeapi.REST(
    config.API_KEY,
    config.SECRET_KEY,
    config.BASE_URL,
    api_version='v2'
)


# 4. Helper Functions
def check_current_position(symbol):
    """
    Check if we currently hold a position in the given symbol.
    
    Returns:
        tuple: (bool, Position or None) - True if position exists, False otherwise
    """
    try:
        position = api.get_position(symbol)
        return True, position
    except Exception:
        # API throws an error if a position does not exist
        return False, None


def fetch_historical_data(symbol, data_limit):
    """
    Fetch historical price data for the given symbol.
    
    Args:
        symbol: Stock symbol to fetch data for
        data_limit: Number of days of data to fetch
        
    Returns:
        pandas.DataFrame: DataFrame with OHLCV data
    """
    barset = api.get_bars(
        symbol,
        TimeFrame.Day,
        limit=data_limit,
        adjustment='raw'
    )
    return barset.df


def calculate_moving_averages(dataframe, short_window, long_window):
    """
    Calculate Simple Moving Averages for the given windows.
    
    Args:
        dataframe: DataFrame with price data
        short_window: Period for short-term SMA
        long_window: Period for long-term SMA
        
    Returns:
        pandas.DataFrame: DataFrame with added SMA columns
    """
    dataframe[f'sma_{short_window}'] = dataframe['close'].rolling(window=short_window).mean()
    dataframe[f'sma_{long_window}'] = dataframe['close'].rolling(window=long_window).mean()
    return dataframe


def detect_golden_cross(previous_day, current_day, short_window, long_window):
    """
    Detect a Golden Cross signal (bullish entry).
    
    A Golden Cross occurs when the short SMA crosses above the long SMA.
    This is a buy signal indicating potential upward momentum.
    
    Args:
        previous_day: Previous day's data row
        current_day: Current day's data row
        short_window: Short SMA window period
        long_window: Long SMA window period
        
    Returns:
        bool: True if Golden Cross detected, False otherwise
    """
    short_sma_prev = previous_day[f'sma_{short_window}']
    long_sma_prev = previous_day[f'sma_{long_window}']
    short_sma_curr = current_day[f'sma_{short_window}']
    long_sma_curr = current_day[f'sma_{long_window}']
    
    # Golden Cross: short SMA was below long SMA yesterday, but above today
    return (short_sma_prev < long_sma_prev) and (short_sma_curr > long_sma_curr)


def detect_death_cross(previous_day, current_day, short_window, long_window):
    """
    Detect a Death Cross signal (bearish exit).
    
    A Death Cross occurs when the short SMA crosses below the long SMA.
    This is a sell signal indicating potential downward momentum.
    
    Args:
        previous_day: Previous day's data row
        current_day: Current day's data row
        short_window: Short SMA window period
        long_window: Long SMA window period
        
    Returns:
        bool: True if Death Cross detected, False otherwise
    """
    short_sma_prev = previous_day[f'sma_{short_window}']
    long_sma_prev = previous_day[f'sma_{long_window}']
    short_sma_curr = current_day[f'sma_{short_window}']
    long_sma_curr = current_day[f'sma_{long_window}']
    
    # Death Cross: short SMA was above long SMA yesterday, but below today
    return (short_sma_prev > long_sma_prev) and (short_sma_curr < long_sma_curr)


def place_buy_order(symbol, quantity):
    """
    Place a market buy order for the given symbol and quantity.
    
    Args:
        symbol: Stock symbol to buy
        quantity: Number of shares to buy
    """
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='day'
        )
        print(f"✅ BUY order placed successfully for {quantity} share(s) of {symbol}.")
    except Exception as e:
        print(f"❌ Error placing BUY order: {e}")


def place_sell_order(symbol, quantity):
    """
    Place a market sell order for the given symbol and quantity.
    
    Args:
        symbol: Stock symbol to sell
        quantity: Number of shares to sell
    """
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"✅ SELL order placed successfully for {quantity} share(s) of {symbol}.")
    except Exception as e:
        print(f"❌ Error placing SELL order: {e}")


# 5. Main Logic
def run_trading_bot():
    """
    The main function for the trading bot.
    
    This function runs an infinite loop that:
    1. Checks current position status
    2. Fetches market data and calculates indicators
    3. Detects trading signals (Golden Cross / Death Cross)
    4. Places orders when signals are detected
    5. Waits before the next iteration
    """
    print("🚀 Trading Bot is starting...")
    print(f"📊 Trading symbol: {SYMBOL_TO_TRADE}")
    print(f"📈 SMA windows: {SMA_SHORT_WINDOW}-day / {SMA_LONG_WINDOW}-day")
    print(f"⏰ Loop interval: {LOOP_SLEEP_MINUTES} minutes")
    print("=" * 60)
    
    # Main Bot Loop
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # 1. Check Bot's State: Do we have a position?
            is_in_position, position = check_current_position(SYMBOL_TO_TRADE)
            if is_in_position:
                print(f"✅ Position exists: {position.qty} share(s) of {SYMBOL_TO_TRADE}.")
            else:
                print("ℹ️ No position currently held.")

            # 2. Market Analysis: Fetch data and calculate indicators
            # We need enough data for the longest SMA + 1 period for comparison
            data_limit = SMA_LONG_WINDOW + 1
            try:
                dataframe = fetch_historical_data(SYMBOL_TO_TRADE, data_limit)
                dataframe = calculate_moving_averages(dataframe, SMA_SHORT_WINDOW, SMA_LONG_WINDOW)
            except Exception as e:
                print(f"❌ Error fetching or processing market data: {e}")
                print("Continuing to next iteration...")
                time.sleep(60)
                continue

            # 3. Signal Detection: Compare the last two data points
            current_day = dataframe.iloc[-1]
            previous_day = dataframe.iloc[-2]

            # 4. Decision Logic & Action
            # Golden Cross (Bullish Entry Signal)
            if not is_in_position and detect_golden_cross(
                previous_day, current_day, SMA_SHORT_WINDOW, SMA_LONG_WINDOW
            ):
                print(f"📈 Golden Cross Detected! Placing BUY order for {QTY_PER_TRADE} share(s) of {SYMBOL_TO_TRADE}.")
                place_buy_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)

            # Death Cross (Bearish Exit Signal)
            elif is_in_position and detect_death_cross(
                previous_day, current_day, SMA_SHORT_WINDOW, SMA_LONG_WINDOW
            ):
                print(f"📉 Death Cross Detected! Placing SELL order for {QTY_PER_TRADE} share(s) of {SYMBOL_TO_TRADE}.")
                place_sell_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)

            else:
                print("Signal: No crossover. Holding current state.")

            # 5. Sleep until the next loop iteration
            sleep_seconds = LOOP_SLEEP_MINUTES * 60
            print(f"Action complete. Sleeping for {LOOP_SLEEP_MINUTES} minutes...")
            time.sleep(sleep_seconds)

        except KeyboardInterrupt:
            # Gracefully shut down the bot on Ctrl+C
            print("\n🛑 Bot is shutting down. Goodbye!")
            break
        except Exception as e:
            # Handle other potential errors (e.g., API connection issues)
            print(f"❌ An error occurred: {e}")
            print("Continuing...")
            time.sleep(60)


# 6. Run
if __name__ == '__main__':
    run_trading_bot()
