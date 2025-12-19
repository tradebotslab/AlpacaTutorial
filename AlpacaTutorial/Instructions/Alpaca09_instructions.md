Tutorial 9: Simple Exit Logic – Selling on a Reversal Signal
Objective: In this tutorial, you will complete your simple bot's logic by implementing an exit strategy. You will learn how to check if you own a stock and then sell it when the trend signal that got you into the trade reverses.

1. Why You Need an Exit Strategy
An entry signal gets you into a trade, but an exit strategy is how you realize a profit or cut a loss. A complete trading strategy must define not only when to buy, but also when to sell.

For our moving average crossover strategy, the exit logic is simple and symmetrical:

Entry: Buy on a Golden Cross (short-SMA crosses above long-SMA).

Exit: Sell on a Death Cross (short-SMA crosses below long-SMA).

This means we will hold the stock as long as the uptrend signal is valid and sell it as soon as a downtrend signal appears.

2. The Logic of the Exit
To implement this, our bot needs to answer two questions during each loop:

"Do I currently own the stock?" We need to check our open positions.

"Has a Death Cross just occurred?" We need to run the crossover detection logic from the previous tutorial.

If the answer to both questions is "yes," it's time to sell.

3. Project Setup
We will now combine everything we've learned into a single, functioning bot. In your alpaca_bot_project folder, create a new file named crossover_bot_v1.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── ... (previous files)
└── crossover_bot_v1.py  # New file
4. Creating the Script (crossover_bot_v1.py)
This script integrates the main loop, data fetching, indicator calculation, and both entry and exit logic.

python
# crossover_bot_v1.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime

# --- Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')
SYMBOL = "AAPL"
QTY_TO_TRADE = 1

def run_bot():
    print("Bot is starting...")
    
    # --- Main Loop ---
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. Check if we already have a position ---
            try:
                position = api.get_position(SYMBOL)
                position_exists = True
                print(f"Position exists: {position.qty} shares of {SYMBOL}.")
            except Exception as e:
                # Throws an error if position does not exist
                position_exists = False
                print("No position exists.")

            # --- 2. Fetch Data and Calculate SMAs ---
            barset = api.get_bars(SYMBOL, TimeFrame.Day, limit=51, adjustment='raw')
            df = barset.df
            df['sma_20'] = df['close'].rolling(window=20).mean()
            df['sma_50'] = df['close'].rolling(window=50).mean()

            current_day = df.iloc[-1]
            previous_day = df.iloc[-2]

            # --- 3. Implement Trading Logic ---
            # Golden Cross (Entry Condition)
            if not position_exists and previous_day['sma_20'] < previous_day['sma_50'] and current_day['sma_20'] > current_day['sma_50']:
                print("Golden Cross Detected! Placing BUY order.")
                api.submit_order(symbol=SYMBOL, qty=QTY_TO_TRADE, side='buy', type='market', time_in_force='day')

            # Death Cross (Exit Condition)
            elif position_exists and previous_day['sma_20'] > previous_day['sma_50'] and current_day['sma_20'] < current_day['sma_50']:
                print("Death Cross Detected! Placing SELL order.")
                api.submit_order(symbol=SYMBOL, qty=QTY_TO_TRADE, side='sell', type='market', time_in_force='day')
            
            else:
                print("No signal. Holding.")

            # --- Sleep until the next interval (e.g., 5 minutes) ---
            print("Action complete. Sleeping for 5 minutes...")
            time.sleep(300) # 300 seconds = 5 minutes

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing...")
            time.sleep(60)

# --- Entry point of the script ---
if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nBot is shutting down. Goodbye!")
5. Understanding the Code
Check for Position (api.get_position):

Before doing anything, we need to know our current state. api.get_position(SYMBOL) is a direct way to check if we own a specific stock.

If it succeeds, it means we have a position, and we set position_exists to True.

If it fails (throws an exception), it means we don't own the stock, and we set position_exists to False. This try/except block is a simple way to manage our state.

Combined Trading Logic:

Entry (if not position_exists and ...): The bot will only consider buying if two conditions are met: it does not already have a position, AND a Golden Cross has just occurred. This prevents the bot from buying more shares when it's already in a trade.

Exit (elif position_exists and ...): The bot will only consider selling if two conditions are met: it does have a position, AND a Death Cross has just occurred. This prevents the bot from trying to sell a stock it doesn't own.

The Main Loop in Action:

The bot now runs in a complete cycle. It wakes up, checks its state, analyzes the market for signals, acts only if its rules are met, and then goes back to sleep.

We've set the sleep interval to 5 minutes (time.sleep(300)). Since we are using daily data, checking this frequently isn't strictly necessary, but it's a realistic interval for a live bot.