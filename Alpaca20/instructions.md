Tutorial 20: The Bigger Picture – Analyzing Multiple Timeframes
Objective: In this advanced tutorial, you will learn a powerful technique used by professional traders: Multi-Timeframe Analysis (MTF). You will build a bot that first identifies the primary trend on a high timeframe (the Daily chart) and then looks for precise entry points on a lower timeframe (the Hourly chart).

1. What is Multi-Timeframe Analysis?
Trading on a single timeframe is like navigating with only a compass. You know your immediate direction, but you can't see the overall landscape. You might be buying in what looks like a small uptrend, while ignoring that you're in the middle of a massive, long-term downtrend.

Multi-Timeframe Analysis solves this by using a "top-down" approach:

Higher Timeframe (HTF) - The Map: You use a chart like the Daily (D1) or Weekly (W1) to establish the dominant, primary trend. Are we in a bull market or a bear market? This tells you which direction you should be trading.

Lower Timeframe (LTF) - The Compass: You use a chart like the Hourly (H1) or 15-Minute (M15) to find the best possible moment to enter a trade in the direction of the primary trend.

This method filters out low-probability trades that go against the "main current" of the market. The mantra is: "Trade with the trend, enter on the pullback."

2. Our MTF Strategy
We will build a bot that follows this exact mantra.

Daily Chart (The Map): We will determine the primary trend using a 50-day Simple Moving Average (SMA).

If Price > 50-day SMA: The primary trend is UP. Our bot is only allowed to look for BUY signals.

If Price < 50-day SMA: The primary trend is DOWN. Our bot is forbidden from buying and will do nothing.

Hourly Chart (The Compass): Once we've confirmed the primary trend is UP, we will look for a low-risk entry point.

Entry Signal: We will wait for a temporary pullback or "dip" on the hourly chart, identified by the RSI becoming oversold (RSI crosses above 30).

This creates a high-probability "buy the dip" strategy within a confirmed uptrend.

3. Creating the Script (mtf_bot.py)
This script is the most advanced one yet, as it needs to fetch and analyze two different sets of data within each loop.

python
# mtf_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "TSLA"
QTY_PER_TRADE = 5
# HTF (Daily) Config
HTF_SMA_PERIOD = 50
# LTF (Hourly) Config
LTF_RSI_PERIOD = 14
LTF_RSI_OVERSOLD = 30
# General
LOOP_SLEEP_SECONDS = 300 # Check every 5 minutes

def run_mtf_bot():
    """Main function for the Multi-Timeframe Bot."""
    print("🚀 Multi-Timeframe Bot (D1 Trend + H1 Entry) is starting...")
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. HIGHER TIMEFRAME ANALYSIS (DAILY CHART) ---
            print("Analyzing Daily chart for primary trend...")
            daily_bars = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Day, limit=HTF_SMA_PERIOD + 5, adjustment='raw').df
            daily_bars[f'sma_{HTF_SMA_PERIOD}'] = daily_bars.ta.sma(length=HTF_SMA_PERIOD)
            
            latest_daily_bar = daily_bars.iloc[-1]
            primary_trend_is_up = latest_daily_bar['close'] > latest_daily_bar[f'sma_{HTF_SMA_PERIOD}']
            
            if primary_trend_is_up:
                print(f"✅ Primary Trend is UP (Price > {HTF_SMA_PERIOD}-Day SMA). Looking for BUY signals on Hourly chart.")
            else:
                print(f"❌ Primary Trend is DOWN (Price < {HTF_SMA_PERIOD}-Day SMA). No trades will be placed.")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue # Skip to the next loop iteration

            # --- 2. LOWER TIMEFRAME ANALYSIS (HOURLY CHART) ---
            # This code only runs if the primary trend is UP.
            print("Analyzing Hourly chart for entry point...")
            
            # Check for existing position first
            try:
                position = api.get_position(SYMBOL_TO_TRADE)
                print(f"Position already exists ({position.qty} shares). Holding.")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue # Skip to the next loop
            except Exception:
                # No position, we can proceed
                pass

            hourly_bars = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Hour, limit=LTF_RSI_PERIOD + 5, adjustment='raw').df
            hourly_bars.ta.rsi(length=LTF_RSI_PERIOD, append=True)
            
            current_hourly_bar = hourly_bars.iloc[-1]
            previous_hourly_bar = hourly_bars.iloc[-2]

            # --- 3. COMBINED MTF TRADING LOGIC ---
            # Entry Signal: RSI crosses up from oversold on the hourly chart
            rsi_buy_signal = previous_hourly_bar[f'RSI_{LTF_RSI_PERIOD}'] < LTF_RSI_OVERSOLD and \
                             current_hourly_bar[f'RSI_{LTF_RSI_PERIOD}'] > LTF_RSI_OVERSOLD

            if rsi_buy_signal:
                print(f"📈 CONFIRMED BUY! Primary trend is UP and LTF shows a dip-buy opportunity. Placing order.")
                api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='buy', type='market', time_in_force='day')
            else:
                print("Signal: No LTF entry signal found. Waiting.")

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
    run_mtf_bot()
4. Understanding the Code
Top-Down Logic: Notice the structure of the main loop. It analyzes the daily data first. If the condition primary_trend_is_up is False, it prints a message and uses continue to immediately jump to the next iteration of the loop, skipping all the lower-timeframe code.

Separate Data Fetches: The bot makes two distinct calls to api.get_bars() within the loop: one for TimeFrame.Day and one for TimeFrame.Hour. This is essential to keep the analyses separate.

The "Gatekeeper": The if primary_trend_is_up: statement acts as a gatekeeper. It ensures that the bot only ever considers buying when the market's main current is in its favor. This is the most critical part of the strategy.

The Entry Trigger: The final buy signal is only evaluated inside the gatekeeper block. The bot waits patiently for a pullback (an oversold RSI reading on the hourly chart) within the established primary uptrend. This increases the probability of a successful trade compared to just blindly buying on an oversold signal in any market condition.