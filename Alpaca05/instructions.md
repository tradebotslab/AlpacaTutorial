utorial 5: What Happened to My Order? – Checking Status & Positions
Objective: In this tutorial, you will learn how to check the status of your submitted orders to confirm if they have been filled and how to view your current open positions.

1. Prerequisites
Completed Tutorial 4: You should have already run the place_order.py script to submit an order.

An Order ID: Have an Order ID ready from the output of the place_order.py script.

Paper Trading Account: This script should be run against your Paper Trading account where the order was placed.

2. Project Setup
In your alpaca_bot_project folder, create a new file named check_status.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── hello_alpaca.py
├── fetch_data.py
├── place_order.py
└── check_status.py      # New file
3. Creating the Script (check_status.py)
Open the check_status.py file and add the following code. This script will retrieve all your recent orders and list your current account positions.

python
# check_status.py

import alpaca_trade_api as tradeapi
import config

# --- 1. Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

try:
    # --- 2. Get a list of all open orders ---
    orders = api.list_orders(
        status='open' # You can filter by 'open', 'closed', 'all'
    )
    print("--- Open Orders ---")
    if not orders:
        print("You have no open orders.")
    else:
        for order in orders:
            print(f"ID: {order.id}, Symbol: {order.symbol}, Qty: {order.qty}, Side: {order.side}, Status: {order.status}")

    # --- 3. Check a specific order by its ID ---
    # Replace 'YOUR_ORDER_ID_HERE' with an actual ID from a previous trade
    # For example: order_id = "a1b2c3d4-e5f6-a7b8-c9d0-e1f2a3b4c5d6"
    # If you don't have one, you can comment out this section
    print("\n--- Checking a Specific Order ---")
    try:
        # NOTE: You need to replace this with a real Order ID
        order_id_to_check = "YOUR_ORDER_ID_HERE"
        specific_order = api.get_order(order_id_to_check)
        print(f"Status of order {specific_order.id}: {specific_order.status}")
        if specific_order.status == 'filled':
            print(f"Filled at price: {specific_order.filled_avg_price} for {specific_order.filled_qty} shares.")
    except Exception as e:
        print(f"Could not check specific order. Error: {e}")
        print("Please replace 'YOUR_ORDER_ID_HERE' with a valid ID.")


    # --- 4. Get a list of all current positions ---
    positions = api.list_positions()
    print("\n--- Current Positions ---")
    if not positions:
        print("You have no open positions.")
    else:
        for position in positions:
            print(f"Symbol: {position.symbol}, Qty: {position.qty}, Entry Price: {position.avg_entry_price}, Current Price: {position.current_price}")

except Exception as e:
    print(f"An error occurred: {e}")
4. Understanding the Code
Authentication: As always, we start by connecting to the Alpaca API.

Listing Orders (api.list_orders):

This function retrieves a list of your orders.

You can filter the orders by their status. Common filters are 'open' (for orders that have not yet been filled or canceled), 'closed' (for filled, canceled, or rejected orders), and 'all'.

The script iterates through any open orders and prints their key details. An order with a status of filled means the trade was executed successfully.

Checking a Specific Order (api.get_order):

When you place an order, the API gives you a unique id. Using api.get_order(order_id) is the most direct way to track what happened to a specific transaction.

This section of the script is a template. You must replace 'YOUR_ORDER_ID_HERE' with an actual ID you received from running place_order.py.

If the order's status is 'filled', the Order object will also contain useful information like filled_avg_price and filled_qty.

Listing Positions (api.list_positions):

This function shows you all the assets you currently own.

A position is created after a buy order is filled. It represents your holding in a particular stock. If you sell all shares of a stock, that position will be closed and will no longer appear in this list.

The script iterates through your positions and prints details like the symbol, quantity, your average entry price, and the current market price.

The Order-to-Position Workflow
The process you've now automated follows a clear path:

Submit Order: You run place_order.py to submit a buy order. The API returns an Order object with a unique ID and a status like accepted.

Order Fills: The exchange processes your order, and its status changes to filled.

Check Status: You run check_status.py to confirm the order was filled.

Position Opens: Once the order is filled, api.list_positions() will show your new holding as an open position.

