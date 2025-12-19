Tutorial 19: Signal Confirmation – Combining Two Indicators
Objective: In this tutorial, you will take a significant step toward building more robust trading strategies. You will learn how to reduce false signals by building a bot that requires confirmation from two different types of indicators—RSI and MACD—before entering a trade.

1. The Problem of False Signals
Any single indicator can produce "false signals."

RSI might signal a market is oversold, but the price continues to fall for a long time in a strong downtrend.

MACD might have a bullish crossover, but it could be a brief, weak move that quickly reverses.

Relying on one indicator is like listening to one advisor. A smarter approach is to seek a "second opinion" from a different type of indicator. This is called signal confirmation.

2. Our Confirmation Strategy
We will combine a momentum oscillator (RSI) with a trend-following indicator (MACD). This is a classic combination because they measure different aspects of the market.

RSI tells us if a price move is overextended (overbought/oversold).

MACD tells us about the strength and direction of the underlying trend.

Our Logic:

Buy Signal (High-Confidence Entry): We will only enter a trade if BOTH of the following conditions are true:

RSI Signal: The market is coming out of an oversold condition (RSI crosses above 30). This tells us the selling pressure might be exhausted.

MACD Signal: A bullish crossover occurs (MACD line crosses above the signal line). This confirms that new upward momentum is building.

Sell Signal (Exit): To keep things simple, we will exit the trade as soon as the momentum shows signs of failing. We will use a single signal for our exit: a bearish MACD crossover.

3. Prerequisites & Setup
pandas-ta library must be installed.

Project Setup: In your alpaca_bot_project folder, create a new file named confirmation_bot.py.

4. Creating the Script (confirmation_bot.py)
This script combines the logic from our RSI and MACD bots into a single, more intelligent strategy.

python
# confirmation_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AMD"
QTY_PER_TRADE = 10
# RSI Config
RSI_PERIOD = 14
RSI_OVERSOLD = 30
# MACD Config
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
# General
LOOP_SLEEP_SECONDS = 60

def run_confirmation_bot():
    """Main function for the RSI + MACD Confirmation Bot."""
    print("🚀 Confirmation Bot (RSI + MACD) is starting...")
    
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
            barset = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Hour, limit=200, adjustment='raw')
            df = barset.df
            
            # --- 3. Calculate BOTH Indicators ---
            df.ta.rsi(length=RSI_PERIOD, append=True)
            df.ta.macd(fast=MACD_FAST, slow=MACD_SLOW, signal=MACD_SIGNAL, append=True)
            
            # --- 4. Rename Columns for Clarity ---
            df.rename(columns={f'RSI_{RSI_PERIOD}': 'rsi',
                               f'MACD_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'macd_line',
                               f'MACDs_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'signal_line'}, inplace=True)
            
            current_bar = df.iloc[-1]
            previous_bar = df.iloc[-2]

            print(f"Price: {current_bar['close']:.2f} | RSI: {current_bar['rsi']:.2f} | MACD: {current_bar['macd_line']:.2f} | Signal: {current_bar['signal_line']:.2f}")

            # --- 5. Signal Confirmation Logic ---
            # Define the individual signals first for clarity
            rsi_buy_signal = previous_bar['rsi'] < RSI_OVERSOLD and current_bar['rsi'] > RSI_OVERSOLD
            macd_buy_signal = previous_bar['macd_line'] < previous_bar['signal_line'] and current_bar['macd_line'] > current_bar['signal_line']
            
            # BUY Signal (Entry with Confirmation)
            if not position_exists and rsi_buy_signal and macd_buy_signal:
                
                print(f"📈 CONFIRMED BUY! RSI and MACD signals aligned. Placing order.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='buy', type='market', time_in_force='day')

            # SELL Signal (Exit)
            elif position_exists and \
                 previous_bar['macd_line'] > previous_bar['signal_line'] and \
                 current_bar['macd_line'] < current_bar['signal_line']:
                
                print(f"📉 SELL Signal! MACD bearish crossover. Placing order.")
                position_qty = api.get_position(SYMBOL_TO_TRADE).qty
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=position_qty, side='sell', type='market', time_in_force='day')
            
            else:
                print("Signal: No confirmed signal. Holding.")

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
    run_confirmation_bot()
5. Understanding the Code
Calculating Both Indicators: We simply call both df.ta.rsi() and df.ta.macd() one after the other. pandas-ta efficiently calculates and appends all the necessary columns to our DataFrame.

Clear Signal Definitions: To make the final if statement clean and readable, we first evaluate the individual signals and store them in boolean variables (rsi_buy_signal, macd_buy_signal).

The Confirmation if Statement:

python
if not position_exists and rsi_buy_signal and macd_buy_signal:
This is the heart of our new strategy. The and keyword is critical. It ensures that the bot will only proceed to place a buy order if all three conditions are true: we don't already have a position, the RSI gives a buy signal, AND the MACD gives a buy signal.

Reduced Trading Frequency: You will notice that this bot trades much less frequently than the single-indicator bots. This is by design. It's filtering out lower-probability setups and waiting patiently for a high-quality signal where both momentum and trend are aligned in its favor.

Simpler Exit: We use only the MACD bearish crossover as our exit. This is a common practice. Entry rules are often stricter than exit rules. The goal is to get out quickly once momentum begins to fade, and a single indicator is often sufficient for this purpose.

