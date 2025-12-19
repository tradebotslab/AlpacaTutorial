Tutorial 16: Relative Strength – Building an RSI-Based Bot
Objective: In this tutorial, you will learn how to build a "mean-reversion" trading bot using one of the most popular momentum indicators: the Relative Strength Index (RSI). The bot will be designed to identify and trade overbought and oversold market conditions.

1. What is the Relative Strength Index (RSI)?
The RSI is a momentum oscillator that measures the speed and change of price movements. It oscillates between 0 and 100 and is typically used to identify overbought or oversold conditions in a market.

RSI Reading > 70: Generally considered overbought. This suggests that the asset has moved up too far, too fast, and might be due for a corrective pullback or reversal (a potential sell signal).

RSI Reading < 30: Generally considered oversold. This suggests that the asset has moved down too far, too fast, and might be due for a rally or bounce (a potential buy signal).

Our strategy will be to sell when the market is overbought and buy when it is oversold.

2. Prerequisites & Setup
Calculating RSI manually is complex. We will use a fantastic library called pandas-ta that handles all the calculations for us.

Install pandas-ta: Open your terminal and run:

bash
pip install pandas-ta
Project Setup: In your alpaca_bot_project folder, create a new file named rsi_bot.py.

3. Creating the Script (rsi_bot.py)
This script will fetch data, calculate the RSI, and place trades when the RSI crosses the overbought (70) or oversold (30) thresholds.

python
# rsi_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
import pandas_ta as ta # Import the pandas-ta library
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "BTC/USD" # RSI works well with volatile assets like crypto
QTY_PER_TRADE = 1
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
LOOP_SLEEP_SECONDS = 60 # Check every minute

def run_rsi_bot():
    """The main function for the RSI bot."""
    print("🚀 RSI Trading Bot is starting...")
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. Check for existing position ---
            try:
                position = api.get_position(SYMBOL_TO_TRADE)
                position_exists = True
                print(f"✅ Position exists: {position.qty} of {SYMBOL_TO_TRADE}.")
            except Exception:
                position_exists = False
                print("ℹ️ No position currently held.")

            # --- 2. Fetch Data ---
            # Using 15-minute bars for a more active strategy
            barset = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Minute, limit=200, adjustment='raw')
            df = barset.df
            
            # --- 3. Calculate RSI using pandas-ta ---
            # The .ta.rsi() method is added to the DataFrame by the library.
            df['rsi'] = df.ta.rsi(length=RSI_PERIOD)
            
            # --- 4. Extract latest RSI values ---
            current_day = df.iloc[-1]
            previous_day = df.iloc[-2]

            print(f"Current Price: {current_day['close']:.2f}, Current RSI: {current_day['rsi']:.2f}")

            # --- 5. Implement RSI Trading Logic ---
            # BUY Signal: RSI crosses UP from below the oversold level
            if not position_exists and \
               previous_day['rsi'] < RSI_OVERSOLD and current_day['rsi'] > RSI_OVERSOLD:
                
                print(f"📈 BUY Signal! RSI crossed above {RSI_OVERSOLD}. Placing order.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='buy', type='market', time_in_force='day')

            # SELL Signal: RSI crosses DOWN from above the overbought level
            elif position_exists and \
                 previous_day['rsi'] > RSI_OVERBOUGHT and current_day['rsi'] < RSI_OVERBOUGHT:
                
                print(f"📉 SELL Signal! RSI crossed below {RSI_OVERBOUGHT}. Placing order.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='sell', type='market', time_in_force='day')
            
            else:
                print("Signal: No RSI crossover signal. Holding.")

            # --- Sleep ---
            time.sleep(LOOP_SLEEP_SECONDS)

        except KeyboardInterrupt:
            print("\n🛑 Bot shutting down.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)

# --- Entry point of the script ---
if __name__ == '__main__':
    run_rsi_bot()
4. Understanding the Code
import pandas_ta as ta: This line imports the library. By convention, it's given the alias ta.

Configuration: We've added new variables for the RSI_PERIOD (14 is the standard), RSI_OVERBOUGHT (70), and RSI_OVERSOLD (30). We're also using a more volatile symbol (BTC/USD) and checking every minute to create a more active strategy.

df['rsi'] = df.ta.rsi(...): This is the key line. The pandas-ta library automatically adds the .ta accessor to your DataFrame. You can simply call df.ta.rsi() to calculate the indicator and it will be appended as a new column named 'rsi'. It's clean, simple, and powerful.

The Trading Logic:

Buy Signal (previous_day['rsi'] < 30 and current_day['rsi'] > 30): This logic detects the exact moment the RSI crosses up through the oversold line. It doesn't just buy because the RSI is low, but when it shows signs of recovering.

Sell Signal (previous_day['rsi'] > 70 and current_day['rsi'] < 70): Symmetrically, this detects the moment the RSI crosses down through the overbought line, signaling that momentum may be waning.

Mean Reversion: This type of strategy is known as "mean reversion" because it bets on the price returning to its average (mean) after an extreme move. It is the opposite of a "trend-following" strategy like our moving average crossover bot.