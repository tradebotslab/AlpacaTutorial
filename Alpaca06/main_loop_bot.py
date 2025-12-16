# main_loop_bot.py

# 1. Imports
import alpaca_trade_api as tradeapi
import config
import time
from datetime import datetime

# 2. Constants
# Sleep interval between loop iterations in seconds
# We use 60 seconds to avoid rate limiting the Alpaca API
LOOP_INTERVAL_SECONDS = 60
# Sleep interval when an error occurs (shorter to retry sooner)
ERROR_RETRY_INTERVAL_SECONDS = 30

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

# 4. Helper functions
def get_account_status():
    """
    Fetches the current account status from Alpaca API.
    Returns the account object containing buying power and status.
    """
    account = api.get_account()
    return account

def format_timestamp():
    """
    Creates a formatted timestamp string for logging.
    Returns the current date and time in readable format.
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

# 5. Main logic
def main():
    """
    The main function that runs the trading bot's infinite loop.
    The bot wakes up at regular intervals, checks account status,
    and sleeps until the next iteration.
    """
    print("Bot is starting...")
    
    # The Main Loop - runs forever until stopped
    while True:
        try:
            # Get current timestamp for logging purposes
            current_timestamp = format_timestamp()
            print(f"\n--- Loop running at {current_timestamp} ---")
            
            # Fetch account information from Alpaca API
            # In a real trading bot, this would also include:
            # - Fetching market data
            # - Running technical analysis
            # - Checking for trade signals
            # - Placing orders if conditions are met
            account = get_account_status()
            
            # Display account information
            print(f"Account Status: {account.status}")
            print(f"Buying Power: ${account.buying_power}")
            
            # Sleep to prevent overwhelming the API and avoid rate limiting
            # Without this sleep, the loop would run thousands of times per second
            print(f"Action complete. Sleeping for {LOOP_INTERVAL_SECONDS} seconds...")
            time.sleep(LOOP_INTERVAL_SECONDS)
            
        except Exception as error:
            # If any error occurs, log it and continue the loop
            # This ensures the bot keeps running even if one iteration fails
            print(f"An error occurred: {error}")
            print("Continuing...")
            # Wait a shorter time before retrying after an error
            time.sleep(ERROR_RETRY_INTERVAL_SECONDS)

# 6. Run
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle graceful shutdown when user presses Ctrl+C
        # This prevents the program from crashing with an error message
        print("\nBot is shutting down. Goodbye!")

