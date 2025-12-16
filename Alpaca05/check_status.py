# check_status.py
# Tutorial 5: What Happened to My Order? – Checking Status & Positions
# This script demonstrates how to check order status and view current positions

# 1. Imports
import alpaca_trade_api as tradeapi
import config
import logging

# Configure logging to help track errors and important events
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 2. Constants
# Order statuses we can filter by: 'open', 'closed', 'all'
ORDER_STATUS_FILTER = 'open'

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL)

# 4. Helper functions
def display_open_orders():
    """
    Retrieves and displays all open orders from the account.
    This helps you see which orders are still pending execution.
    """
    try:
        orders = api.list_orders(status=ORDER_STATUS_FILTER)
        print("--- Open Orders ---")
        if not orders:
            print("You have no open orders.")
        else:
            for order in orders:
                print(f"ID: {order.id}, Symbol: {order.symbol}, Qty: {order.qty}, Side: {order.side}, Status: {order.status}")
        return orders
    except Exception as e:
        logging.error(f"Failed to retrieve open orders: {e}")
        print(f"An error occurred while retrieving orders: {e}")
        return []


def check_specific_order(order_id):
    """
    Checks the status of a specific order by its ID.
    This is useful when you want to verify if a particular order was filled.
    
    Args:
        order_id: The unique identifier of the order to check
    """
    print("\n--- Checking a Specific Order ---")
    try:
        specific_order = api.get_order(order_id)
        print(f"Status of order {specific_order.id}: {specific_order.status}")
        if specific_order.status == 'filled':
            print(f"Filled at price: {specific_order.filled_avg_price} for {specific_order.filled_qty} shares.")
        return specific_order
    except Exception as e:
        logging.error(f"Failed to check specific order {order_id}: {e}")
        print(f"Could not check specific order. Error: {e}")
        print("Please make sure you have a valid Order ID.")
        return None


def display_current_positions():
    """
    Retrieves and displays all current open positions.
    A position represents stock you currently own after a buy order has been filled.
    """
    try:
        positions = api.list_positions()
        print("\n--- Current Positions ---")
        if not positions:
            print("You have no open positions.")
        else:
            for position in positions:
                print(f"Symbol: {position.symbol}, Qty: {position.qty}, Entry Price: {position.avg_entry_price}, Current Price: {position.current_price}")
        return positions
    except Exception as e:
        logging.error(f"Failed to retrieve positions: {e}")
        print(f"An error occurred while retrieving positions: {e}")
        return []


# 5. Main logic
def main():
    """
    Main function that orchestrates checking order status and positions.
    This follows the workflow: Check orders -> Check specific order (optional) -> Check positions
    """
    try:
        # Get a list of all open orders
        # This shows orders that haven't been filled or canceled yet
        open_orders = display_open_orders()
        
        # Check a specific order by its ID
        # NOTE: Replace 'YOUR_ORDER_ID_HERE' with an actual Order ID from place_order.py output
        # If you don't have one, you can comment out this section
        order_id_to_check = "YOUR_ORDER_ID_HERE"
        if order_id_to_check != "YOUR_ORDER_ID_HERE":
            check_specific_order(order_id_to_check)
        else:
            print("\n--- Skipping Specific Order Check ---")
            print("To check a specific order, replace 'YOUR_ORDER_ID_HERE' with an actual Order ID.")
        
        # Get a list of all current positions
        # Positions are created after buy orders are filled
        current_positions = display_current_positions()
        
        logging.info("Status check completed successfully")
        
    except Exception as e:
        logging.error(f"An error occurred in main: {e}")
        print(f"An error occurred: {e}")


# 6. Run
if __name__ == "__main__":
    main()
