Lesson 25: Making Your Bot Resilient – Handling API and Connection Errors
Welcome to Lesson 25. Your bot can now trade, log, configure, remember its state, and send notifications. But what happens when the internet hiccups? Or when the Alpaca API is briefly down for maintenance? Without proper error handling, your bot is a house of cards—one puff of wind and the whole thing comes crashing down.

In this crucial lesson, you will learn how to build a resilient bot that can gracefully handle and recover from temporary API failures and network issues using try-except blocks.

The Problem: A Brittle Bot
A bot without error handling is "brittle." Any unexpected issue, no matter how small or temporary, will cause it to crash.

Consider this code:

python
# This code is brittle!
import alpaca

# ... client setup ...

# Get the latest price for SPY
latest_trade = trading_client.get_latest_trade("SPY")
price = latest_trade.p

# If the network connection drops for just a second right here,
# the line above will raise an exception, and the script will crash.
# The bot is now offline until you manually restart it.
If your bot crashes, it can't manage open positions, can't enter new trades, and leaves you completely blind. A resilient bot, on the other hand, anticipates these problems and is programmed to survive them.

The Solution: Python's try-except Block
The primary tool for building resilience in Python is the try-except block. It allows you to "try" running a piece of code that might fail. If it succeeds, great. If it fails (raises an "exception"), instead of crashing, the program immediately jumps to the except block, where you can define your recovery logic.

The basic structure looks like this:

python
try:
    # --- Code that might fail goes here ---
    # For example, an API call or a network request.
    print("Attempting to connect to the server...")
    potentially_failing_function()
    print("Success!")

except Exception as e:
    # --- This code runs ONLY if the 'try' block fails ---
    # 'e' is a variable that holds the details of the error.
    print(f"An error occurred: {e}")
    # Here you can log the error, send a notification, etc.

print("The program continues to run instead of crashing.")
Key Failure Points in a Trading Bot
You should wrap any code that communicates with the outside world in a try-except block. This includes:

All Alpaca API Calls: get_account(), submit_order(), get_open_position(), get_latest_trade(), etc.

Network Requests: Sending Discord notifications via webhooks.

File Operations: Reading from config.json or reading/writing to state.json.

Step 1: Fortifying an API Call
Let's make a simple API call resilient.

BEFORE (Brittle):

python
account_info = trading_client.get_account()
print(f"Account is worth: {account_info.portfolio_value}")
AFTER (Resilient):

python
try:
    account_info = trading_client.get_account()
    print(f"Account is worth: {account_info.portfolio_value}")
except Exception as e:
    print(f"Could not connect to Alpaca to get account info: {e}")
    # In a real bot, you would log this and probably exit the current cycle.
Step 2: Integrating Logging and Notifications
When an error occurs, you need to know about it. The except block is the perfect place to use the logging and notification tools we built in previous lessons.

python
# This example combines everything: try-except, logging, and notifications.

try:
    # Attempt to submit a BUY order
    market_order = trading_client.submit_order(order_data=market_order_data)

    # If the order succeeds, log and notify about the success
    log_msg = f"SUCCESS: Submitted BUY order {market_order.id}"
    logging.info(log_msg)
    send_discord_notification(DISCORD_WEBHOOK_URL, f"🚀 {log_msg}")

    # Update and save state
    bot_state['is_in_position'] = True
    save_state(bot_state)

except Exception as e:
    # If the order fails, log and notify about the error
    log_msg = f"ERROR: Failed to submit BUY order: {e}"
    logging.error(log_msg)
    send_discord_notification(DISCORD_WEBHOOK_URL, f"❌ {log_msg}")

    # The bot continues running, and will try again on the next cycle.
Now, if Alpaca's API is momentarily unavailable when your bot tries to place a trade, you will get an instant Discord alert about the failure, the error will be saved in your log file for later diagnosis, and most importantly, the bot will not crash.

Step 3: Deciding on a Recovery Strategy
What the bot does in the except block is its recovery strategy.

Strategy	When to Use	Example
Log and Continue	For non-critical failures that don't affect the core logic.	A Discord notification fails to send. The trade was still placed, so the bot can continue.
Log and Skip Cycle	For critical failures where the bot cannot make an informed decision.	The bot fails to fetch market data from Alpaca. It can't decide whether to buy or sell, so the safest option is to stop the current run and try again later.
Retry with Delay (Advanced)	For temporary network issues.	The bot fails to connect. It waits for 10 seconds (time.sleep(10)) and tries the same API call again, up to 3 times, before giving up for the cycle.
For most cases, "Log and Skip Cycle" is the safest and simplest strategy.

Conclusion
Error handling is not an optional feature; it is a fundamental requirement for any serious, autonomous system. By wrapping all external interactions in try-except blocks, you transform your bot from a brittle script into a resilient worker that can withstand the inevitable glitches and outages of the real world. Your bot is now significantly more reliable and ready for production use.

In the next lessons, we'll finally start implementing trading strategies based on real market data. See you there!