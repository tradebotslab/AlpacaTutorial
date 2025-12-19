Tutorial 17: The Magic of Volatility – A Bollinger Bands® Bot
Objective: In this tutorial, you will build a bot that capitalizes on changes in market volatility using Bollinger Bands®. You will learn to implement a "squeeze breakout" strategy, which aims to enter a trade just as a period of low volatility erupts into a significant price move.

1. What are Bollinger Bands® and the "Squeeze"?
Bollinger Bands® are a powerful volatility indicator consisting of three lines:

A Middle Band: A Simple Moving Average (SMA) of the price.

An Upper Band: The middle band plus a set number of standard deviations (usually 2).

A Lower Band: The middle band minus the same number of standard deviations.

The distance between the upper and lower bands is a direct measure of volatility.

Bands Widen: Volatility is high.

Bands Narrow: Volatility is low.

A "Squeeze" is a period of very low volatility where the bands contract tightly around the price. The core theory is that these quiet periods are often followed by explosive breakouts. Our strategy is to identify a squeeze and then enter a trade when the price breaks out of this consolidation, catching the beginning of the new move.

2. Prerequisites & Setup
We will again use the pandas-ta library, which makes calculating Bollinger Bands® incredibly simple.

Project Setup: In your alpaca_bot_project folder, create a new file named bollinger_bot.py.

3. Creating the Script (bollinger_bot.py)
This script will identify a Bollinger Band squeeze and place a buy order when the price breaks out above the upper band. It will then sell when the price reverts back towards the middle band.

python
# bollinger_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "NVDA"
BB_PERIOD = 20
BB_STD_DEV = 2.0
# The 'squeeze' is identified when the Bandwidth is below this threshold
SQUEEZE_THRESHOLD = 4.0 # This value may need tuning based on the asset
QTY_PER_TRADE = 5
LOOP_SLEEP_SECONDS = 60 # Check every minute

def run_bollinger_bot():
    """The main function for the Bollinger Bands Squeeze Bot."""
    print("🚀 Bollinger Bands Squeeze Bot is starting...")
    
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
            barset = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Hour, limit=100, adjustment='raw')
            df = barset.df
            
            # --- 3. Calculate Bollinger Bands using pandas-ta ---
            # This automatically adds columns: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0, BBB_20_2.0, BBP_20_2.0
            df.ta.bbands(length=BB_PERIOD, std=BB_STD_DEV, append=True)
            
            # --- 4. Extract latest data points ---
            # We rename columns for easier access
            df.rename(columns={f'BBL_{BB_PERIOD}_{BB_STD_DEV}': 'lower',
                               f'BBM_{BB_PERIOD}_{BB_STD_DEV}': 'middle',
                               f'BBU_{BB_PERIOD}_{BB_STD_DEV}': 'upper',
                               f'BBB_{BB_PERIOD}_{BB_STD_DEV}': 'bandwidth'}, inplace=True)
            
            current_bar = df.iloc[-1]
            previous_bar = df.iloc[-2]

            print(f"Price: {current_bar['close']:.2f}, Bandwidth: {current_bar['bandwidth']:.2f}%")

            # --- 5. Implement Bollinger Band Squeeze Breakout Logic ---
            # BUY Signal: Breakout from a squeeze
            if not position_exists and \
               previous_bar['bandwidth'] < SQUEEZE_THRESHOLD and \
               current_bar['close'] > current_bar['upper']:
                
                print(f"📈 BUY Signal! Breakout from squeeze detected. Placing order.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='buy', type='market', time_in_force='day')

            # SELL Signal: Price reverts back to the mean (middle band)
            elif position_exists and current_bar['close'] < current_bar['middle']:
                
                print(f"📉 SELL Signal! Price reverted to the middle band. Placing order.")
                # We sell all shares we hold
                position_qty = api.get_position(SYMBOL_TO_TRADE).qty
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=position_qty, side='sell', type='market', time_in_force='day')
            
            else:
                print("Signal: No breakout or reversion signal. Holding.")

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
    run_bollinger_bot()
4. Understanding the Code
SQUEEZE_THRESHOLD: This is a key strategic parameter. We define a "squeeze" as any period where the Bollinger Bandwidth is below this value (e.g., 4.0%). The ideal value varies by asset and timeframe and requires testing.

df.ta.bbands(...): This single line of code from pandas-ta calculates all five Bollinger Band components. We set append=True to add them directly as columns to our DataFrame.

Renaming Columns: The default column names from pandas-ta are very descriptive (e.g., BBU_20_2.0) but long. We rename them to lower, middle, upper, and bandwidth to make our if statements much cleaner and easier to read.

The Buy Logic (if not position_exists and ...): This is the core of the breakout strategy. It only triggers if two conditions are met simultaneously:

previous_bar['bandwidth'] < SQUEEZE_THRESHOLD: The market was in a state of low volatility on the previous bar.

current_bar['close'] > current_bar['upper']: The price on the current bar has just exploded upwards, breaking above the upper band.

The Sell Logic (elif position_exists and ...): This is a simple "mean reversion" exit. After a powerful breakout, prices often pull back. Our bot takes its profit (or cuts its loss) when the price momentum fades and crosses back below the middle band (the 20-period SMA). This is a simple but effective way to exit a momentum trade.