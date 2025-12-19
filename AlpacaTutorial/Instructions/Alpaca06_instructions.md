Tutorial 6: Anatomy of a Bot – The Main Loop
Objective: In this tutorial, you will learn about the most critical component of any automated bot: the main loop. You will build a simple, infinite loop that serves as the bot's "heartbeat," allowing it to perform actions at regular, controlled intervals.

1. What is a Main Loop?
Every automated bot, whether for trading, social media, or data collection, needs a core engine that runs continuously. This is the main loop.

Think of it as the bot's consciousness. It's an infinite loop that:

Wakes up at a set interval.

Performs a series of tasks (e.g., checks the market, analyzes data, looks for a trade signal).

Goes back to sleep for a set period.

Repeats this cycle indefinitely until you stop it.

This structure allows your bot to operate autonomously 24/7 without any manual intervention.

2. Project Setup
In your alpaca_bot_project folder, create a new file named main_loop_bot.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── ... (previous files)
└── main_loop_bot.py     # New file
3. Creating the Script (main_loop_bot.py)
Open the main_loop_bot.py file and add the following code. This script creates a simple bot that wakes up every 60 seconds to check your account's buying power.

python
# main_loop_bot.py

import alpaca_trade_api as tradeapi
import config
import time
from datetime import datetime

# --- 1. Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

def run_bot():
    print("Bot is starting...")
    
    # --- 2. The Main Loop ---
    while True:
        try:
            # Get the current time for logging
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 3. The Bot's Action ---
            # For this example, we'll just check our account status.
            # In a real bot, you would fetch data, run your strategy, etc.
            account = api.get_account()
            
            print(f"Account Status: {account.status}")
            print(f"Buying Power: ${account.buying_power}")
            
            # --- 4. Sleep Until the Next Interval ---
            # We'll run this loop once every 60 seconds.
            print("Action complete. Sleeping for 60 seconds...")
            time.sleep(60)

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing...")
            # If an error occurs, wait a bit before trying again
            time.sleep(30)


# --- This is the entry point of our script ---
if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        # --- 5. Graceful Shutdown ---
        print("\nBot is shutting down. Goodbye!")
4. Understanding the Code
Authentication: We connect to the API as usual.

The Main Loop (while True:): This is the core of our bot. while True: creates a loop that will run forever unless it is explicitly stopped. The entire logic of our bot will live inside this loop.

The Bot's Action: Inside the loop, we define what the bot should do each time it wakes up. For this simple example, we call api.get_account() to check our buying power. In a real trading bot, this section would be much more complex, involving steps like:

Fetching the latest market data.

Calculating technical indicators.

Checking if your strategy's conditions for a trade are met.

Placing an order if conditions are right.

Sleeping (time.sleep(60)): This is a critical component. After performing its actions, the bot needs to pause.

Why? If you don't include a sleep command, the loop will run thousands of times per second, overwhelming your computer and spamming the Alpaca API. This will get your API key rate-limited (temporarily blocked).

time.sleep(60) tells the script to pause for 60 seconds before starting the next iteration of the loop. This interval is the "heartbeat" of your bot.

Graceful Shutdown (KeyboardInterrupt):

An infinite loop needs a way to be stopped. When you run this script in your terminal, you can press Ctrl+C.

The try...except KeyboardInterrupt: block "catches" this command, allowing you to print a clean shutdown message instead of having the program crash with an error.

How to Run and Stop the Bot
Run: Open your terminal, navigate to your project folder, and run the script:

bash
python main_loop_bot.py
You will see it print the startup message and then your account status. It will then pause.

Stop: Wait for it to run at least one or two loops, then press Ctrl+C on your keyboard. You will see the "Bot is shutting down" message.