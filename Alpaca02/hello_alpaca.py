# hello_alpaca.py
# Tutorial 2: "Hello, Alpaca!" - Connect & Check Your Account Status

# 1. Imports
import alpaca_trade_api as tradeapi
import config

# 2. Constants
# No additional constants needed for this basic connection script

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)


# 4. Helper functions
def get_account_info(api_connection):
    """
    Retrieves and returns the account information from Alpaca.
    
    Args:
        api_connection: The initialized Alpaca REST API connection object
    
    Returns:
        Account object containing information like equity, buying power, etc.
    """
    # We use try-except to handle potential connection errors gracefully
    # This prevents the script from crashing if there's a network issue or invalid API keys
    try:
        account = api_connection.get_account()
        return account
    except Exception as error:
        # Print the error so the user knows what went wrong
        print(f"Error connecting to Alpaca API: {error}")
        return None


def display_account_summary(account):
    """
    Prints a formatted summary of the account information to the console.
    
    Args:
        account: The account object returned from the Alpaca API
    """
    if account is None:
        print("Cannot display account summary - account information not available.")
        return
    
    # We print each piece of information on a separate line for clarity
    # This makes it easy to see all the account details at a glance
    print("\n" + "="*50)
    print("ACCOUNT SUMMARY")
    print("="*50)
    print(f"Account Status: {account.status}")
    print(f"Current Equity: ${float(account.equity):,.2f}")
    print(f"Buying Power: ${float(account.buying_power):,.2f}")
    print(f"Cash: ${float(account.cash):,.2f}")
    print(f"Portfolio Value: ${float(account.portfolio_value):,.2f}")
    print("="*50 + "\n")


# 5. Main logic
def main():
    """
    Main function that orchestrates the connection to Alpaca and displays account information.
    This is where the script's primary logic lives.
    """
    print("Connecting to Alpaca API...")
    
    # Get the account information from Alpaca
    account = get_account_info(api)
    
    # Display the account summary if we successfully retrieved it
    if account is not None:
        display_account_summary(account)
        print("Successfully connected to Alpaca! Your account information is shown above.")
    else:
        print("Failed to connect to Alpaca. Please check your API keys in config.py and your internet connection.")


# 6. Run
if __name__ == "__main__":
    main()
