# dynamic_sizing_bot.py
# Tutorial 13: Never Risk Too Much – Calculating Position Size

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame

# --- Constants ---
SYMBOL_TO_TRADE = "AAPL"
# --- THIS IS THE CORE OF OUR RISK STRATEGY ---
RISK_PER_TRADE_PERCENTAGE = 1.0  # Risk only 1% of our total equity per trade
TAKE_PROFIT_PERCENTAGE = 3.0     # A 3:1 reward-to-risk ratio
STOP_LOSS_PERCENTAGE = 1.0       # The distance to our stop-loss from entry

# --- API Connection ---
api = tradeapi.REST(
    config.API_KEY, 
    config.SECRET_KEY, 
    config.BASE_URL, 
    api_version='v2'
)


def check_position_exists(symbol):
    """
    Check if we currently have a position in the given symbol.
    Returns the position object if it exists, None otherwise.
    WHY: We need to know if we already own shares before buying more.
    """
    try:
        position = api.get_position(symbol)
        return position
    except Exception:
        # No position exists - this is expected when we have no shares
        return None


def get_historical_bars(symbol, limit):
    """
    Fetch historical daily bars for analysis.
    Returns a pandas DataFrame with OHLCV data.
    WHY: We need historical data to calculate moving averages.
    """
    barset = api.get_bars(
        symbol, 
        TimeFrame.Day, 
        limit=limit, 
        adjustment='raw'
    )
    bars_dataframe = barset.df
    return bars_dataframe


def calculate_moving_averages(dataframe):
    """
    Calculate 20-day and 50-day Simple Moving Averages.
    Returns the dataframe with two new columns added.
    WHY: Moving averages help identify trends and generate signals.
    """
    dataframe['sma_20'] = dataframe['close'].rolling(window=20).mean()
    dataframe['sma_50'] = dataframe['close'].rolling(window=50).mean()
    return dataframe


def detect_golden_cross(dataframe):
    """
    Detect if a Golden Cross signal occurred.
    Golden Cross = 20 SMA crosses above 50 SMA.
    Returns True if signal detected, False otherwise.
    WHY: This is our entry signal for bullish trades.
    """
    current_day = dataframe.iloc[-1]
    previous_day = dataframe.iloc[-2]
    
    # Check if crossover happened
    previous_20_below_50 = previous_day['sma_20'] < previous_day['sma_50']
    current_20_above_50 = current_day['sma_20'] > current_day['sma_50']
    
    golden_cross_detected = previous_20_below_50 and current_20_above_50
    return golden_cross_detected


def get_current_price(symbol):
    """
    Get the most recent trade price for the symbol.
    Returns the price as a float.
    WHY: We need the current price to calculate position size and targets.
    """
    latest_trade = api.get_latest_trade(symbol)
    current_price = latest_trade.price
    return current_price


def get_account_equity():
    """
    Get the total equity (cash + stock value) in our account.
    Returns equity as a float.
    WHY: We need to know our total capital to calculate risk amount.
    """
    account = api.get_account()
    total_equity = float(account.equity)
    return total_equity


def calculate_position_size(total_equity, entry_price, risk_percentage, stop_loss_percentage):
    """
    Calculate how many shares to buy based on risk management rules.
    This is the CORE of professional position sizing.
    
    Returns the number of shares to buy (integer).
    WHY: This ensures we only risk a fixed percentage of capital per trade.
    """
    # --- Step 1: Calculate how much money we can risk ---
    # If we have $10,000 and risk 1%, we can risk $100
    risk_amount_dollars = total_equity * (risk_percentage / 100)
    
    # --- Step 2: Calculate where our stop-loss will be ---
    # If entry is $100 and stop is 1% away, stop is at $99
    stop_loss_price = entry_price * (1 - stop_loss_percentage / 100)
    
    # --- Step 3: Calculate risk per share ---
    # If we buy at $100 and stop at $99, we risk $1 per share
    risk_per_share = entry_price - stop_loss_price
    
    # --- Step 4: Calculate position size ---
    # If we can risk $100 total and risk $1 per share, buy 100 shares
    # THIS IS THE FORMULA THAT PROTECTS YOUR CAPITAL
    if risk_per_share <= 0:
        # Safety check: stop-loss must be below entry
        return 0
    
    position_size = risk_amount_dollars / risk_per_share
    
    # Round down to whole shares
    position_size_integer = int(position_size)
    
    return position_size_integer


def calculate_take_profit_price(entry_price, profit_percentage):
    """
    Calculate the take-profit price based on desired profit percentage.
    Returns the calculated target price rounded to 2 decimal places.
    WHY: This converts your profit goal into a specific dollar amount.
    """
    take_profit_price = entry_price * (1 + profit_percentage / 100)
    rounded_price = round(take_profit_price, 2)
    return rounded_price


def calculate_stop_loss_price(entry_price, loss_percentage):
    """
    Calculate the stop-loss price based on maximum acceptable loss.
    Returns the calculated stop price rounded to 2 decimal places.
    WHY: This protects you from losing more than you're comfortable with.
    """
    stop_loss_price = entry_price * (1 - loss_percentage / 100)
    rounded_price = round(stop_loss_price, 2)
    return rounded_price


def submit_bracket_order(symbol, quantity, take_profit_price, stop_loss_price):
    """
    Submit a bracket order with dynamically calculated position size.
    The broker will automatically manage both exits.
    WHY: This automates the entire trade with proper risk management.
    """
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='day',
        order_class='bracket',
        take_profit={'limit_price': take_profit_price},
        stop_loss={'stop_price': stop_loss_price}
    )


def run_dynamic_sizing_bot():
    """
    Main function that runs the dynamic position sizing bot.
    This bot implements professional-grade risk management.
    WHY: Position sizing is what separates amateur traders from professionals.
    """
    print("🚀 Dynamic Position Sizing Bot is starting...")
    print(f"Trading Symbol: {SYMBOL_TO_TRADE}")
    print(f"💰 Risk per Trade: {RISK_PER_TRADE_PERCENTAGE}% of equity")
    print(f"🎯 Take-Profit Target: {TAKE_PROFIT_PERCENTAGE}%")
    print(f"🛡️  Stop-Loss Protection: {STOP_LOSS_PERCENTAGE}%")
    print(f"📊 Risk/Reward Ratio: 1:{TAKE_PROFIT_PERCENTAGE/STOP_LOSS_PERCENTAGE}")
    print("-" * 60)
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {current_time} ---")

            # --- Step 1: Check if we have a position ---
            position = check_position_exists(SYMBOL_TO_TRADE)
            
            if position is not None:
                # We already have a position
                current_position_value = float(position.qty) * float(position.current_price)
                print(f"✅ Position exists: {position.qty} share(s)")
                print(f"💵 Position Value: ${current_position_value:,.2f}")
                print("ℹ️  Holding position. Bracket order managing exits.")
                
            else:
                # No position exists, look for entry signal
                print("ℹ️  No position held. Analyzing for entry signal...")

                # --- Step 2: Get historical data ---
                bars = get_historical_bars(SYMBOL_TO_TRADE, limit=51)
                
                # --- Step 3: Calculate moving averages ---
                bars_with_sma = calculate_moving_averages(bars)
                
                # --- Step 4: Check for Golden Cross signal ---
                signal_detected = detect_golden_cross(bars_with_sma)
                
                if signal_detected:
                    print("📈 Golden Cross Detected! Calculating dynamic position size...")

                    # --- Step 5: Get account equity ---
                    # THIS IS CRITICAL - we need current equity for position sizing
                    total_equity = get_account_equity()
                    
                    # --- Step 6: Get current price ---
                    last_price = get_current_price(SYMBOL_TO_TRADE)
                    
                    # --- Step 7: Calculate position size ---
                    # THIS IS THE CORE OF THIS TUTORIAL
                    qty_to_trade = calculate_position_size(
                        total_equity=total_equity,
                        entry_price=last_price,
                        risk_percentage=RISK_PER_TRADE_PERCENTAGE,
                        stop_loss_percentage=STOP_LOSS_PERCENTAGE
                    )
                    
                    # --- Step 8: Safety check ---
                    if qty_to_trade < 1:
                        print(f"⚠️  Calculated position size is {qty_to_trade} shares (less than 1).")
                        print("⚠️  Account too small or stock too expensive. Skipping trade.")
                        print(f"⚠️  Tip: Need at least ${last_price * STOP_LOSS_PERCENTAGE / RISK_PER_TRADE_PERCENTAGE:,.2f} equity to trade {SYMBOL_TO_TRADE}")
                    else:
                        # --- Step 9: Calculate take-profit and stop-loss prices ---
                        tp_price = calculate_take_profit_price(
                            last_price, 
                            TAKE_PROFIT_PERCENTAGE
                        )
                        
                        sl_price = calculate_stop_loss_price(
                            last_price, 
                            STOP_LOSS_PERCENTAGE
                        )
                        
                        # --- Step 10: Calculate actual dollar amounts ---
                        risk_amount = (last_price - sl_price) * qty_to_trade
                        profit_potential = (tp_price - last_price) * qty_to_trade
                        position_value = last_price * qty_to_trade
                        
                        # --- THIS SHOWS WHY DYNAMIC SIZING MATTERS ---
                        print(f"\n{'='*60}")
                        print(f"💼 Account Equity: ${total_equity:,.2f}")
                        print(f"💰 Entry Price: ${last_price:.2f}")
                        print(f"📏 Position Size Calculated: {qty_to_trade} shares")
                        print(f"💵 Position Value: ${position_value:,.2f}")
                        print(f"🎯 Take-Profit: ${tp_price:.2f} (+{TAKE_PROFIT_PERCENTAGE}%)")
                        print(f"🛡️  Stop-Loss: ${sl_price:.2f} (-{STOP_LOSS_PERCENTAGE}%)")
                        print(f"\n--- Risk Analysis ---")
                        print(f"💸 Risk Amount: ${risk_amount:.2f} ({risk_amount/total_equity*100:.2f}% of equity)")
                        print(f"💰 Profit Potential: ${profit_potential:.2f}")
                        print(f"📊 Risk/Reward: ${risk_amount:.2f} to make ${profit_potential:.2f}")
                        print(f"{'='*60}\n")
                        
                        # --- Step 11: Submit the dynamically sized bracket order ---
                        submit_bracket_order(
                            SYMBOL_TO_TRADE, 
                            qty_to_trade, 
                            tp_price, 
                            sl_price
                        )
                        print("✅ Dynamically sized bracket order submitted successfully!")
                        print(f"ℹ️  This trade risks exactly {RISK_PER_TRADE_PERCENTAGE}% of your capital.")
                        print(f"ℹ️  No matter what the stock price is, your risk is controlled.")
                
                else:
                    print("⏸️  No entry signal detected. Waiting...")
            
            # --- Step 12: Sleep before next iteration ---
            print("\n💤 Sleeping for 5 minutes...")
            time.sleep(300)

        except KeyboardInterrupt:
            print("\n🛑 Bot is shutting down. Goodbye!")
            break
            
        except Exception as error:
            print(f"❌ An error occurred: {error}")
            print("⚠️  Continuing in 60 seconds...")
            time.sleep(60)


# --- Entry Point ---
if __name__ == '__main__':
    run_dynamic_sizing_bot()

