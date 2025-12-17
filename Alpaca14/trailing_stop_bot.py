# 1. Imports
import alpaca_trade_api as tradeapi
import config
import time
from datetime import datetime

# 2. Constants
SYMBOL = "SPY"
TRAIL_PERCENT = 5.0  # 5% trailing stop-loss
CHECK_INTERVAL_SECONDS = 60  # Check every 60 seconds

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

# 4. Helper functions
def get_account_info():
    """
    Fetches and displays current account information.
    Returns the account object for further use.
    """
    try:
        account = api.get_account()
        print(f"\n=== Account Information ===")
        print(f"Account Status: {account.status}")
        print(f"Buying Power: ${float(account.buying_power):.2f}")
        print(f"Cash: ${float(account.cash):.2f}")
        print(f"Portfolio Value: ${float(account.portfolio_value):.2f}")
        return account
    except Exception as e:
        print(f"Error fetching account info: {e}")
        return None


def get_current_price(symbol):
    """
    Retrieves the current price for a given symbol.
    Uses the last trade price from the latest bar.
    """
    try:
        barset = api.get_bars(symbol, tradeapi.TimeFrame.Minute, limit=1)
        if barset and len(barset) > 0:
            current_price = barset[0].c  # Closing price of the last bar
            return current_price
        else:
            print(f"No data available for {symbol}")
            return None
    except Exception as e:
        print(f"Error getting current price for {symbol}: {e}")
        return None


def check_existing_position(symbol):
    """
    Checks if we already have an open position for the given symbol.
    Returns the position object if found, None otherwise.
    """
    try:
        positions = api.list_positions()
        for position in positions:
            if position.symbol == symbol:
                return position
        return None
    except Exception as e:
        print(f"Error checking positions: {e}")
        return None


def place_order_with_trailing_stop(symbol, qty, trail_percent):
    """
    Places a market buy order with a trailing stop-loss.
    
    The trailing stop automatically moves up as the price increases,
    protecting profits while giving the trade room to grow.
    
    Parameters:
    - symbol: Stock symbol to trade
    - qty: Number of shares to buy
    - trail_percent: Trailing stop percentage (e.g., 5.0 for 5%)
    """
    try:
        # Submit market order with trailing stop
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc',  # Good 'til canceled - order stays active
            order_class='oto',    # One-Triggers-Other - trailing stop activates after buy fills
            take_profit=dict(
                limit_price=None  # We're not using take profit in this tutorial
            ) if False else None,  # Placeholder for future tutorials
            stop_loss=dict(
                stop_price=None,
                trail_percent=trail_percent  # This is the key parameter!
            )
        )
        
        print(f"\n✅ Order placed successfully!")
        print(f"Order ID: {order.id}")
        print(f"Symbol: {order.symbol}")
        print(f"Quantity: {order.qty}")
        print(f"Side: {order.side}")
        print(f"Type: {order.type}")
        print(f"Trailing Stop: {trail_percent}%")
        
        return order
    except Exception as e:
        print(f"❌ Error placing order: {e}")
        return None


def monitor_position(symbol):
    """
    Monitors the current position and displays relevant information.
    Shows current price, entry price, profit/loss, and trailing stop status.
    """
    try:
        position = check_existing_position(symbol)
        
        if not position:
            print(f"\n📊 No position found for {symbol}")
            return False
        
        # Get current price
        current_price = get_current_price(symbol)
        if not current_price:
            return True
        
        # Calculate profit/loss
        entry_price = float(position.avg_entry_price)
        current_value = float(position.market_value)
        unrealized_pl = float(position.unrealized_pl)
        unrealized_pl_percent = float(position.unrealized_plpc) * 100
        
        # Display position information
        print(f"\n=== Position Status for {symbol} ===")
        print(f"Quantity: {position.qty} shares")
        print(f"Entry Price: ${entry_price:.2f}")
        print(f"Current Price: ${current_price:.2f}")
        print(f"Current Value: ${current_value:.2f}")
        print(f"Unrealized P/L: ${unrealized_pl:.2f} ({unrealized_pl_percent:.2f}%)")
        
        # Calculate where the trailing stop is (approximately)
        # Note: The actual trailing stop is managed by Alpaca and moves automatically
        trailing_stop_price = current_price * (1 - TRAIL_PERCENT / 100)
        print(f"Approximate Trailing Stop: ${trailing_stop_price:.2f}")
        print(f"(Actual stop is managed automatically by Alpaca)")
        
        return True
    except Exception as e:
        print(f"Error monitoring position: {e}")
        return False


# 5. Main logic
def main():
    """
    Main trading bot logic:
    1. Check account status
    2. Check if we already have a position
    3. If no position, place an order with trailing stop
    4. If position exists, monitor it
    """
    print("=" * 50)
    print("🚀 Trailing Stop-Loss Bot Starting...")
    print("=" * 50)
    
    # Get account information
    account = get_account_info()
    if not account:
        print("❌ Cannot proceed without account information")
        return
    
    # Check if we already have a position
    existing_position = check_existing_position(SYMBOL)
    
    if existing_position:
        print(f"\n📌 You already have a position in {SYMBOL}")
        print(f"Shares: {existing_position.qty}")
        print(f"Entry Price: ${float(existing_position.avg_entry_price):.2f}")
        print(f"Current Value: ${float(existing_position.market_value):.2f}")
        print(f"\n🔄 Entering monitoring mode...")
        
        # Monitor the position
        while True:
            still_open = monitor_position(SYMBOL)
            if not still_open:
                print(f"\n✅ Position closed (trailing stop triggered or manually closed)")
                break
            
            print(f"\n⏳ Waiting {CHECK_INTERVAL_SECONDS} seconds before next check...")
            time.sleep(CHECK_INTERVAL_SECONDS)
    else:
        print(f"\n📊 No existing position in {SYMBOL}")
        
        # Get current price for reference
        current_price = get_current_price(SYMBOL)
        if not current_price:
            print("❌ Cannot get current price")
            return
        
        print(f"Current Price: ${current_price:.2f}")
        
        # Calculate how many shares we can buy with available cash
        # Using 90% of available cash for safety
        available_cash = float(account.cash) * 0.9
        shares_to_buy = int(available_cash / current_price)
        
        if shares_to_buy < 1:
            print(f"❌ Insufficient funds to buy {SYMBOL}")
            print(f"Available: ${available_cash:.2f}, Price: ${current_price:.2f}")
            return
        
        print(f"\n💡 Planning to buy {shares_to_buy} shares at ~${current_price:.2f}")
        print(f"With {TRAIL_PERCENT}% trailing stop-loss")
        
        # Calculate initial stop-loss price
        initial_stop_price = current_price * (1 - TRAIL_PERCENT / 100)
        print(f"Initial Stop Price: ${initial_stop_price:.2f}")
        print(f"(This will automatically move up as price increases)")
        
        # Place the order
        print(f"\n📤 Placing order...")
        order = place_order_with_trailing_stop(SYMBOL, shares_to_buy, TRAIL_PERCENT)
        
        if order:
            print(f"\n✅ Order submitted successfully!")
            print(f"\n📋 What happens next:")
            print(f"1. Order fills at market price")
            print(f"2. Trailing stop activates automatically")
            print(f"3. As price rises, stop moves up with it")
            print(f"4. If price falls {TRAIL_PERCENT}% from highest point, position closes")
            print(f"\n🔄 Entering monitoring mode...")
            
            # Wait for order to fill
            time.sleep(5)
            
            # Monitor the position
            while True:
                still_open = monitor_position(SYMBOL)
                if not still_open:
                    print(f"\n✅ Position closed (trailing stop triggered or manually closed)")
                    break
                
                print(f"\n⏳ Waiting {CHECK_INTERVAL_SECONDS} seconds before next check...")
                time.sleep(CHECK_INTERVAL_SECONDS)


# 6. Run
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

