# mtf_bot.py
# Tutorial 20: Multi-Timeframe Analysis Bot
# This bot uses a "top-down" approach: Daily chart for trend, Hourly chart for entry

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# --- API Connection ---
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
LOOP_SLEEP_SECONDS = 300  # Check every 5 minutes


def get_daily_trend_direction(symbol, sma_period):
    """
    Analyze the Daily chart to determine the primary trend.
    Returns True if trend is UP, False if DOWN.
    """
    try:
        # Fetch daily bars with extra data for SMA calculation
        daily_bars = api.get_bars(
            symbol,
            TimeFrame.Day,
            limit=sma_period + 5,
            adjustment='raw'
        ).df
        
        # Calculate Simple Moving Average
        daily_bars[f'sma_{sma_period}'] = daily_bars['close'].rolling(window=sma_period).mean()
        
        # Get the most recent daily bar
        latest_daily_bar = daily_bars.iloc[-1]
        
        # Determine if price is above or below the SMA
        primary_trend_is_up = latest_daily_bar['close'] > latest_daily_bar[f'sma_{sma_period}']
        
        return primary_trend_is_up
        
    except Exception as error:
        print(f"Error analyzing daily trend: {error}")
        return None


def get_hourly_rsi_values(symbol, rsi_period):
    """
    Analyze the Hourly chart to calculate RSI values.
    Returns a tuple: (current_rsi, previous_rsi)
    """
    try:
        # Fetch hourly bars with extra data for RSI calculation
        hourly_bars = api.get_bars(
            symbol,
            TimeFrame.Hour,
            limit=rsi_period + 5,
            adjustment='raw'
        ).df
        
        # Calculate RSI using pandas_ta
        hourly_bars.ta.rsi(length=rsi_period, append=True)
        
        # Get current and previous RSI values
        current_hourly_bar = hourly_bars.iloc[-1]
        previous_hourly_bar = hourly_bars.iloc[-2]
        
        current_rsi = current_hourly_bar[f'RSI_{rsi_period}']
        previous_rsi = previous_hourly_bar[f'RSI_{rsi_period}']
        
        return current_rsi, previous_rsi
        
    except Exception as error:
        print(f"Error analyzing hourly RSI: {error}")
        return None, None


def check_existing_position(symbol):
    """
    Check if we already have an open position in this symbol.
    Returns True if position exists, False otherwise.
    """
    try:
        position = api.get_position(symbol)
        print(f"Position already exists ({position.qty} shares). Holding.")
        return True
    except Exception:
        # No position exists (get_position throws exception if no position)
        return False


def place_buy_order(symbol, quantity):
    """
    Place a market buy order for the specified symbol and quantity.
    """
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='day'
        )
        print(f"✅ Order placed successfully! Order ID: {order.id}")
        return True
    except Exception as error:
        print(f"❌ Error placing order: {error}")
        return False


def run_mtf_bot():
    """
    Main function for the Multi-Timeframe Bot.
    Runs continuously, checking both Daily and Hourly timeframes.
    """
    print("=" * 60)
    print("🚀 Multi-Timeframe Bot (D1 Trend + H1 Entry) is starting...")
    print("=" * 60)
    print(f"Symbol: {SYMBOL_TO_TRADE}")
    print(f"Quantity per trade: {QTY_PER_TRADE}")
    print(f"HTF SMA Period: {HTF_SMA_PERIOD} days")
    print(f"LTF RSI Period: {LTF_RSI_PERIOD} hours")
    print(f"RSI Oversold Level: {LTF_RSI_OVERSOLD}")
    print(f"Loop interval: {LOOP_SLEEP_SECONDS} seconds")
    print("=" * 60)
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- STEP 1: HIGHER TIMEFRAME ANALYSIS (DAILY CHART) ---
            print("📊 Analyzing Daily chart for primary trend...")
            primary_trend_is_up = get_daily_trend_direction(SYMBOL_TO_TRADE, HTF_SMA_PERIOD)
            
            # Handle error in fetching daily data
            if primary_trend_is_up is None:
                print("⚠️ Could not determine daily trend. Waiting...")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue
            
            # Display trend analysis result
            if primary_trend_is_up:
                print(f"✅ Primary Trend is UP (Price > {HTF_SMA_PERIOD}-Day SMA).")
                print("   Looking for BUY signals on Hourly chart...")
            else:
                print(f"❌ Primary Trend is DOWN (Price < {HTF_SMA_PERIOD}-Day SMA).")
                print("   No trades will be placed. Waiting for trend reversal...")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue  # Skip to the next loop iteration

            # --- STEP 2: CHECK FOR EXISTING POSITION ---
            # This code only runs if the primary trend is UP
            if check_existing_position(SYMBOL_TO_TRADE):
                time.sleep(LOOP_SLEEP_SECONDS)
                continue  # Skip to the next loop

            # --- STEP 3: LOWER TIMEFRAME ANALYSIS (HOURLY CHART) ---
            print("🔍 Analyzing Hourly chart for entry point...")
            current_rsi, previous_rsi = get_hourly_rsi_values(SYMBOL_TO_TRADE, LTF_RSI_PERIOD)
            
            # Handle error in fetching hourly data
            if current_rsi is None or previous_rsi is None:
                print("⚠️ Could not calculate RSI. Waiting...")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue
            
            print(f"   Previous RSI: {previous_rsi:.2f}")
            print(f"   Current RSI: {current_rsi:.2f}")

            # --- STEP 4: COMBINED MTF TRADING LOGIC ---
            # Entry Signal: RSI crosses up from oversold on the hourly chart
            # WHY: We want to buy after a temporary dip (oversold) in an uptrend
            rsi_buy_signal = (previous_rsi < LTF_RSI_OVERSOLD and 
                            current_rsi > LTF_RSI_OVERSOLD)

            if rsi_buy_signal:
                print("=" * 60)
                print(f"📈 CONFIRMED BUY SIGNAL!")
                print(f"   ✅ Primary trend is UP (Daily chart)")
                print(f"   ✅ RSI crossed above {LTF_RSI_OVERSOLD} (Hourly chart)")
                print(f"   Placing BUY order for {QTY_PER_TRADE} shares of {SYMBOL_TO_TRADE}...")
                print("=" * 60)
                place_buy_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)
            else:
                print("⏳ Signal: No LTF entry signal found. Waiting for pullback...")

            # --- Sleep before next loop iteration ---
            time.sleep(LOOP_SLEEP_SECONDS)

        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("🛑 Bot shutting down by user request.")
            print("=" * 60)
            break
            
        except Exception as error:
            print(f"⚠️ An unexpected error occurred: {error}")
            print("Waiting 60 seconds before retry...")
            time.sleep(60)


# --- Entry point of the script ---
if __name__ == '__main__':
    run_mtf_bot()

