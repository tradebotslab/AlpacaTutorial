# resilient_bot.py
# Tutorial 25: Making Your Bot Resilient – Handling API and Connection Errors

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


# --- Configuration Loading with Error Handling ---
def load_configuration():
    """
    Load configuration from JSON file with comprehensive error handling.
    WHY: File operations can fail, so we need to handle those errors gracefully.
    """
    print("📂 Loading configuration from config.json...")
    logging.info("Loading configuration from config.json...")
    
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
        print("✅ Configuration loaded successfully!")
        logging.info("Configuration loaded successfully!")
        return config
    
    except FileNotFoundError:
        error_message = "config.json not found. Please make sure the file exists."
        print(f"❌ Error: {error_message}")
        print("💡 Tip: Copy config.example.json to config.json and fill in your details.")
        logging.error(error_message)
        # This is a critical error - we cannot continue without configuration
        exit(1)
    
    except json.JSONDecodeError as error:
        error_message = f"config.json contains invalid JSON format: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        # This is a critical error - we cannot continue with corrupted config
        exit(1)
    
    except Exception as error:
        error_message = f"Unexpected error loading configuration: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        exit(1)


# --- Load Configuration ---
config = load_configuration()

# --- Extract Configuration Values ---
API_KEY = config['api_key']
API_SECRET = config['api_secret']
IS_PAPER_TRADING = config['paper_trading']
SYMBOL = config['trade_symbol']
QUANTITY = config['trade_quantity']
SHORT_WINDOW = config['strategy_parameters']['short_window']
LONG_WINDOW = config['strategy_parameters']['long_window']
CHECK_INTERVAL_SECONDS = config.get('check_interval_seconds', 300)
DISCORD_WEBHOOK_URL = config.get('discord_webhook_url', '')

# --- API Connection with Error Handling ---
def initialize_alpaca_clients():
    """
    Initialize Alpaca API clients with error handling.
    WHY: API initialization can fail if credentials are invalid.
    """
    try:
        trading_client = TradingClient(API_KEY, API_SECRET, paper=IS_PAPER_TRADING)
        data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
        print("✅ Alpaca API clients initialized successfully!")
        logging.info("Alpaca API clients initialized successfully!")
        return trading_client, data_client
    
    except Exception as error:
        error_message = f"Failed to initialize Alpaca clients: {error}"
        print(f"❌ Error: {error_message}")
        print("💡 Check your API credentials in config.json")
        logging.error(error_message)
        exit(1)


trading_client, data_client = initialize_alpaca_clients()


# --- Discord Notification Function with Error Handling ---
def send_discord_notification(message):
    """
    Sends a message to a Discord channel via a webhook with error handling.
    WHY: Network requests can fail, but this is not critical for trading operations.
    STRATEGY: Log and Continue - notification failure should not stop the bot.
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
        response.raise_for_status()
        logging.info(f"Discord notification sent: {message[:50]}...")
        
    except requests.exceptions.Timeout:
        # Timeout is a common temporary issue
        logging.warning("Discord notification timed out (10 seconds)")
        print("⚠️  Warning: Discord notification timed out")
    
    except requests.exceptions.ConnectionError as error:
        # Network connectivity issue
        logging.warning(f"Discord notification failed - connection error: {error}")
        print("⚠️  Warning: Could not connect to Discord (network issue)")
    
    except requests.exceptions.HTTPError as error:
        # HTTP error (4xx, 5xx)
        logging.warning(f"Discord notification failed - HTTP error: {error}")
        print(f"⚠️  Warning: Discord webhook error: {error}")
    
    except Exception as error:
        # Any other unexpected error
        logging.error(f"Unexpected error sending Discord notification: {error}")
        print(f"⚠️  Warning: Unexpected Discord error: {error}")


# --- State Management Functions with Error Handling ---
def load_state():
    """
    Loads the bot's state from the state file with error handling.
    WHY: File operations can fail due to corrupted files or permission issues.
    STRATEGY: Return default state if loading fails.
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
    
    except json.JSONDecodeError as error:
        error_message = f"State file contains invalid JSON: {error}"
        print(f"⚠️  {error_message}. Starting with default state.")
        logging.warning(error_message)
        return {'is_in_position': False}
    
    except Exception as error:
        error_message = f"Unexpected error loading state: {error}"
        print(f"⚠️  {error_message}. Starting with default state.")
        logging.error(error_message)
        return {'is_in_position': False}


def save_state(state):
    """
    Saves the bot's state to the state file with error handling.
    WHY: File write operations can fail due to disk space or permissions.
    STRATEGY: Log and Continue - if we can't save state, we continue but log the error.
    """
    try:
        with open(STATE_FILE, 'w') as state_file:
            json.dump(state, state_file, indent=2)
        logging.info(f"State saved: {state}")
        print(f"💾 State saved to disk: {state}")
        return True
    
    except PermissionError:
        error_message = "Permission denied when saving state file"
        logging.error(error_message)
        print(f"❌ Error: {error_message}")
        return False
    
    except OSError as error:
        error_message = f"OS error when saving state (disk space?): {error}"
        logging.error(error_message)
        print(f"❌ Error: {error_message}")
        return False
    
    except Exception as error:
        error_message = f"Unexpected error saving state: {error}"
        logging.error(error_message)
        print(f"❌ Error: {error_message}")
        return False


def synchronize_state_with_broker(symbol):
    """
    Verifies the bot's state against the actual position at the broker with error handling.
    WHY: API calls can fail, but this is critical for determining position status.
    STRATEGY: If API fails, return None to signal that we couldn't verify.
    """
    print(f"🔄 Synchronizing state with broker for {symbol}...")
    logging.info(f"Synchronizing state with broker for {symbol}...")
    
    try:
        position = trading_client.get_open_position(symbol)
        # If this doesn't raise an exception, we have a position
        qty = float(position.qty)
        print(f"✅ Found existing position on Alpaca: {qty} shares of {symbol}")
        logging.info(f"Found existing position: {qty} shares of {symbol}")
        return True
    
    except Exception as error:
        # Check if it's a "no position found" error vs a real API error
        error_str = str(error).lower()
        
        if 'position does not exist' in error_str or 'not found' in error_str:
            # This is normal - no position exists
            print(f"ℹ️  No existing position found on Alpaca for {symbol}")
            logging.info(f"No existing position found for {symbol}")
            return False
        else:
            # This is a real API error
            error_message = f"API error when checking position: {error}"
            print(f"❌ Error: {error_message}")
            logging.error(error_message)
            return None  # Signal that we couldn't determine the state


def get_historical_bars(symbol, days_limit):
    """
    Fetch historical daily bars for analysis with error handling.
    Returns a pandas DataFrame with OHLCV data, or None if failed.
    WHY: Network and API calls can fail temporarily.
    STRATEGY: Return None and let caller decide how to handle it.
    """
    try:
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Day,
            limit=days_limit
        )
        bars = data_client.get_stock_bars(request_params)
        dataframe = bars.df
        
        if dataframe is None or len(dataframe) == 0:
            print(f"⚠️  No data returned for {symbol}")
            logging.warning(f"No data returned for {symbol}")
            return None
        
        return dataframe
    
    except requests.exceptions.Timeout:
        error_message = "API request timed out while fetching historical data"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None
    
    except requests.exceptions.ConnectionError:
        error_message = "Network connection error while fetching historical data"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None
    
    except Exception as error:
        error_message = f"Error fetching historical data: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None


def calculate_moving_averages(dataframe, short_window, long_window):
    """
    Calculate Simple Moving Averages with error handling.
    WHY: Data processing can fail if dataframe is malformed.
    """
    try:
        dataframe['sma_short'] = dataframe['close'].rolling(window=short_window).mean()
        dataframe['sma_long'] = dataframe['close'].rolling(window=long_window).mean()
        return dataframe
    
    except KeyError as error:
        error_message = f"Missing required column in dataframe: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None
    
    except Exception as error:
        error_message = f"Error calculating moving averages: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None


def detect_golden_cross(dataframe):
    """
    Detect if a Golden Cross signal occurred with error handling.
    WHY: Data access can fail if dataframe is incomplete or malformed.
    """
    try:
        if len(dataframe) < 2:
            return False
        
        current_day = dataframe.iloc[-1]
        previous_day = dataframe.iloc[-2]
        
        # Check if crossover happened
        previous_short_below_long = previous_day['sma_short'] < previous_day['sma_long']
        current_short_above_long = current_day['sma_short'] > current_day['sma_long']
        
        golden_cross_detected = previous_short_below_long and current_short_above_long
        return golden_cross_detected
    
    except (KeyError, IndexError) as error:
        error_message = f"Error detecting golden cross: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False
    
    except Exception as error:
        error_message = f"Unexpected error in golden cross detection: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False


def detect_death_cross(dataframe):
    """
    Detect if a Death Cross signal occurred with error handling.
    WHY: Data access can fail if dataframe is incomplete or malformed.
    """
    try:
        if len(dataframe) < 2:
            return False
        
        current_day = dataframe.iloc[-1]
        previous_day = dataframe.iloc[-2]
        
        # Check if crossover happened
        previous_short_above_long = previous_day['sma_short'] > previous_day['sma_long']
        current_short_below_long = current_day['sma_short'] < current_day['sma_long']
        
        death_cross_detected = previous_short_above_long and current_short_below_long
        return death_cross_detected
    
    except (KeyError, IndexError) as error:
        error_message = f"Error detecting death cross: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False
    
    except Exception as error:
        error_message = f"Unexpected error in death cross detection: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False


def submit_market_order(symbol, quantity, side):
    """
    Submit a market order to buy or sell with comprehensive error handling.
    WHY: This is the most critical operation - order submission can fail for many reasons.
    STRATEGY: Return None if failed, and log detailed error information.
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
        logging.info(f"Order submitted: {order.side} {order.qty} shares of {order.symbol}, ID: {order.id}")
        return order
    
    except requests.exceptions.Timeout:
        error_message = "Order submission timed out"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None
    
    except requests.exceptions.ConnectionError:
        error_message = "Network connection error during order submission"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None
    
    except Exception as error:
        error_str = str(error).lower()
        
        # Provide specific error messages for common issues
        if 'insufficient' in error_str and 'buying power' in error_str:
            error_message = "Insufficient buying power to place order"
        elif 'market is closed' in error_str or 'not open' in error_str:
            error_message = "Cannot place order - market is closed"
        elif 'symbol' in error_str and 'invalid' in error_str:
            error_message = f"Invalid symbol: {symbol}"
        else:
            error_message = f"Order submission failed: {error}"
        
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None


def close_position_safely(symbol):
    """
    Close a position with comprehensive error handling.
    WHY: Position closing is critical and can fail for multiple reasons.
    STRATEGY: Return True if successful, False if failed.
    """
    try:
        trading_client.close_position(symbol)
        print("✅ Position closed successfully!")
        logging.info(f"Position closed successfully for {symbol}")
        return True
    
    except requests.exceptions.Timeout:
        error_message = "Position close request timed out"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False
    
    except requests.exceptions.ConnectionError:
        error_message = "Network connection error during position close"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False
    
    except Exception as error:
        error_str = str(error).lower()
        
        if 'position does not exist' in error_str or 'not found' in error_str:
            # Position doesn't exist - this might actually be okay
            print("⚠️  Warning: Position already closed or doesn't exist")
            logging.warning(f"Position doesn't exist when trying to close: {symbol}")
            return True  # Treat as success since the desired state is achieved
        elif 'market is closed' in error_str:
            error_message = "Cannot close position - market is closed"
        else:
            error_message = f"Error closing position: {error}"
        
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return False


def get_account_info():
    """
    Get account information with error handling.
    WHY: Account info is useful but not critical - if it fails, bot can continue.
    STRATEGY: Return None if failed.
    """
    try:
        account = trading_client.get_account()
        return account
    
    except Exception as error:
        error_message = f"Failed to get account info: {error}"
        print(f"❌ Error: {error_message}")
        logging.error(error_message)
        return None


def run_resilient_bot():
    """
    Main function that runs a resilient trading bot with comprehensive error handling.
    WHY: This demonstrates how to build a production-ready bot that can survive failures.
    """
    print("\n" + "=" * 70)
    print("🛡️  Resilient Trading Bot Starting...")
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
    print("🛡️  This bot includes comprehensive error handling!")
    print("   It will survive temporary API failures and network issues.")
    print("=" * 70)
    
    logging.info("=" * 70)
    logging.info("Resilient Trading Bot Starting")
    logging.info(f"Symbol: {SYMBOL}, Quantity: {QUANTITY}")
    logging.info(f"Strategy: Golden Cross ({SHORT_WINDOW}/{LONG_WINDOW})")
    logging.info("=" * 70)
    
    # --- Send startup notification to Discord ---
    startup_message = (
        f"🛡️  **Resilient Bot Started**\n"
        f"```\n"
        f"Symbol: {SYMBOL}\n"
        f"Quantity: {QUANTITY} shares\n"
        f"Strategy: Golden Cross ({SHORT_WINDOW}/{LONG_WINDOW})\n"
        f"Paper Trading: {IS_PAPER_TRADING}\n"
        f"Error Handling: Enabled\n"
        f"```"
    )
    send_discord_notification(startup_message)
    
    # --- Step 1: Load saved state ---
    bot_state = load_state()
    is_in_position = bot_state.get('is_in_position', False)
    
    print(f"\n📋 Loaded State: is_in_position = {is_in_position}")
    
    # --- Step 2: Synchronize with broker (source of truth) ---
    actual_position = synchronize_state_with_broker(SYMBOL)
    
    if actual_position is None:
        # API failed - we couldn't verify position
        print("⚠️  WARNING: Could not verify position with broker due to API error")
        print("   Bot will use saved state, but this may be risky.")
        print("   Consider stopping the bot and checking your connection.")
        logging.warning("Failed to synchronize state with broker - using saved state")
        
        sync_error_message = (
            f"⚠️  **State Sync Failed**\n"
            f"```\n"
            f"Could not verify position with broker\n"
            f"Using saved state: {is_in_position}\n"
            f"This may be risky - check connection\n"
            f"```"
        )
        send_discord_notification(sync_error_message)
    
    elif actual_position != is_in_position:
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
    
    # --- Display account info if available ---
    account_info = get_account_info()
    if account_info:
        print(f"\n💰 Account Info:")
        print(f"   Portfolio Value: ${float(account_info.portfolio_value):,.2f}")
        print(f"   Buying Power: ${float(account_info.buying_power):,.2f}")
        print(f"   Cash: ${float(account_info.cash):,.2f}")
    
    print("\n🔄 Starting main loop...\n")
    
    # Track consecutive errors for circuit breaker pattern
    consecutive_errors = 0
    MAX_CONSECUTIVE_ERRORS = 5
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {current_time} ---")
            logging.info(f"--- Loop running at {current_time} ---")

            # --- Step 3: Get historical data ---
            bars = get_historical_bars(SYMBOL, days_limit=LONG_WINDOW + 2)
            
            if bars is None:
                # CRITICAL FAILURE: Cannot get market data
                print(f"⚠️  CRITICAL: Could not fetch market data.")
                print(f"   STRATEGY: Skip this cycle and try again later.")
                logging.warning("Skipping cycle due to data fetch failure")
                
                # Send notification about data fetch failure
                data_error_message = (
                    f"⚠️  **Data Fetch Failed**\n"
                    f"```\n"
                    f"Could not fetch market data for {SYMBOL}\n"
                    f"Action: Skipping this cycle\n"
                    f"Will retry in {CHECK_INTERVAL_SECONDS} seconds\n"
                    f"```"
                )
                send_discord_notification(data_error_message)
                
                # Skip this cycle
                consecutive_errors += 1
                print(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
                time.sleep(CHECK_INTERVAL_SECONDS)
                continue
            
            if len(bars) < LONG_WINDOW:
                print(f"⚠️  Not enough historical data. Need at least {LONG_WINDOW} bars, got {len(bars)}.")
                logging.warning(f"Not enough historical data: {len(bars)} bars")
                consecutive_errors += 1
                print(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
                time.sleep(CHECK_INTERVAL_SECONDS)
                continue
            
            # --- Step 4: Calculate moving averages ---
            bars_with_sma = calculate_moving_averages(bars, SHORT_WINDOW, LONG_WINDOW)
            
            if bars_with_sma is None:
                # Data processing failed
                print(f"⚠️  CRITICAL: Could not calculate moving averages.")
                print(f"   STRATEGY: Skip this cycle.")
                logging.warning("Skipping cycle due to SMA calculation failure")
                consecutive_errors += 1
                print(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
                time.sleep(CHECK_INTERVAL_SECONDS)
                continue
            
            # Get the latest values
            try:
                latest_bar = bars_with_sma.iloc[-1]
                latest_close = latest_bar['close']
                latest_sma_short = latest_bar['sma_short']
                latest_sma_long = latest_bar['sma_long']
                
                # Check for NaN values (not enough data for SMA calculation)
                if pd.isna(latest_sma_short) or pd.isna(latest_sma_long):
                    print(f"⚠️  SMA values are NaN. Need more data points.")
                    logging.warning("SMA values are NaN")
                    consecutive_errors += 1
                    print(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
                    time.sleep(CHECK_INTERVAL_SECONDS)
                    continue
                
                print(f"📊 Current Price: ${latest_close:.2f}")
                print(f"📈 SMA {SHORT_WINDOW}: ${latest_sma_short:.2f}")
                print(f"📉 SMA {LONG_WINDOW}: ${latest_sma_long:.2f}")
                print(f"📋 Current State: is_in_position = {is_in_position}")
                
            except (KeyError, IndexError) as error:
                error_message = f"Error accessing bar data: {error}"
                print(f"❌ Error: {error_message}")
                logging.error(error_message)
                consecutive_errors += 1
                print(f"💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
                time.sleep(CHECK_INTERVAL_SECONDS)
                continue
            
            # Reset consecutive errors counter on success
            consecutive_errors = 0
            
            # --- Step 5: Check for signals based on current state ---
            if not is_in_position:
                # Look for BUY signal (Golden Cross)
                signal_detected = detect_golden_cross(bars_with_sma)
                
                if signal_detected:
                    print("\n" + "=" * 70)
                    print("🎯 GOLDEN CROSS DETECTED!")
                    print("=" * 70)
                    print(f"📊 Short SMA ({SHORT_WINDOW}) crossed above Long SMA ({LONG_WINDOW})")
                    print(f"💰 Attempting to buy {QUANTITY} shares of {SYMBOL}")
                    logging.info("GOLDEN CROSS DETECTED - Attempting BUY")
                    
                    # Submit buy order
                    order = submit_market_order(SYMBOL, QUANTITY, OrderSide.BUY)
                    
                    if order:
                        # --- SUCCESS: Update and save state after successful order ---
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
                        # --- FAILURE: Order submission failed ---
                        print("❌ BUY order failed. Position NOT opened.")
                        print("   State NOT updated (still not in position).")
                        logging.error("BUY order failed - state unchanged")
                        
                        # Send error notification
                        error_message = (
                            f"❌ **BUY Order Failed**\n"
                            f"```\n"
                            f"Symbol: {SYMBOL}\n"
                            f"Quantity: {QUANTITY} shares\n"
                            f"Signal: Golden Cross detected but order failed\n"
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
                    print(f"💸 Attempting to close position on {SYMBOL}")
                    logging.info("DEATH CROSS DETECTED - Attempting SELL")
                    
                    # Close the position
                    close_success = close_position_safely(SYMBOL)
                    
                    if close_success:
                        # --- SUCCESS: Update and save state after successful close ---
                        is_in_position = False
                        bot_state['is_in_position'] = False
                        save_state(bot_state)
                        print("💾 State updated: is_in_position = False")
                        logging.info("Position closed successfully. State updated.")
                        
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
                    else:
                        # --- FAILURE: Position close failed ---
                        print("❌ Position close failed.")
                        print("   State NOT updated (still in position according to bot).")
                        print("   Manual verification recommended!")
                        logging.error("Position close failed - state unchanged")
                        
                        # Send error notification
                        error_message = (
                            f"❌ **SELL Order Failed**\n"
                            f"```\n"
                            f"Symbol: {SYMBOL}\n"
                            f"Signal: Death Cross detected but close failed\n"
                            f"Manual verification recommended!\n"
                            f"```"
                        )
                        send_discord_notification(error_message)
                else:
                    print("📊 Holding position. Monitoring for exit signal...")
                    logging.info("Holding position. No exit signal.")
            
            # --- Circuit Breaker: Check if too many errors ---
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                critical_message = (
                    f"🚨 **CRITICAL: Too Many Consecutive Errors**\n"
                    f"```\n"
                    f"Consecutive errors: {consecutive_errors}\n"
                    f"Bot will pause for 5 minutes before retrying\n"
                    f"Manual intervention may be needed\n"
                    f"```"
                )
                print(f"\n🚨 CRITICAL: {consecutive_errors} consecutive errors detected!")
                print(f"   Bot will pause for 5 minutes before retrying.")
                logging.critical(f"Circuit breaker triggered: {consecutive_errors} consecutive errors")
                send_discord_notification(critical_message)
                
                time.sleep(300)  # 5 minutes
                consecutive_errors = 0  # Reset counter after long pause
                continue
            
            # --- Step 6: Sleep before next iteration ---
            print(f"\n💤 Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n\n" + "=" * 70)
            print("🛑 Bot is shutting down. State has been saved.")
            print("   When you restart, the bot will remember its position!")
            print("=" * 70)
            logging.info("Bot shutdown by user (KeyboardInterrupt).")
            
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
            # Catch-all for any unexpected errors in the main loop
            error_message = f"Unexpected error in main loop: {error}"
            print(f"\n❌ {error_message}")
            logging.error(error_message)
            print("⚠️  Bot will retry in 60 seconds...")
            
            # Send error notification to Discord
            error_notification = (
                f"❌ **Unexpected Error in Main Loop**\n"
                f"```\n"
                f"Error: {str(error)[:200]}\n"
                f"Status: Bot will retry in 60 seconds\n"
                f"```"
            )
            send_discord_notification(error_notification)
            
            consecutive_errors += 1
            time.sleep(60)


# --- Entry Point ---
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("📚 Alpaca Trading Course - Lesson 25")
    print("📖 Making Your Bot Resilient – Handling API and Connection Errors")
    print("=" * 70)
    
    run_resilient_bot()

