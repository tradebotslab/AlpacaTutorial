"""
Lesson 21: Logging Bot - Creating a "Black Box" for Your Trading Bot

This script demonstrates how to implement comprehensive logging in a trading bot.
Every decision, action, and error is recorded to a log file for later analysis.

Author: Alpaca Trading Course
Lesson: 21 - The Bot's "Black Box" – Logging Every Decision to a File
"""

# 1. Imports
import logging
from logging.handlers import RotatingFileHandler
import alpaca_trade_api as tradeapi
import config
import time
from datetime import datetime

# 2. Constants
SYMBOL = "AAPL"
TRADE_QUANTITY = 1
CHECK_INTERVAL_SECONDS = 60
MAX_LOG_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_LOG_COUNT = 3


# 3. Configure Logging
def setup_logging():
    """
    Configure the logging system with both file and console output.
    Uses RotatingFileHandler to prevent log files from growing too large.
    
    WHY: Rotating logs prevent disk space issues in long-running bots.
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        'trading_bot.log',
        maxBytes=MAX_LOG_FILE_SIZE,
        backupCount=BACKUP_LOG_COUNT
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler for real-time monitoring
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(detailed_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info("=" * 70)
    logging.info("LOGGING SYSTEM INITIALIZED")
    logging.info("=" * 70)


# 4. API Connection
def initialize_api():
    """
    Initialize connection to Alpaca API.
    
    WHY: Separating initialization allows for better error handling and logging.
    """
    try:
        api = tradeapi.REST(
            config.API_KEY,
            config.SECRET_KEY,
            base_url=config.BASE_URL
        )
        logging.info("Successfully connected to Alpaca API")
        
        # Log account information
        account = api.get_account()
        logging.info(f"Account Status: {account.status}")
        logging.info(f"Buying Power: ${float(account.buying_power):,.2f}")
        logging.info(f"Portfolio Value: ${float(account.portfolio_value):,.2f}")
        
        return api
    except Exception as error:
        logging.critical(f"Failed to initialize Alpaca API: {error}")
        raise


# 5. Helper Functions
def get_current_position(api, symbol):
    """
    Check if we currently have a position in the given symbol.
    
    WHY: Need to know position status before making trading decisions.
    """
    try:
        position = api.get_position(symbol)
        quantity = int(position.qty)
        logging.debug(f"Current position in {symbol}: {quantity} shares")
        return quantity
    except Exception as error:
        # WHY: Position not found is normal (not an error), just means we have no position
        if "position does not exist" in str(error).lower():
            logging.debug(f"No current position in {symbol}")
            return 0
        else:
            logging.error(f"Error checking position for {symbol}: {error}")
            return 0


def get_latest_price(api, symbol):
    """
    Get the latest price for a symbol.
    
    WHY: Price information is needed for trading decisions and logging.
    """
    try:
        barset = api.get_barset(symbol, 'minute', limit=1)
        latest_bar = barset[symbol][0]
        latest_price = latest_bar.c
        logging.debug(f"Latest price for {symbol}: ${latest_price:.2f}")
        return latest_price
    except Exception as error:
        logging.error(f"Error getting price for {symbol}: {error}")
        return None


def make_trade_decision(api, symbol):
    """
    Simple trading logic that demonstrates different logging levels.
    
    In a real bot, this would include your actual trading strategy.
    For demonstration, this uses a simple time-based logic.
    
    WHY: This function shows how to log decisions at different severity levels.
    """
    current_hour = datetime.now().hour
    current_position = get_current_position(api, symbol)
    latest_price = get_latest_price(api, symbol)
    
    if latest_price is None:
        logging.warning(f"Cannot make decision for {symbol} - price unavailable")
        return
    
    # Simple logic: Buy in morning hours, sell in afternoon, hold otherwise
    # WHY: This is just for demonstration - replace with your actual strategy
    if current_hour >= 10 and current_hour < 12 and current_position == 0:
        decision = "BUY"
        logging.info(f"DECISION: {decision} {symbol} at ${latest_price:.2f} (Morning buying window)")
        execute_buy_order(api, symbol, TRADE_QUANTITY, latest_price)
    elif current_hour >= 14 and current_hour < 16 and current_position > 0:
        decision = "SELL"
        logging.info(f"DECISION: {decision} {symbol} at ${latest_price:.2f} (Afternoon selling window)")
        execute_sell_order(api, symbol, current_position, latest_price)
    else:
        decision = "HOLD"
        logging.debug(f"DECISION: {decision} {symbol} at ${latest_price:.2f} (Outside trading window)")


def execute_buy_order(api, symbol, quantity, price):
    """
    Execute a buy order and log all details.
    
    WHY: Comprehensive logging of order execution is crucial for audit trail.
    """
    try:
        logging.info(f"Attempting to BUY {quantity} shares of {symbol} at ${price:.2f}")
        
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='day'
        )
        
        logging.info(f"✓ BUY ORDER SUBMITTED - Order ID: {order.id}")
        logging.info(f"  Symbol: {symbol}")
        logging.info(f"  Quantity: {quantity}")
        logging.info(f"  Type: Market Order")
        logging.info(f"  Status: {order.status}")
        
        # Wait a moment and check order status
        time.sleep(2)
        updated_order = api.get_order(order.id)
        logging.info(f"  Order Status Update: {updated_order.status}")
        
        if updated_order.filled_at:
            filled_price = float(updated_order.filled_avg_price)
            logging.info(f"  Filled at: ${filled_price:.2f}")
            
    except Exception as error:
        logging.error(f"✗ FAILED to submit BUY order for {symbol}: {error}")
        logging.error(f"  Attempted quantity: {quantity}")
        logging.error(f"  Target price: ${price:.2f}")


def execute_sell_order(api, symbol, quantity, price):
    """
    Execute a sell order and log all details.
    
    WHY: Comprehensive logging of order execution is crucial for audit trail.
    """
    try:
        logging.info(f"Attempting to SELL {quantity} shares of {symbol} at ${price:.2f}")
        
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='day'
        )
        
        logging.info(f"✓ SELL ORDER SUBMITTED - Order ID: {order.id}")
        logging.info(f"  Symbol: {symbol}")
        logging.info(f"  Quantity: {quantity}")
        logging.info(f"  Type: Market Order")
        logging.info(f"  Status: {order.status}")
        
        # Wait a moment and check order status
        time.sleep(2)
        updated_order = api.get_order(order.id)
        logging.info(f"  Order Status Update: {updated_order.status}")
        
        if updated_order.filled_at:
            filled_price = float(updated_order.filled_avg_price)
            logging.info(f"  Filled at: ${filled_price:.2f}")
            
    except Exception as error:
        logging.error(f"✗ FAILED to submit SELL order for {symbol}: {error}")
        logging.error(f"  Attempted quantity: {quantity}")
        logging.error(f"  Target price: ${price:.2f}")


def log_market_status(api):
    """
    Log current market status.
    
    WHY: Knowing market hours helps debug why trades aren't executing.
    """
    try:
        clock = api.get_clock()
        if clock.is_open:
            logging.info("Market is OPEN")
        else:
            logging.info("Market is CLOSED")
            logging.info(f"Next market open: {clock.next_open}")
    except Exception as error:
        logging.error(f"Error checking market status: {error}")


# 6. Main Function
def main():
    """
    Main bot loop with comprehensive logging.
    
    WHY: The main loop orchestrates all bot activities and ensures they're logged.
    """
    # Initialize logging first
    setup_logging()
    
    logging.info("Starting Logging Bot - Lesson 21")
    logging.info(f"Monitoring symbol: {SYMBOL}")
    logging.info(f"Check interval: {CHECK_INTERVAL_SECONDS} seconds")
    
    # Initialize API connection
    try:
        api = initialize_api()
    except Exception as error:
        logging.critical("Cannot continue without API connection. Exiting.")
        return
    
    # Log initial market status
    log_market_status(api)
    
    # Main bot loop
    iteration_count = 0
    try:
        while True:
            iteration_count += 1
            logging.info("-" * 70)
            logging.info(f"ITERATION {iteration_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            logging.info("-" * 70)
            
            try:
                # Check market status
                clock = api.get_clock()
                
                if clock.is_open:
                    # Make trading decision
                    make_trade_decision(api, SYMBOL)
                else:
                    logging.info("Market is closed - skipping trading logic")
                    logging.debug(f"Next market open: {clock.next_open}")
            
            except Exception as error:
                logging.error(f"Error in main loop iteration {iteration_count}: {error}")
                logging.exception("Full exception details:")
            
            # Wait before next iteration
            logging.debug(f"Sleeping for {CHECK_INTERVAL_SECONDS} seconds...")
            time.sleep(CHECK_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        logging.info("=" * 70)
        logging.info("Bot stopped by user (Ctrl+C)")
        logging.info(f"Total iterations completed: {iteration_count}")
        logging.info("=" * 70)
    except Exception as error:
        logging.critical(f"Unexpected error in main loop: {error}")
        logging.exception("Full exception details:")
    finally:
        logging.info("Logging Bot shutdown complete")


# 7. Run
if __name__ == "__main__":
    main()

