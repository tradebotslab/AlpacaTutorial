Tutorial 15: Implementing a Trailing Stop-Loss in Code
Objective: This is an advanced tutorial that shows you how to build your own trailing stop-loss mechanism from scratch. Instead of using the broker's built-in trailing stop, you will write the code to manually monitor your trade and adjust a standard stop-loss order upwards as the price moves in your favor.

1. Why Manually Implement a Trailing Stop?
While using the broker's native 'trailing_stop' order class is simpler and more reliable, manually implementing the logic can offer more flexibility and control. For example, you could create a trailing stop that moves based on a moving average or another indicator, not just price.

This tutorial is a valuable exercise in understanding the mechanics of order management and what happens "under the hood."

The Manual Logic:

Enter a trade with a standard market order.

Immediately place a separate, standard stop order and save its ID.

In the main loop, if the position is profitable, check if the stop-loss can be moved up.

If it can, cancel the old stop order and submit a new one at the higher price level.

Repeat this process, ratcheting the stop-loss up to protect profits.

2. The Challenge: Managing State
This is more complex because the bot now needs to manage its "state." It must remember the ID of its active stop-loss order to be able to modify it. If the bot restarts, this state is lost. For this tutorial, we will store the ID in a simple variable while the bot is running.

3. Creating the Script (manual_trail_bot.py)
This script requires significant new logic for order management.

python
# manual_trail_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 10
TRAIL_PERCENTAGE = 3.0 # The trailing stop will be 3% below the high price
LOOP_SLEEP_SECONDS = 30 # Check the price every 30 seconds

# --- State Management ---
# We need to store the ID of our active stop-loss order
active_stop_order_id = None

def run_manual_trail_bot():
    """The main function for the manual trailing stop bot."""
    global active_stop_order_id
    print("🚀 Manual Trailing Stop Bot is starting...")
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. Check if we have a position ---
            try:
                position = api.get_position(SYMBOL_TO_TRADE)
                print(f"✅ Position exists: {position.qty} shares.")
                
                # --- 2. MANAGE THE TRAILING STOP ---
                if active_stop_order_id is None:
                    print("⚠️ Position exists but no stop order ID. This shouldn't happen. Waiting for next loop.")
                    time.sleep(LOOP_SLEEP_SECONDS)
                    continue

                # Get the current highest price and our existing stop order
                last_price = api.get_latest_trade(SYMBOL_TO_TRADE).price
                existing_stop_order = api.get_order(active_stop_order_id)
                existing_stop_price = float(existing_stop_order.stop_price)

                # Calculate the new potential stop price
                new_stop_price = round(last_price * (1 - TRAIL_PERCENTAGE / 100), 2)

                # If the new stop price is higher, we adjust it upwards
                if new_stop_price > existing_stop_price:
                    print(f"📈 Adjusting stop-loss upwards to ${new_stop_price}")
                    # Cancel the old order and submit a new one
                    api.replace_order(
                        order_id=active_stop_order_id,
                        stop_price=new_stop_price
                    )
                    # The replace_order method returns the new order object, so we don't need to re-save the ID
                    print("✅ Stop-loss successfully replaced.")
                else:
                    print(f"ℹ️ Price has not moved up enough. Current stop remains at ${existing_stop_price}")

            except Exception:
                # No position exists
                print("ℹ️ No position held. Analyzing for entry signal...")
                active_stop_order_id = None # Ensure state is clean

                # --- 3. CHECK FOR ENTRY SIGNAL ---
                barset = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Day, limit=51, adjustment='raw')
                df = barset.df
                df['sma_20'] = df['close'].rolling(window=20).mean()
                df['sma_50'] = df['close'].rolling(window=50).mean()
                current_day = df.iloc[-1]
                previous_day = df.iloc[-2]

                if previous_day['sma_20'] < previous_day['sma_50'] and current_day['sma_20'] > current_day['sma_50']:
                    print("📈 Golden Cross Detected! Placing BUY order.")
                    buy_order = api.submit_order(symbol=SYMBOL_TO_TRADE, qty=QTY_PER_TRADE, side='buy', type='market', time_in_force='day')
                    
                    # --- 4. PLACE INITIAL STOP-LOSS ---
                    print("Waiting 5 seconds for buy order to fill...")
                    time.sleep(5)
                    
                    entry_price = api.get_position(SYMBOL_TO_TRADE).avg_entry_price
                    initial_stop_price = round(float(entry_price) * (1 - TRAIL_PERCENTAGE / 100), 2)
                    
                    print(f"Placing initial stop-loss at ${initial_stop_price}")
                    stop_order = api.submit_order(
                        symbol=SYMBOL_TO_TRADE,
                        qty=QTY_PER_TRADE,
                        side='sell',
                        type='stop', # This is a standard stop order, not a trailing stop
                        time_in_force='gtc', # Good 'til Canceled
                        stop_price=initial_stop_price
                    )
                    active_stop_order_id = stop_order.id # Save the ID for future loops
                    print(f"✅ Initial stop-loss order placed with ID: {active_stop_order_id}")

            # --- Sleep until the next loop ---
            time.sleep(LOOP_SLEEP_SECONDS)

        except KeyboardInterrupt:
            print("\n🛑 Bot shutting down...")
            if active_stop_order_id:
                print("Canceling active stop-loss order...")
                api.cancel_order(active_stop_order_id)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            active_stop_order_id = None
            time.sleep(60)

if __name__ == '__main__':
    run_manual_trail_bot()
4. Understanding the Code
State Management (active_stop_order_id): We use a global variable to store the ID of our stop-loss order. When we have a position, this variable is our key to finding and modifying the correct order. When the position is closed, we reset it to None.

Managing the Trail (if new_stop_price > ...): This is the core logic. In each loop where we have a position, we calculate a potential new stop price based on the current market price. We only act if this new price is higher than our existing stop price. This ensures the stop only moves up.

Replacing the Order (api.replace_order): Instead of manually canceling and then submitting, the Alpaca API provides a convenient replace_order method. This atomically replaces an existing order with a new one. Here, we use it to change just the stop_price of our existing stop-loss order to the new, higher value.

Placing the Initial Stop (api.submit_order(type='stop')): After the bot buys shares, it immediately submits a separate sell order with type='stop'. This is our initial safety net. We immediately save its ID to our active_stop_order_id variable so the next loop can begin monitoring it. We use 'gtc' (Good 'til Canceled) so it doesn't expire at the end of the day.

Shutdown (KeyboardInterrupt): It's crucial to handle shutdown gracefully. If you stop the bot with Ctrl+C, it now attempts to cancel any active stop-loss order so you aren't left with an orphaned order in your account.

⚠️ Important Considerations
Complexity and Risk: This manual approach is significantly more complex and has more potential points of failure than using a native, broker-side trailing stop. Network issues, API errors, or bugs in your code could lead to your stop-loss not being updated correctly.

Statelessness: If this bot script stops and restarts, it will lose the active_stop_order_id and will not be able to manage the existing trade. A production-grade bot would need a database or file to persist its state.

Educational Purpose: This tutorial is a powerful demonstration of order management concepts. For most real-world use cases, the native 'trailing_stop' order class is the safer and more reliable choice.