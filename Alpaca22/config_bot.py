# config_bot.py
# Tutorial 22: Stop Digging in the Code – Using an External Config File

# --- Imports ---
import json
import time
import pandas as pd
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# --- Loading Configuration from JSON File ---
# WHY: This separates configuration from code, making it easier to manage
print("📂 Loading configuration from config.json...")

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    print("✅ Configuration loaded successfully!")
except FileNotFoundError:
    print("❌ Error: config.json not found. Please make sure the file exists.")
    print("💡 Tip: Copy config.example.json to config.json and fill in your details.")
    exit()
except json.JSONDecodeError:
    print("❌ Error: config.json contains invalid JSON format.")
    exit()

# --- Extract Configuration Values ---
# WHY: Converting JSON values to Python variables for easy use throughout the code
API_KEY = config['api_key']
API_SECRET = config['api_secret']
IS_PAPER_TRADING = config['paper_trading']
SYMBOL = config['trade_symbol']
QUANTITY = config['trade_quantity']
SHORT_WINDOW = config['strategy_parameters']['short_window']
LONG_WINDOW = config['strategy_parameters']['long_window']
CHECK_INTERVAL_SECONDS = config.get('check_interval_seconds', 300)  # Default 5 minutes

# --- API Connection ---
# WHY: Initialize Alpaca clients with credentials from config
trading_client = TradingClient(API_KEY, API_SECRET, paper=IS_PAPER_TRADING)
data_client = StockHistoricalDataClient(API_KEY, API_SECRET)


def check_position_exists(symbol):
    """
    Check if we currently have a position in the given symbol.
    Returns the position object if it exists, None otherwise.
    WHY: We need to know if we already own shares before buying more.
    """
    try:
        positions = trading_client.get_all_positions()
        for position in positions:
            if position.symbol == symbol:
                return position
        return None
    except Exception as error:
        print(f"❌ Error checking position: {error}")
        return None


def get_historical_bars(symbol, days_limit):
    """
    Fetch historical daily bars for analysis.
    Returns a pandas DataFrame with OHLCV data.
    WHY: We need historical data to calculate moving averages.
    """
    try:
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            limit=days_limit
        )
        bars = data_client.get_stock_bars(request_params)
        dataframe = bars.df
        return dataframe
    except Exception as error:
        print(f"❌ Error fetching historical data: {error}")
        return None


def calculate_moving_averages(dataframe, short_window, long_window):
    """
    Calculate Simple Moving Averages based on configured windows.
    Returns the dataframe with two new columns added.
    WHY: Moving averages help identify trends and generate signals.
    """
    dataframe['sma_short'] = dataframe['close'].rolling(window=short_window).mean()
    dataframe['sma_long'] = dataframe['close'].rolling(window=long_window).mean()
    return dataframe


def detect_golden_cross(dataframe):
    """
    Detect if a Golden Cross signal occurred.
    Golden Cross = short SMA crosses above long SMA.
    Returns True if signal detected, False otherwise.
    WHY: This is our entry signal for bullish trades.
    """
    if len(dataframe) < 2:
        return False
    
    current_day = dataframe.iloc[-1]
    previous_day = dataframe.iloc[-2]
    
    # Check if crossover happened
    previous_short_below_long = previous_day['sma_short'] < previous_day['sma_long']
    current_short_above_long = current_day['sma_short'] > current_day['sma_long']
    
    golden_cross_detected = previous_short_below_long and current_short_above_long
    return golden_cross_detected


def submit_market_order(symbol, quantity, side):
    """
    Submit a market order to buy or sell.
    WHY: This executes the trade when our strategy generates a signal.
    """
    try:
        market_order_data = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=side,
            time_in_force=TimeInForce.DAY
        )
        
        order = trading_client.submit_order(order_data=market_order_data)
        print(f"✅ Order submitted successfully!")
        print(f"   Order ID: {order.id}")
        print(f"   Symbol: {order.symbol}")
        print(f"   Quantity: {order.qty}")
        print(f"   Side: {order.side}")
        return order
    except Exception as error:
        print(f"❌ Error submitting order: {error}")
        return None


def run_config_bot():
    """
    Main function that runs the configuration-based trading bot.
    WHY: This demonstrates how easy it is to manage a bot using external config.
    """
    print("\n" + "=" * 70)
    print("🚀 Configuration-Based Trading Bot Starting...")
    print("=" * 70)
    print(f"📊 Trading Symbol: {SYMBOL}")
    print(f"📏 Quantity per Trade: {QUANTITY} shares")
    print(f"📈 Strategy: Golden Cross ({SHORT_WINDOW}/{LONG_WINDOW} SMA)")
    print(f"⏱️  Check Interval: {CHECK_INTERVAL_SECONDS} seconds")
    print(f"🔧 Paper Trading: {IS_PAPER_TRADING}")
    print("=" * 70)
    print("\n💡 To change these settings, simply edit config.json!")
    print("   No need to dig through the code!\n")
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {current_time} ---")

            # --- Step 1: Check if we have a position ---
            position = check_position_exists(SYMBOL)
            
            if position is not None:
                # We already have a position
                current_position_value = float(position.qty) * float(position.current_price)
                unrealized_pl = float(position.unrealized_pl)
                unrealized_pl_percent = float(position.unrealized_plpc) * 100
                
                print(f"✅ Position exists: {position.qty} share(s)")
                print(f"💵 Current Value: ${current_position_value:,.2f}")
                print(f"📊 Unrealized P/L: ${unrealized_pl:,.2f} ({unrealized_pl_percent:.2f}%)")
                print("ℹ️  Holding position. Monitoring...")
                
            else:
                # No position exists, look for entry signal
                print("ℹ️  No position held. Analyzing for entry signal...")

                # --- Step 2: Get historical data ---
                # Need enough bars for the longer moving average
                bars = get_historical_bars(SYMBOL, days_limit=LONG_WINDOW + 2)
                
                if bars is None or len(bars) < LONG_WINDOW:
                    print(f"⚠️  Not enough historical data. Need at least {LONG_WINDOW} bars.")
                else:
                    # --- Step 3: Calculate moving averages ---
                    bars_with_sma = calculate_moving_averages(bars, SHORT_WINDOW, LONG_WINDOW)
                    
                    # Get the latest values
                    latest_bar = bars_with_sma.iloc[-1]
                    latest_close = latest_bar['close']
                    latest_sma_short = latest_bar['sma_short']
                    latest_sma_long = latest_bar['sma_long']
                    
                    print(f"📊 Current Price: ${latest_close:.2f}")
                    print(f"📈 SMA {SHORT_WINDOW}: ${latest_sma_short:.2f}")
                    print(f"📉 SMA {LONG_WINDOW}: ${latest_sma_long:.2f}")
                    
                    # --- Step 4: Check for Golden Cross signal ---
                    signal_detected = detect_golden_cross(bars_with_sma)
                    
                    if signal_detected:
                        print("\n" + "=" * 70)
                        print("🎯 GOLDEN CROSS DETECTED!")
                        print("=" * 70)
                        print(f"📊 Short SMA ({SHORT_WINDOW}) crossed above Long SMA ({LONG_WINDOW})")
                        print(f"💰 Buying {QUANTITY} shares of {SYMBOL}")
                        
                        # --- Step 5: Submit buy order ---
                        order = submit_market_order(SYMBOL, QUANTITY, OrderSide.BUY)
                        
                        if order:
                            print("✅ Position opened successfully!")
                            print("\n💡 Want to change the strategy parameters?")
                            print("   Just edit config.json - no code changes needed!")
                    else:
                        print("⏸️  No entry signal detected. Waiting...")
            
            # --- Step 6: Sleep before next iteration ---
            print(f"\n💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("🛑 Bot is shutting down. Goodbye!")
            print("=" * 70)
            break
            
        except Exception as error:
            print(f"❌ An error occurred: {error}")
            print("⚠️  Continuing in 60 seconds...")
            time.sleep(60)


# --- Entry Point ---
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("📚 Alpaca Trading Course - Lesson 22")
    print("📖 Stop Digging in the Code – Using an External Config File")
    print("=" * 70)
    
    run_config_bot()

