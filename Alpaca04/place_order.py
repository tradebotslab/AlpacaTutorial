# place_order.py
# Tutorial 4: Your First Trade – Placing a MARKET Order
# This script demonstrates how to place a market order to buy or sell a stock

# 1. Imports
import alpaca_trade_api as tradeapi
import config

# 2. Constants
SYMBOL = "AAPL"  # The stock symbol to trade
QUANTITY = 1  # Number of shares to buy or sell
ORDER_SIDE = 'buy'  # 'buy' to purchase shares, 'sell' to sell shares
ORDER_TYPE = 'market'  # Market order executes at the best available price immediately
TIME_IN_FORCE = 'day'  # Order is valid until the end of the current trading day

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

# 4. Helper functions
def check_market_status():
    """
    Check if the market is currently open.
    Returns True if market is open, False otherwise.
    """
    try:
        clock = api.get_clock()
        return clock.is_open
    except Exception as e:
        print(f"Error checking market status: {e}")
        return False


def place_market_order(symbol, quantity, side, order_type, time_in_force):
    """
    Place a market order for the specified stock.
    
    Args:
        symbol: Stock symbol (e.g., "AAPL")
        quantity: Number of shares to trade
        side: 'buy' or 'sell'
        order_type: Type of order (e.g., 'market')
        time_in_force: How long the order should remain active (e.g., 'day')
    
    Returns:
        Order object if successful, None otherwise
    """
    try:
        print(f"Placing a {side} order for {quantity} share(s) of {symbol}...")
        
        # Use the 'submit_order' method to place the order
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        
        return order
    except Exception as e:
        print(f"An error occurred while placing the order: {e}")
        return None


def display_order_confirmation(order):
    """
    Display confirmation details of a successfully placed order.
    
    Args:
        order: Order object returned from submit_order
    """
    if order:
        print("Order was placed successfully!")
        print(f"Order ID: {order.id}")
        print(f"Symbol: {order.symbol}")
        print(f"Quantity: {order.qty}")
        print(f"Status: {order.status}")


# 5. Main logic
def main():
    """
    Main function that orchestrates the order placement process.
    Checks market status, places order, and displays confirmation.
    """
    # Check if the market is open before attempting to place an order
    # This prevents immediate order rejections when market is closed
    is_market_open = check_market_status()
    
    if not is_market_open:
        print("The market is currently closed. Cannot place orders.")
        return
    
    # Place the market order with the defined parameters
    order = place_market_order(
        symbol=SYMBOL,
        quantity=QUANTITY,
        side=ORDER_SIDE,
        order_type=ORDER_TYPE,
        time_in_force=TIME_IN_FORCE
    )
    
    # Display confirmation if order was placed successfully
    display_order_confirmation(order)


# 6. Run
if __name__ == "__main__":
    main()
