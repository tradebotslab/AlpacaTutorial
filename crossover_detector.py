# crossover_detector.py
# Tutorial 8: Simple Entry Logic – Detecting a Moving Average Crossover

# 1. Imports
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
import config

# 2. Constants
SYMBOL = "AAPL"
SHORT_SMA_WINDOW = 20
LONG_SMA_WINDOW = 50
# We need 51 bars to have two full values for the 50-day SMA to compare
DATA_LIMIT = 51

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL, api_version='v2')

# 4. Helper functions
def get_historical_data(symbol, limit):
    """
    Fetches historical price data from Alpaca API.
    We need enough data points to calculate both SMAs and have previous values for comparison.
    """
    barset = api.get_bars(
        symbol,
        TimeFrame.Day,
        limit=limit,
        adjustment='raw'
    )
    return barset.df

def calculate_smas(dataframe, short_window, long_window):
    """
    Calculates Simple Moving Averages for both short and long periods.
    We use rolling mean to smooth out price fluctuations and identify trends.
    """
    dataframe['sma_20'] = dataframe['close'].rolling(window=short_window).mean()
    dataframe['sma_50'] = dataframe['close'].rolling(window=long_window).mean()
    return dataframe

def detect_crossover(previous_day, current_day):
    """
    Detects if a moving average crossover occurred between two days.
    We compare the relationship between SMAs on previous day vs current day to detect the exact moment of crossover.
    """
    previous_short_sma = previous_day['sma_20']
    previous_long_sma = previous_day['sma_50']
    current_short_sma = current_day['sma_20']
    current_long_sma = current_day['sma_50']
    
    # Golden Cross: short SMA was below long SMA yesterday, but is above it today
    # This indicates bullish momentum shift
    is_golden_cross = previous_short_sma < previous_long_sma and current_short_sma > current_long_sma
    
    # Death Cross: short SMA was above long SMA yesterday, but is below it today
    # This indicates bearish momentum shift
    is_death_cross = previous_short_sma > previous_long_sma and current_short_sma < current_long_sma
    
    return is_golden_cross, is_death_cross

# 5. Main logic
def main():
    try:
        # Fetch historical data
        price_dataframe = get_historical_data(SYMBOL, DATA_LIMIT)
        
        # Calculate moving averages
        price_dataframe = calculate_smas(price_dataframe, SHORT_SMA_WINDOW, LONG_SMA_WINDOW)
        
        # Extract the last two rows for comparison
        # We need both current and previous day to detect if relationship changed
        last_two_days = price_dataframe.iloc[-2:]
        current_day = last_two_days.iloc[-1]
        previous_day = last_two_days.iloc[-2]
        
        # Display data for verification
        print(f"--- Data for Signal Check ---")
        print(f"Previous Day (Close: {previous_day['close']:.2f}): SMA20={previous_day['sma_20']:.2f}, SMA50={previous_day['sma_50']:.2f}")
        print(f"Current Day (Close: {current_day['close']:.2f}):  SMA20={current_day['sma_20']:.2f}, SMA50={current_day['sma_50']:.2f}")
        
        # Detect crossover
        print("\n--- Signal ---")
        is_golden_cross, is_death_cross = detect_crossover(previous_day, current_day)
        
        if is_golden_cross:
            print("Golden Cross Detected! Potential BUY signal.")
        elif is_death_cross:
            print("Death Cross Detected! Potential SELL signal.")
        else:
            print("No crossover detected. Hold.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# 6. Run
if __name__ == "__main__":
    main()
