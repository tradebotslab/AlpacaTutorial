Tutorial 8: Simple Entry Logic – Detecting a Moving Average Crossover
Objective: In this tutorial, you will build on the previous lesson to create your first piece of trading logic. You will learn how to write a simple if statement to detect a "moving average crossover," a classic signal used in many trading strategies.

1. What is a Moving Average Crossover?
A moving average crossover occurs when a shorter-term Simple Moving Average (SMA) crosses over a longer-term SMA. This event is often interpreted by traders as a signal that the trend may be changing.

There are two main types of crossovers:

Golden Cross (Bullish Signal): The short-term SMA crosses above the long-term SMA. This can indicate that the price momentum is shifting upwards, and is often seen as a signal to buy.

Death Cross (Bearish Signal): The short-term SMA crosses below the long-term SMA. This can indicate that the price momentum is shifting downwards, and is often seen as a signal to sell.

2. The Logic of Detection
How do we detect the exact moment of a crossover? We can't just check if sma_20 > sma_50. We need to know if that relationship has just changed.

The logic is as follows:

A Golden Cross occurs if on the previous day the short-SMA was below the long-SMA, AND on the current day the short-SMA is above the long-SMA.

3. Project Setup
In your alpaca_bot_project folder, create a new file named crossover_detector.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── ... (previous files)
└── crossover_detector.py # New file
4. Creating the Script (crossover_detector.py)
Open crossover_detector.py and add the following code. This script will fetch data, calculate SMAs, and then check if a crossover occurred on the most recent day.

python
# crossover_detector.py

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
import config

# --- 1. Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

try:
    # --- 2. Fetch Data and Calculate SMAs (from Tutorial 7) ---
    symbol = "AAPL"
    barset = api.get_bars(
        symbol,
        TimeFrame.Day,
        limit=51, # We need 51 bars to have two full values for the 50-day SMA
        adjustment='raw'
    )
    df = barset.df
    
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()

    # --- 3. Extract the Last Two Rows for Comparison ---
    # We need the most recent day (current) and the day before it (previous)
    # .iloc[-1] gets the last row, .iloc[-2] gets the second to last row
    last_two_days = df.iloc[-2:]

    current_day = last_two_days.iloc[-1]
    previous_day = last_two_days.iloc[-2]

    print(f"--- Data for Signal Check ---")
    print(f"Previous Day (Close: {previous_day['close']:.2f}): SMA20={previous_day['sma_20']:.2f}, SMA50={previous_day['sma_50']:.2f}")
    print(f"Current Day (Close: {current_day['close']:.2f}):  SMA20={current_day['sma_20']:.2f}, SMA50={current_day['sma_50']:.2f}")

    # --- 4. The Crossover Logic ---
    print("\n--- Signal ---")
    # Golden Cross (Bullish) Condition
    if previous_day['sma_20'] < previous_day['sma_50'] and current_day['sma_20'] > current_day['sma_50']:
        print("Golden Cross Detected! Potential BUY signal.")
    
    # Death Cross (Bearish) Condition
    elif previous_day['sma_20'] > previous_day['sma_50'] and current_day['sma_20'] < current_day['sma_50']:
        print("Death Cross Detected! Potential SELL signal.")
    
    else:
        print("No crossover detected. Hold.")

except Exception as e:
    print(f"An error occurred: {e}")
5. Understanding the Code
Fetch Data: We fetch the last 51 days of data. We need at least 50 days to calculate one value for sma_50, and we need the 51st day to have a previous sma_50 value to compare against.

Calculate SMAs: Same logic as in the previous tutorial.

Extract Last Two Rows (.iloc[-1] and .iloc[-2]):

To check for a change, we need to compare today's state with yesterday's state.

pandas makes this easy. .iloc[-1] selects the very last row of the DataFrame (the current, most recent data).

.iloc[-2] selects the second-to-last row (the previous period's data).

We store these two rows in current_day and previous_day variables to make the if statement easier to read.

The if/elif/else Logic: This is the "brain" of our signal detector.

Golden Cross: The first if statement checks the exact condition for a bullish crossover: was the 20-day SMA below the 50-day yesterday, AND is it above it today?

Death Cross: The elif (else if) statement checks the opposite condition for a bearish crossover.

No Signal: If neither of those conditions is true, the else block executes, telling us to hold.

