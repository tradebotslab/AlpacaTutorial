# discord_bot.py
# Tutorial 24: Stay Updated – Sending Real-Time Notifications to Discord

# --- Imports ---
import json
import time
import logging
import requests
import pandas as pd
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# --- Configuration Files ---
# WHY: Separate configuration files for different concerns
CONFIG_FILE = 'config.json'
STATE_FILE = 'state.json'

# --- Logging Setup ---
# WHY: Logging helps track bot actions and debug issues
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Loading Configuration from JSON File ---
# WHY: This separates configuration from code, making it easier to manage
print("📂 Loading configuration from config.json...")
logging.info("Loading configuration from config.json...")

try:
    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)
    print("✅ Configuration loaded successfully!")
    logging.info("Configuration loaded successfully!")
except FileNotFoundError:
    print("❌ Error: config.json not found. Please make sure the file exists.")
    print("💡 Tip: Copy config.example.json to config.json and fill in your details.")
    logging.error("config.json not found!")
    exit()
except json.JSONDecodeError:
    print("❌ Error: config.json contains invalid JSON format.")
    logging.error("config.json contains invalid JSON format!")
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
DISCORD_WEBHOOK_URL = config.get('discord_webhook_url', '')  # Optional Discord webhook

# --- API Connection ---
# WHY: Initialize Alpaca clients with credentials from config
trading_client = TradingClient(API_KEY, API_SECRET, paper=IS_PAPER_TRADING)
data_client = StockHistoricalDataClient(API_KEY, API_SECRET)


# --- Discord Notification Function ---
def send_discord_notification(message):
    """
    Sends a message to a Discord channel via a webhook.
    WHY: Real-time notifications provide immediate awareness of bot actions.
    """
    if not DISCORD_WEBHOOK_URL:
        # Silently skip if no webhook is configured
        return
    
    data = {"content": message}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(
            DISCORD_WEBHOOK_URL, 
            data=json.dumps(data), 
            headers=headers,
            timeout=10
        )
        response.raise_for_status()  # Raises an exception for bad status codes
        logging.info(f"Discord notification sent: {message[:50]}...")
    except requests.exceptions.RequestException as error:
        # Log the error but don't stop the bot
        logging.error(f"Failed to send Discord notification: {error}")
        print(f"⚠️  Warning: Could not send Discord notification: {error}")


# --- State Management Functions ---
def load_state():
    """
    Loads the bot's state from the state file.
    WHY: This allows the bot to remember its position across restarts.
    """
    try:
        with open(STATE_FILE, 'r') as state_file:
            state = json.load(state_file)
        print("✅ State file found. Loaded bot state from disk.")
        logging.info(f"State loaded from file: {state}")
        return state
    except FileNotFoundError:
        print("⚠️  State file not found. Starting with default state.")
        logging.warning("State file not found. Starting with default state.")
        return {'is_in_position': False}
    except json.JSONDecodeError:
        print("⚠️  State file contains invalid JSON. Starting with default state.")
        logging.warning("State file contains invalid JSON. Starting with default state.")
        return {'is_in_position': False}


def save_state(state):
    """
    Saves the bot's state to the state file.
    WHY: This ensures the bot can restore its position after a restart.
    """
    try:
        with open(STATE_FILE, 'w') as state_file:
            json.dump(state, state_file, indent=2)
        logging.info(f"State saved: {state}")
        print(f"💾 State saved to disk: {state}")
    except Exception as error:
        logging.error(f"Failed to save state: {error}")
        print(f"❌ Error saving state: {error}")


def synchronize_state_with_broker(symbol):
    """
    Verifies the bot's state against the actual position at the broker.
    WHY: The broker is the ultimate source of truth. This protects against
    corrupted state files or missed updates.
    """
    print(f"🔄 Synchronizing state with broker for {symbol}...")
    logging.info(f"Synchronizing state with broker for {symbol}...")
    
    try:
        position = trading_client.get_open_position(symbol)
        # If this doesn't raise an exception, we have a position
        is_in_position = True
        qty = float(position.qty)
        print(f"✅ Found existing position on Alpaca: {qty} shares of {symbol}")
        logging.info(f"Found existing position: {qty} shares of {symbol}")
    except Exception:
        # An exception means no open position was found for that symbol
        is_in_position = False
        print(f"ℹ️  No existing position found on Alpaca for {symbol}")
        logging.info(f"No existing position found for {symbol}")
    
    return is_in_position


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
        logging.error(f"Error fetching historical data: {error}")
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


def detect_death_cross(dataframe):
    """
    Detect if a Death Cross signal occurred.
    Death Cross = short SMA crosses below long SMA.
    Returns True if signal detected, False otherwise.
    WHY: This is our exit signal (bearish indicator).
    """
    if len(dataframe) < 2:
        return False
    
    current_day = dataframe.iloc[-1]
    previous_day = dataframe.iloc[-2]
    
    # Check if crossover happened
    previous_short_above_long = previous_day['sma_short'] > previous_day['sma_long']
    current_short_below_long = current_day['sma_short'] < current_day['sma_long']
    
    death_cross_detected = previous_short_above_long and current_short_below_long
    return death_cross_detected


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
        logging.info(f"Order submitted: {order.side} {order.qty} shares of {order.symbol}")
        return order
    except Exception as error:
        print(f"❌ Error submitting order: {error}")
        logging.error(f"Error submitting order: {error}")
        return None


def run_discord_notified_bot():
    """
    Main function that runs the trading bot with Discord notifications and state management.
    WHY: This demonstrates how to build a fully observable, resilient trading bot.
    """
    print("\n" + "=" * 70)
    print("🚀 Discord-Notified Trading Bot Starting...")
    print("=" * 70)
    print(f"📊 Trading Symbol: {SYMBOL}")
    print(f"📏 Quantity per Trade: {QUANTITY} shares")
    print(f"📈 Strategy: Golden Cross ({SHORT_WINDOW}/{LONG_WINDOW} SMA)")
    print(f"⏱️  Check Interval: {CHECK_INTERVAL_SECONDS} seconds")
    print(f"🔧 Paper Trading: {IS_PAPER_TRADING}")
    
    if DISCORD_WEBHOOK_URL:
        print(f"📢 Discord Notifications: ✅ ENABLED")
    else:
        print(f"📢 Discord Notifications: ⚠️  DISABLED (no webhook configured)")
    
    print("=" * 70)
    
    logging.info("=" * 70)
    logging.info("Discord-Notified Trading Bot Starting")
    logging.info(f"Symbol: {SYMBOL}, Quantity: {QUANTITY}")
    logging.info(f"Strategy: Golden Cross ({SHORT_WINDOW}/{LONG_WINDOW})")
    logging.info("=" * 70)
    
    # --- Send startup notification to Discord ---
    startup_message = (
        f"✅ **Bot Started Up**\n"
        f"```\n"
        f"Symbol: {SYMBOL}\n"
        f"Quantity: {QUANTITY} shares\n"
        f"Strategy: Golden Cross ({SHORT_WINDOW}/{LONG_WINDOW})\n"
        f"Paper Trading: {IS_PAPER_TRADING}\n"
        f"```"
    )
    send_discord_notification(startup_message)
    
    # --- Step 1: Load saved state ---
    bot_state = load_state()
    is_in_position = bot_state.get('is_in_position', False)
    
    print(f"\n📋 Loaded State: is_in_position = {is_in_position}")
    
    # --- Step 2: Synchronize with broker (source of truth) ---
    actual_position = synchronize_state_with_broker(SYMBOL)
    
    if actual_position != is_in_position:
        print("\n⚠️  WARNING: State mismatch detected!")
        print(f"   Saved state: {is_in_position}")
        print(f"   Actual broker state: {actual_position}")
        print("   Updating local state to match broker...")
        logging.warning(f"State mismatch: saved={is_in_position}, actual={actual_position}")
        
        # Send Discord notification about state mismatch
        mismatch_message = (
            f"⚠️  **State Mismatch Detected**\n"
            f"```\n"
            f"Saved State: {is_in_position}\n"
            f"Broker State: {actual_position}\n"
            f"Action: Synchronized to match broker\n"
            f"```"
        )
        send_discord_notification(mismatch_message)
        
        is_in_position = actual_position
        bot_state['is_in_position'] = is_in_position
        save_state(bot_state)
    else:
        print("✅ State is synchronized with broker.")
    
    print("\n💡 This bot combines state management with Discord notifications!")
    print("   You'll receive real-time updates on your phone or desktop.\n")
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {current_time} ---")
            logging.info(f"--- Loop running at {current_time} ---")

            # --- Step 3: Get historical data ---
            bars = get_historical_bars(SYMBOL, days_limit=LONG_WINDOW + 2)
            
            if bars is None or len(bars) < LONG_WINDOW:
                print(f"⚠️  Not enough historical data. Need at least {LONG_WINDOW} bars.")
                logging.warning("Not enough historical data.")
            else:
                # --- Step 4: Calculate moving averages ---
                bars_with_sma = calculate_moving_averages(bars, SHORT_WINDOW, LONG_WINDOW)
                
                # Get the latest values
                latest_bar = bars_with_sma.iloc[-1]
                latest_close = latest_bar['close']
                latest_sma_short = latest_bar['sma_short']
                latest_sma_long = latest_bar['sma_long']
                
                print(f"📊 Current Price: ${latest_close:.2f}")
                print(f"📈 SMA {SHORT_WINDOW}: ${latest_sma_short:.2f}")
                print(f"📉 SMA {LONG_WINDOW}: ${latest_sma_long:.2f}")
                print(f"📋 Current State: is_in_position = {is_in_position}")
                
                # --- Step 5: Check for signals based on current state ---
                if not is_in_position:
                    # Look for BUY signal (Golden Cross)
                    signal_detected = detect_golden_cross(bars_with_sma)
                    
                    if signal_detected:
                        print("\n" + "=" * 70)
                        print("🎯 GOLDEN CROSS DETECTED!")
                        print("=" * 70)
                        print(f"📊 Short SMA ({SHORT_WINDOW}) crossed above Long SMA ({LONG_WINDOW})")
                        print(f"💰 Buying {QUANTITY} shares of {SYMBOL}")
                        logging.info("GOLDEN CROSS DETECTED - Attempting BUY")
                        
                        # Submit buy order
                        order = submit_market_order(SYMBOL, QUANTITY, OrderSide.BUY)
                        
                        if order:
                            # --- CRITICAL: Update and save state after successful order ---
                            is_in_position = True
                            bot_state['is_in_position'] = True
                            save_state(bot_state)
                            print("✅ Position opened and state saved!")
                            logging.info("Position opened successfully. State updated.")
                            
                            # --- Send Discord notification about BUY order ---
                            buy_message = (
                                f"🚀 **BUY Order Executed**\n"
                                f"```\n"
                                f"Symbol: {SYMBOL}\n"
                                f"Quantity: {QUANTITY} shares\n"
                                f"Price: ${latest_close:.2f}\n"
                                f"Signal: Golden Cross\n"
                                f"SMA {SHORT_WINDOW}: ${latest_sma_short:.2f}\n"
                                f"SMA {LONG_WINDOW}: ${latest_sma_long:.2f}\n"
                                f"Order ID: {order.id}\n"
                                f"```"
                            )
                            send_discord_notification(buy_message)
                        else:
                            # Send error notification
                            error_message = (
                                f"❌ **BUY Order Failed**\n"
                                f"```\n"
                                f"Symbol: {SYMBOL}\n"
                                f"Quantity: {QUANTITY} shares\n"
                                f"Check logs for details\n"
                                f"```"
                            )
                            send_discord_notification(error_message)
                    else:
                        print("⏸️  No entry signal detected. Waiting...")
                        logging.info("No entry signal detected.")
                
                else:
                    # We are in a position, look for SELL signal (Death Cross)
                    signal_detected = detect_death_cross(bars_with_sma)
                    
                    if signal_detected:
                        print("\n" + "=" * 70)
                        print("⚠️  DEATH CROSS DETECTED!")
                        print("=" * 70)
                        print(f"📊 Short SMA ({SHORT_WINDOW}) crossed below Long SMA ({LONG_WINDOW})")
                        print(f"💸 Closing position on {SYMBOL}")
                        logging.info("DEATH CROSS DETECTED - Attempting SELL")
                        
                        # Close the position
                        try:
                            trading_client.close_position(SYMBOL)
                            print("✅ Position closed successfully!")
                            logging.info("Position closed successfully.")
                            
                            # --- CRITICAL: Update and save state after successful close ---
                            is_in_position = False
                            bot_state['is_in_position'] = False
                            save_state(bot_state)
                            print("💾 State updated: is_in_position = False")
                            
                            # --- Send Discord notification about SELL order ---
                            sell_message = (
                                f"💸 **SELL Order Executed**\n"
                                f"```\n"
                                f"Symbol: {SYMBOL}\n"
                                f"Action: Position Closed\n"
                                f"Exit Price: ${latest_close:.2f}\n"
                                f"Signal: Death Cross\n"
                                f"SMA {SHORT_WINDOW}: ${latest_sma_short:.2f}\n"
                                f"SMA {LONG_WINDOW}: ${latest_sma_long:.2f}\n"
                                f"```"
                            )
                            send_discord_notification(sell_message)
                            
                        except Exception as error:
                            print(f"❌ Error closing position: {error}")
                            logging.error(f"Error closing position: {error}")
                            
                            # Send error notification
                            error_message = (
                                f"❌ **SELL Order Failed**\n"
                                f"```\n"
                                f"Symbol: {SYMBOL}\n"
                                f"Error: {str(error)[:100]}\n"
                                f"```"
                            )
                            send_discord_notification(error_message)
                    else:
                        print("📊 Holding position. Monitoring for exit signal...")
                        logging.info("Holding position. No exit signal.")
            
            # --- Step 6: Sleep before next iteration ---
            print(f"\n💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("🛑 Bot is shutting down. State has been saved.")
            print("   When you restart, the bot will remember its position!")
            print("=" * 70)
            logging.info("Bot shutdown by user.")
            
            # Send shutdown notification to Discord
            shutdown_message = (
                f"⏹️  **Bot Shutdown**\n"
                f"```\n"
                f"Reason: Manual stop by user\n"
                f"Final State: is_in_position = {is_in_position}\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"```"
            )
            send_discord_notification(shutdown_message)
            break
            
        except Exception as error:
            print(f"❌ An error occurred: {error}")
            logging.error(f"An error occurred: {error}")
            print("⚠️  Continuing in 60 seconds...")
            
            # Send error notification to Discord
            error_message = (
                f"❌ **Unexpected Error**\n"
                f"```\n"
                f"Error: {str(error)[:200]}\n"
                f"Status: Bot will retry in 60 seconds\n"
                f"```"
            )
            send_discord_notification(error_message)
            
            time.sleep(60)


# --- Entry Point ---
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("📚 Alpaca Trading Course - Lesson 24")
    print("📖 Stay Updated – Sending Real-Time Notifications to Discord")
    print("=" * 70)
    
    run_discord_notified_bot()

