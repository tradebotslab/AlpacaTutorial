Tutorial 11: The Safety Net – How to Set a Simple Stop-Loss
Objective: In this tutorial, you will learn one of the most critical aspects of risk management: how to automatically protect your trades by setting a stop-loss. You will do this by submitting "bracket orders," which attach both a stop-loss and a take-profit order to your entry trade.

1. What are Stop-Loss and Take-Profit?
Stop-Loss: An order that automatically sells your stock if its price falls to a specific level. Its purpose is to limit your potential loss on a trade. It's your "safety net."

Take-Profit: An order that automatically sells your stock if its price rises to a specific target level. Its purpose is to lock in profits.

Manually watching the market to decide when to sell is difficult and stressful. By automating these exits, you remove emotion from the decision and enforce disciplined trading.

2. The Power of Bracket Orders
A Bracket Order is a powerful feature that combines three orders into one:

The Main Entry Order: Your initial buy (or sell) order.

A Take-Profit Order: A limit order to sell at a higher price.

A Stop-Loss Order: A stop order to sell at a lower price.

These three orders are linked. When the main order is filled, the two exit orders (take-profit and stop-loss) become active. The moment one of these exit orders is triggered (e.g., your take-profit target is hit), the other one is automatically canceled. This is also known as a "One-Cancels-Other" (OCO) order.

3. Project Setup
In your alpaca_bot_project folder, create a new file named bracket_bot.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── ... (previous files)
└── bracket_bot.py       # New file
4. Creating the Script (bracket_bot.py)
This script modifies our crossover bot to use bracket orders for entry. Notice how the exit logic is now much simpler—the bracket order handles it for us.

python
# bracket_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime

# --- Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 1
TAKE_PROFIT_PERCENTAGE = 5.0  # 5%
STOP_LOSS_PERCENTAGE = 2.0   # 2%

def run_bracket_bot():
    """The main function for the bracket order bot."""
    print("🚀 Bracket Order Bot is starting...")
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. Check if we have a position ---
            try:
                position = api.get_position(SYMBOL_TO_TRADE)
                print(f"✅ Position exists: {position.qty} share(s). Holding and letting bracket order manage the exit.")
                
            except Exception:
                # No position exists, so we check for an entry signal
                print("ℹ️ No position held. Analyzing for entry signal...")

                # --- 2. Analyze for Entry ---
                barset = api.get_bars(SYMBOL_TO_TRADE, TimeFrame.Day, limit=51, adjustment='raw')
                df = barset.df
                df['sma_20'] = df['close'].rolling(window=20).mean()
                df['sma_50'] = df['close'].rolling(window=50).mean()

                current_day = df.iloc[-1]
                previous_day = df.iloc[-2]

                # --- 3. Golden Cross Entry Signal ---
                if previous_day['sma_20'] < previous_day['sma_50'] and current_day['sma_20'] > current_day['sma_50']:
                    print("📈 Golden Cross Detected! Preparing bracket order.")

                    # --- 4. Calculate Stop-Loss and Take-Profit Prices ---
                    last_price = api.get_latest_trade(SYMBOL_TO_TRADE).price
                    
                    take_profit_price = round(last_price * (1 + TAKE_PROFIT_PERCENTAGE / 100), 2)
                    stop_loss_price = round(last_price * (1 - STOP_LOSS_PERCENTAGE / 100), 2)

                    print(f"Last Price: ${last_price}")
                    print(f"Take-Profit Target: ${take_profit_price} (+{TAKE_PROFIT_PERCENTAGE}%)")
                    print(f"Stop-Loss Target: ${stop_loss_price} (-{STOP_LOSS_PERCENTAGE}%)")
                    
                    # --- 5. Submit the Bracket Order ---
                    api.submit_order(
                        symbol=SYMBOL_TO_TRADE,
                        qty=QTY_PER_TRADE,
                        side='buy',
                        type='market',
                        time_in_force='day',
                        order_class='bracket', # This is key!
                        take_profit={'limit_price': take_profit_price},
                        stop_loss={'stop_price': stop_loss_price}
                    )
                    print("✅ Bracket order submitted successfully.")
                
                else:
                    print("Signal: No entry signal. Holding.")
            
            # --- Sleep ---
            print("Action complete. Sleeping for 5 minutes...")
            time.sleep(300)

        except KeyboardInterrupt:
            print("\n🛑 Bot is shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Continuing...")
            time.sleep(60)

# --- Entry point of the script ---
if __name__ == '__main__':
    run_bracket_bot()
5. Understanding the Code
Simplified Logic: Notice the main if/else is now based on whether a position exists. If we have a position, we do nothing, because we trust our pre-set bracket order to manage the exit. If we don't have a position, we hunt for a buy signal.

Calculate Exit Prices: Before placing the order, we need to define our exit targets.

We get the most recent trade price using api.get_latest_trade().

We calculate the take_profit_price and stop_loss_price based on the percentages defined in our configuration.

The Bracket Order Submission: This is the most important part. The api.submit_order() call now includes three new parameters:

order_class='bracket': This tells the Alpaca API that we are submitting this special type of linked order.

take_profit={'limit_price': take_profit_price}: A dictionary specifying the price for our take-profit limit order.

stop_loss={'stop_price': stop_loss_price}: A dictionary specifying the price for our stop-loss stop order.

"Set and Forget": Once the order is submitted, the bot's job is done for this trade. It doesn't need to check for a "Death Cross" to sell. The broker will now monitor the price and execute one of the exit orders automatically if the price hits either target. The bot is now free to look for the next opportunity in a different stock, or just wait until this position is closed.