Tutorial 4: Your First Trade – Placing a MARKET Order
Objective: In this tutorial, you will learn how to write a script that buys or sells a single share of a stock at the current market price using a MARKET order.

1. Prerequisites
Completed Tutorial 2: You must have a working config.py file with your API keys.

Paper Trading Account: VERY IMPORTANT! Use your Alpaca Paper Trading Account to test this script. Running it on a Live Account will execute a real trade with real money.

2. Project Setup
In your alpaca_bot_project folder, create a new file named place_order.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── hello_alpaca.py
├── fetch_data.py
└── place_order.py       # New file
3. Creating the Script (place_order.py)
Open the place_order.py file and add the following code. This script will place an order to buy one share of Apple (AAPL).

python
# place_order.py

import alpaca_trade_api as tradeapi
import config

# --- 1. Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# Check if the market is open
clock = api.get_clock()
if not clock.is_open:
    print("The market is currently closed. Cannot place orders.")
    exit() # Exit the script if the market is closed

# --- 2. Define Order Parameters ---
symbol = "AAPL"
qty = 1
side = 'buy'  # 'buy' to purchase, 'sell' to sell
type = 'market' # A market order executes at the best available price
time_in_force = 'day' # The order is valid until the end of the trading day

# --- 3. Place the Order ---
try:
    print(f"Placing a {side} order for {qty} share(s) of {symbol}...")

    # Use the 'submit_order' method to place the order
    order = api.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
    )

    # --- 4. Display Confirmation ---
    print("Order was placed successfully!")
    print(f"Order ID: {order.id}")
    print(f"Symbol: {order.symbol}")
    print(f"Quantity: {order.qty}")
    print(f"Status: {order.status}")

except Exception as e:
    print(f"An error occurred while placing the order: {e}")
4. Understanding the Code
Check Market Status: Before attempting to place an order, it's good practice to check if the market is open. api.get_clock() provides information about the current market status (open/closed) and helps avoid immediate order rejections.

Order Parameters:

symbol = "AAPL": The stock you want to trade.

qty = 1: The number of shares. This must be an integer.

side = 'buy': The side of the trade. Set to 'buy' to purchase or 'sell' to sell.

type = 'market': The order type. A market order is executed immediately at the best price currently available on the market. It's the simplest type of order.

time_in_force = 'day': Specifies how long the order should remain active if not immediately filled. 'day' means the order is valid for the current trading day only. Another popular option is 'gtc' (Good 'til Canceled).

Placing the Order (api.submit_order): This function is the core of the operation. It sends your order to the broker (Alpaca). We place it in a try...except block to handle errors, such as insufficient funds, attempting to trade outside market hours, or an error in the symbol name.

Order Confirmation:

If the order is successfully accepted by the API, the submit_order function returns an Order object.

This object contains all the details of your order, including a unique id that you can use later to check the order's status or cancel it.

The initial status of a market order will typically be accepted or pending_new, and then it will very quickly change to filled if there is liquidity in the market.