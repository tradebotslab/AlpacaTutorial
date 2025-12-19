Tutorial 13: Never Risk Too Much – Calculating Position Size
Objective: In this tutorial, you will learn the single most important rule of money management: position sizing. You will learn how to dynamically calculate the number of shares to buy to ensure that you only risk a small, fixed percentage of your total capital on any single trade.

1. What is Position Sizing, and Why is it Essential?
So far, we have been trading a fixed number of shares (e.g., QTY_PER_TRADE = 1). This is a flawed approach. Risking the same number of shares on a $20 stock and a $500 stock is not the same at all.

Position Sizing is the process of calculating how many shares to buy so that if your stop-loss is hit, you lose a predictable and controlled amount of money.

This is the bedrock of risk management because it:

Prevents Catastrophic Losses: It makes it mathematically impossible for a single bad trade to wipe out a significant portion of your account.

Ensures Consistency: It standardizes your risk across every trade. You risk 1% of your capital whether you're trading Apple or a small-cap stock.

Enables Long-Term Survival: No trader is right 100% of the time. Professional traders survive losing streaks because they manage their risk on every single trade.

2. The Position Sizing Formula
The calculation is straightforward and follows four simple steps:

Define Your Max Risk per Trade: Decide on a small percentage of your total account equity you are willing to risk on one trade. Professionals typically use 1% or 2%.

Calculate Your Risk Amount in Dollars:

Risk Amount ($) = Total Equity * Risk Percentage

Determine Your Risk Per Share: This is the dollar amount you lose per share if your stop-loss is hit.

Risk Per Share ($) = Entry Price - Stop-Loss Price

Calculate the Number of Shares to Buy:

Position Size = Risk Amount ($) / Risk Per Share ($)

Example:

You have a $10,000 account and will risk 1% per trade.

Your Risk Amount is $10,000 * 0.01 = $100.

You want to buy a stock at $50. Your stop-loss will be at $48.

Your Risk Per Share is $50 - $48 = $2.

Your Position Size is $100 / $2 = 50 shares.

If you buy 50 shares at $50 and the trade fails, you will be stopped out at $48, losing exactly $100 (50 shares * $2 loss/share), which is 1% of your capital.

3. Creating the Script (dynamic_sizing_bot.py)
This script upgrades our bracket_bot to use this dynamic calculation instead of a fixed trade quantity.

python
# dynamic_sizing_bot.py

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AAPL"
# --- THIS IS THE CORE OF OUR RISK STRATEGY ---
RISK_PER_TRADE_PERCENTAGE = 1.0 # Risk only 1% of our total equity per trade.
TAKE_PROFIT_PERCENTAGE = 3.0   # A 3:1 reward-to-risk ratio
STOP_LOSS_PERCENTAGE = 1.0     # The distance to our stop-loss from entry

def run_dynamic_sizing_bot():
    print("🚀 Dynamic Sizing Bot is starting...")
    
    while True:
        try:
            # (Loop, position check, and analysis logic remains the same)
            # ...
            # Inside the 'if Golden Cross' block:
            
            print("📈 Golden Cross Detected! Preparing dynamic order.")

            # --- 1. Get Account and Price Info ---
            account = api.get_account()
            total_equity = float(account.equity)
            last_price = api.get_latest_trade(SYMBOL_TO_TRADE).price

            # --- 2. Calculate Position Size ---
            # How much we can risk in dollars
            risk_amount_dollars = total_equity * (RISK_PER_TRADE_PERCENTAGE / 100)
            
            # Where our stop-loss price will be
            stop_loss_price = round(last_price * (1 - STOP_LOSS_PERCENTAGE / 100), 2)
            
            # How much we risk on a single share
            risk_per_share = last_price - stop_loss_price

            # How many shares we can buy
            if risk_per_share <= 0:
                print("⚠️ Risk per share is zero or negative. Skipping trade.")
                continue
            
            qty_to_trade = int(risk_amount_dollars / risk_per_share)
            
            if qty_to_trade < 1:
                print(f"⚠️ Calculated quantity is less than 1 ({qty_to_trade}). Skipping trade.")
                continue

            # --- 3. Calculate Take-Profit Price ---
            take_profit_price = round(last_price * (1 + TAKE_PROFIT_PERCENTAGE / 100), 2)

            print(f"Total Equity: ${total_equity:,.2f}")
            print(f"Risk Amount: ${risk_amount_dollars:,.2f}")
            print(f"Last Price: ${last_price}")
            print(f"Stop-Loss Price: ${stop_loss_price}")
            print(f"Calculated Position Size: {qty_to_trade} shares")
            
            # --- 4. Submit the Dynamically Sized Bracket Order ---
            api.submit_order(
                symbol=SYMBOL_TO_TRADE,
                qty=qty_to_trade, # Use our calculated quantity
                side='buy',
                type='market',
                time_in_force='day',
                order_class='bracket',
                take_profit={'limit_price': take_profit_price},
                stop_loss={'stop_price': stop_loss_price}
            )
            print("✅ Dynamically sized bracket order submitted successfully.")
            
            # (Rest of the loop logic remains the same)
            # ...
        except Exception as e:
            # (Error handling logic remains the same)
            # ...
            pass

if __name__ == '__main__':
    run_dynamic_sizing_bot()
4. Understanding the Code
The key change is the block of calculations performed right after a buy signal is detected.

account = api.get_account(): We fetch the current state of our entire account. account.equity gives us the total value of our portfolio (cash + stocks).

risk_amount_dollars = ...: We translate our RISK_PER_TRADE_PERCENTAGE (1%) into a concrete dollar amount based on our current equity.

risk_per_share = ...: We calculate the exact dollar loss we would incur on a single share if our stop-loss is hit.

qty_to_trade = int(...): This is the formula in action. We divide our total allowed risk in dollars by the risk on a single share. This gives us the precise number of shares to buy. We use int() to ensure we get a whole number.

Safety Checks: We check if qty_to_trade is at least 1. If our account is too small or the stock price too high, the calculation might result in a fraction, so we skip the trade to avoid errors.

qty=qty_to_trade: In the submit_order call, we no longer use a fixed number. We use our dynamically calculated qty_to_trade, ensuring every trade is perfectly sized according to our risk rules.

Congratulations! You have now implemented a professional-grade risk management system. By dynamically sizing every position, your bot is significantly more robust, safer, and better prepared for long-term automated trading. This single technique is often what separates amateur algorithms from professional ones.