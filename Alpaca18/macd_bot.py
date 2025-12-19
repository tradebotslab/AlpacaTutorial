# macd_bot.py
# Tutorial 18: MACD Crossover Trading Bot
# This bot uses the Moving Average Convergence Divergence (MACD) indicator
# to identify momentum shifts and generate buy/sell signals based on crossovers.

# --- 1. Imports ---
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# --- 2. Constants ---
SYMBOL_TO_TRADE = "MSFT"
# Standard MACD parameters (fast EMA, slow EMA, signal line)
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
QTY_PER_TRADE = 10
LOOP_SLEEP_SECONDS = 60  # Check every minute

# --- 3. API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')


# --- 4. Helper Functions ---

def get_position_status(symbol):
    """
    Check if we currently hold a position in the given symbol.
    
    Args:
        symbol (str): The stock symbol to check
    
    Returns:
        tuple: (position_exists, position_qty)
    """
    try:
        position = api.get_position(symbol)
        return True, float(position.qty)
    except Exception:
        return False, 0


def fetch_market_data(symbol, timeframe, limit):
    """
    Fetch historical bar data from Alpaca API.
    
    Args:
        symbol (str): The stock symbol to fetch
        timeframe: The timeframe for bars (e.g., TimeFrame.Hour)
        limit (int): Number of bars to fetch
    
    Returns:
        pandas.DataFrame: Historical price data
    """
    try:
        barset = api.get_bars(symbol, timeframe, limit=limit, adjustment='raw')
        df = barset.df
        return df
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None


def calculate_macd_indicator(df, fast, slow, signal):
    """
    Calculate MACD indicator using pandas-ta library.
    This adds MACD line, signal line, and histogram to the DataFrame.
    
    Args:
        df (pandas.DataFrame): Price data
        fast (int): Fast EMA period
        slow (int): Slow EMA period
        signal (int): Signal line EMA period
    
    Returns:
        pandas.DataFrame: DataFrame with MACD columns added
    """
    # Calculate MACD (adds multiple columns to DataFrame)
    df.ta.macd(fast=fast, slow=slow, signal=signal, append=True)
    
    # Rename columns for clarity
    macd_col_name = f'MACD_{fast}_{slow}_{signal}'
    signal_col_name = f'MACDs_{fast}_{slow}_{signal}'
    
    if macd_col_name in df.columns and signal_col_name in df.columns:
        df.rename(columns={
            macd_col_name: 'macd_line',
            signal_col_name: 'signal_line'
        }, inplace=True)
    
    return df


def detect_bullish_crossover(previous_bar, current_bar):
    """
    Detect if MACD line crossed above signal line (bullish crossover).
    
    Args:
        previous_bar: Previous bar data
        current_bar: Current bar data
    
    Returns:
        bool: True if bullish crossover detected
    """
    previous_macd_below = previous_bar['macd_line'] < previous_bar['signal_line']
    current_macd_above = current_bar['macd_line'] > current_bar['signal_line']
    return previous_macd_below and current_macd_above


def detect_bearish_crossover(previous_bar, current_bar):
    """
    Detect if MACD line crossed below signal line (bearish crossover).
    
    Args:
        previous_bar: Previous bar data
        current_bar: Current bar data
    
    Returns:
        bool: True if bearish crossover detected
    """
    previous_macd_above = previous_bar['macd_line'] > previous_bar['signal_line']
    current_macd_below = current_bar['macd_line'] < current_bar['signal_line']
    return previous_macd_above and current_macd_below


def place_buy_order(symbol, quantity):
    """
    Place a market buy order.
    
    Args:
        symbol (str): Stock symbol to buy
        quantity (int): Number of shares to buy
    """
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='day'
        )
        print(f"✅ BUY order placed: {quantity} shares of {symbol}")
    except Exception as e:
        print(f"❌ Error placing BUY order: {e}")


def place_sell_order(symbol, quantity):
    """
    Place a market sell order.
    
    Args:
        symbol (str): Stock symbol to sell
        quantity (float): Number of shares to sell
    """
    try:
        api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"✅ SELL order placed: {quantity} shares of {symbol}")
    except Exception as e:
        print(f"❌ Error placing SELL order: {e}")


# --- 5. Main Logic ---

def run_macd_bot():
    """
    The main function for the MACD Crossover Bot.
    
    This bot continuously monitors the market and:
    1. Buys when MACD line crosses above signal line (bullish signal)
    2. Sells when MACD line crosses below signal line (bearish signal)
    """
    print("🚀 MACD Crossover Bot is starting...")
    print(f"📊 Trading: {SYMBOL_TO_TRADE}")
    print(f"⚙️ MACD Parameters: Fast={MACD_FAST}, Slow={MACD_SLOW}, Signal={MACD_SIGNAL}")
    print(f"💰 Quantity per trade: {QTY_PER_TRADE} shares")
    print(f"⏱️ Check interval: {LOOP_SLEEP_SECONDS} seconds\n")
    
    while True:
        try:
            # Display current timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"⏰ Loop running at {now}")
            print(f"{'='*60}")
            
            # --- Step 1: Check for existing position ---
            position_exists, position_qty = get_position_status(SYMBOL_TO_TRADE)
            
            if position_exists:
                print(f"✅ Position exists: {position_qty} shares of {SYMBOL_TO_TRADE}")
            else:
                print("ℹ️  No position currently held")
            
            # --- Step 2: Fetch historical data ---
            print(f"📥 Fetching market data...")
            df = fetch_market_data(SYMBOL_TO_TRADE, TimeFrame.Hour, limit=200)
            
            if df is None or len(df) < MACD_SLOW + MACD_SIGNAL:
                print("⚠️  Insufficient data. Waiting for next loop...")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue
            
            # --- Step 3: Calculate MACD indicator ---
            df = calculate_macd_indicator(df, MACD_FAST, MACD_SLOW, MACD_SIGNAL)
            
            # --- Step 4: Extract latest data points ---
            current_bar = df.iloc[-1]
            previous_bar = df.iloc[-2]
            
            current_price = current_bar['close']
            current_macd = current_bar['macd_line']
            current_signal = current_bar['signal_line']
            
            print(f"\n📊 Current Market Data:")
            print(f"   Price: ${current_price:.2f}")
            print(f"   MACD Line: {current_macd:.4f}")
            print(f"   Signal Line: {current_signal:.4f}")
            print(f"   Difference: {(current_macd - current_signal):.4f}")
            
            # --- Step 5: Implement MACD Crossover Trading Logic ---
            
            # BUY Signal: Bullish Crossover (MACD crosses above Signal)
            if not position_exists:
                if detect_bullish_crossover(previous_bar, current_bar):
                    print(f"\n📈 BUY SIGNAL DETECTED!")
                    print(f"   MACD crossed above Signal Line")
                    print(f"   Previous: MACD {previous_bar['macd_line']:.4f} < Signal {previous_bar['signal_line']:.4f}")
                    print(f"   Current:  MACD {current_macd:.4f} > Signal {current_signal:.4f}")
                    place_buy_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)
                else:
                    print(f"\n⏸️  Signal: No bullish crossover. Waiting for entry signal.")
            
            # SELL Signal: Bearish Crossover (MACD crosses below Signal)
            else:
                if detect_bearish_crossover(previous_bar, current_bar):
                    print(f"\n📉 SELL SIGNAL DETECTED!")
                    print(f"   MACD crossed below Signal Line")
                    print(f"   Previous: MACD {previous_bar['macd_line']:.4f} > Signal {previous_bar['signal_line']:.4f}")
                    print(f"   Current:  MACD {current_macd:.4f} < Signal {current_signal:.4f}")
                    place_sell_order(SYMBOL_TO_TRADE, position_qty)
                else:
                    print(f"\n⏸️  Signal: No bearish crossover. Holding position.")
            
            # --- Sleep before next iteration ---
            print(f"\n💤 Sleeping for {LOOP_SLEEP_SECONDS} seconds...")
            time.sleep(LOOP_SLEEP_SECONDS)
        
        except KeyboardInterrupt:
            print("\n\n🛑 Bot shutting down gracefully...")
            print("👋 Thank you for using MACD Crossover Bot!")
            break
        
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print(f"⏳ Waiting 60 seconds before retry...")
            time.sleep(60)


# --- 6. Entry Point ---
if __name__ == '__main__':
    run_macd_bot()

