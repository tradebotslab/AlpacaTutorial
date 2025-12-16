Tutorial 10: Your First Complete Bot – Putting It All Together
Objective: In this final tutorial, you will assemble all the individual components you've built—the main loop, data fetching, indicator calculation, and entry/exit logic—into a single, functioning prototype of a moving average crossover trading bot.

1. The Blueprint of Our Bot
We have now created all the necessary pieces. Let's review how they fit together to form a complete automated strategy:

The Engine (The Main Loop): An infinite while True: loop that runs continuously, acting as the bot's heartbeat. It includes a time.sleep() interval to control its frequency.

State Awareness (Position Check): At the start of each loop, the bot checks if it currently holds a position in the target stock (api.get_position). This is crucial for deciding whether to look for a "buy" or a "sell" signal.

Market Analysis (Data & Indicators): The bot fetches the latest price data (api.get_bars) and calculates the 20-day and 50-day Simple Moving Averages.

Signal Detection (Crossover Logic): It compares the SMAs from the current day and the previous day to detect a Golden Cross (buy signal) or a Death Cross (sell signal).

Action (Placing Orders):

If a buy signal is detected AND the bot has no position, it submits a buy order.

If a sell signal is detected AND the bot has a position, it submits a sell order.

If neither of these conditions is met, it does nothing and "holds."

This cycle repeats indefinitely, allowing the bot to manage a trade from entry to exit without any human intervention.

2. The Final Code (crossover_bot_final.py)
This script represents the culmination of all the previous tutorials. It is a clean, working prototype of a crossover bot. You can create a new file or use the code from Tutorial 9, as it already contains all the necessary elements.

python
# crossover_bot_final.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime

# --- Authentication and API Connection ---
# Make sure your config.py has the correct API keys and base_url for paper trading
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 1 # The number of shares to buy/sell per trade
SMA_SHORT_WINDOW = 20
SMA_LONG_WINDOW = 50
LOOP_SLEEP_MINUTES = 5 # How often the bot's main loop should run

def run_trading_bot():
    """The main function for the trading bot."""
    print("🚀 Trading Bot is starting...")
    
    # --- Main Bot Loop ---
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. Check Bot's State: Do we have a position? ---
            try:
                position = api.get_position(SYMBOL_TO_TRADE)
                we_have_a_position = True
                print(f"✅ Position exists: {position.qty} share(s) of {SYMBOL_TO_TRADE}.")
            except Exception:
                # API throws an error if a position does not exist
                we_have_a_position = False
                print("ℹ️ No position currently held.")

            # --- 2. Market Analysis: Fetch data and calculate indicators ---
            # We need enough data for the longest SMA + 1 period for comparison
            data_limit = SMA_LONG_WINDOW + 1 
            barset = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Day, limit=data_limit, adjustment='raw')
            df = barset.df
            
            df[f'sma_{SMA_SHORT_WINDOW}'] = df['close'].rolling(window=SMA_SHORT_WINDOW).mean()
            df[f'sma_{SMA_LONG_WINDOW}'] = df['close'].rolling(window=SMA_LONG_WINDOW).mean()

            # --- 3. Signal Detection: Compare the last two data points ---
            current_day = df.iloc[-1]
            previous_day = df.iloc[-2]

            # --- 4. Decision Logic & Action ---
            # Golden Cross (Bullish Entry Signal)
            if not we_have_a_position and \
               previous_day[f'sma_{SMA_SHORT_WINDOW}'] < previous_day[f'sma_{SMA_LONG_WINDOW}'] and \
               current_day[f'sma_{SMA_SHORT_WINDOW}'] > current_day[f'sma_{SMA_LONG_WINDOW}']:
                
                print(f"📈 Golden Cross Detected! Placing BUY order for {QTY_PER_TRADE} share(s) of {SYMBOL_TO_TRADE}.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='buy', type='market', time_in_force='day')

            # Death Cross (Bearish Exit Signal)
            elif we_have_a_position and \
                 previous_day[f'sma_{SMA_SHORT_WINDOW}'] > previous_day[f'sma_{SMA_LONG_WINDOW}'] and \
                 current_day[f'sma_{SMA_SHORT_WINDOW}'] < current_day[f'sma_{SMA_LONG_WINDOW}']:
                
                print(f"📉 Death Cross Detected! Placing SELL order for {QTY_PER_TRADE} share(s) of {SYMBOL_TO_TRADE}.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='sell', type='market', time_in_force='day')
            
            else:
                print("Signal: No crossover. Holding current state.")

            # --- 5. Sleep until the next loop iteration ---
            sleep_seconds = LOOP_SLEEP_MINUTES * 60
            print(f"Action complete. Sleeping for {LOOP_SLEEP_MINUTES} minutes...")
            time.sleep(sleep_seconds)

        except KeyboardInterrupt:
            # Gracefully shut down the bot on Ctrl+C
            print("\n🛑 Bot is shutting down. Goodbye!")
            break
        except Exception as e:
            # Handle other potential errors (e.g., API connection issues)
            print(f"An error occurred: {e}")
            print("Continuing...")
            time.sleep(60)

# --- Entry point of the script ---
if __name__ == '__main__':
    run_trading_bot()
3. How to Use and Improve Your Bot
Running the Bot: Save the code as crossover_bot_final.py. Run it from your terminal against your Paper Trading account.

bash
python crossover_bot_final.py
Let it run and observe its behavior. It will check the market every 5 minutes and print its analysis. It will only place a trade when the specific crossover conditions are met.

Next Steps and Improvements: This bot is a fantastic starting point, but a real-world strategy requires more sophistication. Here are ideas for your next steps:

Add More Indicators: Combine the SMA signal with another indicator, like the Relative Strength Index (RSI), to confirm the signal.

Implement a Stop-Loss: Automatically sell if the price drops by a certain percentage after you buy, to limit potential losses.

Trade Multiple Symbols: Modify the loop to analyze and trade a list of several different stocks.

Improve Logging: Instead of just printing to the console, log the bot's actions to a file for later review and analysis.

Error Handling: Build more robust error handling for when the API is down or returns unexpected data.

