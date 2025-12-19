Tutorial 12: Take Your Profits! – Setting a Take-Profit Order
Objective: In this tutorial, you will learn how to define a precise profit target for your trades by configuring the take_profit component of a bracket order. This ensures your bot automatically locks in gains when a trade goes your way.

1. The Importance of a Profit Target
While a stop-loss protects you from significant losses, a take-profit order secures your winnings. It is a pre-set order to sell a stock once it reaches a specific, higher price.

Why is this crucial?

Discipline Over Greed: The market can be volatile. A stock that hits your profit goal can quickly reverse and turn a winning trade into a losing one. A take-profit order removes the temptation to hold on for "just a little more," which often leads to regret.

Strategy Completion: A complete trading strategy has three parts: an entry, a defensive exit (stop-loss), and an offensive exit (take-profit). Without a profit target, your strategy is incomplete.

Automation: It allows your bot to manage the entire lifecycle of a trade, from start to finish, without any emotional decision-making.

2. Defining the Take-Profit in a Bracket Order
Within a bracket order, the take-profit is a limit order. A limit order instructs the broker to sell your shares at a specific price or better.

The logic is straightforward:

Define a Goal: Decide on a target profit, usually as a percentage of your entry price (e.g., "I want to make 5% on this trade").

Calculate the Price: Before placing the buy order, calculate the exact price that corresponds to your profit goal.

Take-Profit Price = Current Price * (1 + Profit Percentage / 100)

Submit the Order: Include this calculated price in the take_profit parameter of your bracket order call.

3. The Code: Highlighting the Take-Profit Logic
We will use the same bracket_bot.py script from the previous tutorial. This time, pay close attention to the lines specifically related to configuring and calculating the take-profit target.

python
# bracket_bot.py (with focus on Take-Profit)

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 1
# --- THIS IS YOUR PROFIT GOAL ---
TAKE_PROFIT_PERCENTAGE = 5.0  # Goal: Secure a 5% profit.
STOP_LOSS_PERCENTAGE = 2.0   # Safety Net: Limit loss to 2%.

def run_bracket_bot():
    print("🚀 Bracket Order Bot is starting...")
    
    while True:
        try:
            # (Loop and position-checking logic remains the same)
            # ...
            # Inside the 'if Golden Cross' block:
            
            # --- 4. Calculate Stop-Loss and Take-Profit Prices ---
            last_price = api.get_latest_trade(SYMBOL_TO_TRADE).price
            
            # --- THIS IS THE TAKE-PROFIT CALCULATION ---
            take_profit_price = round(last_price * (1 + TAKE_PROFIT_PERCENTAGE / 100), 2)
            
            stop_loss_price = round(last_price * (1 - STOP_LOSS_PERCENTAGE / 100), 2)

            print(f"Last Price: ${last_price}")
            # --- This confirms your calculated target ---
            print(f"Take-Profit Target: ${take_profit_price} (+{TAKE_PROFIT_PERCENTAGE}%)")
            print(f"Stop-Loss Target: ${stop_loss_price} (-{STOP_LOSS_PERCENTAGE}%)")
            
            # --- 5. Submit the Bracket Order ---
            api.submit_order(
                symbol=SYMBOL_TO_TRADE,
                qty=QTY_PER_TRADE,
                side='buy',
                type='market',
                time_in_force='day',
                order_class='bracket',
                # --- THIS IS WHERE YOU SET THE TAKE-PROFIT ORDER ---
                take_profit={'limit_price': take_profit_price},
                stop_loss={'stop_price': stop_loss_price}
            )
            print("✅ Bracket order with profit target submitted successfully.")
            
            # (Rest of the loop logic remains the same)
            # ...
        except Exception as e:
            # (Error handling logic remains the same)
            # ...
            pass

if __name__ == '__main__':
    run_bracket_bot()
4. Understanding the Take-Profit Implementation
TAKE_PROFIT_PERCENTAGE = 5.0: This configuration variable at the top of the script makes your strategy clear and easy to adjust. This is where you define your trading goal. A common strategic choice is to set a risk/reward ratio where the potential profit is greater than the potential loss (e.g., risking 2% to make 4% or more).

take_profit_price = round(...): This line translates your percentage goal into a concrete dollar value. We multiply the current price by 1.05 (for a 5% goal) and round it to two decimal places, as required for currency.

take_profit={'limit_price': take_profit_price}: This is the crucial instruction for the API.

The take_profit key tells the broker you are defining the upper boundary of your bracket.

The limit_price key specifies that this is a limit order. This is an advantage for you—it means the broker will execute the sale at your target price or a better (higher) one if the market moves quickly in your favor.

By setting this parameter, you give your bot a clear objective. It enters the trade based on the Golden Cross signal and will now automatically exit and realize its gain if the price hits your predefined target, completing a successful, disciplined trade.