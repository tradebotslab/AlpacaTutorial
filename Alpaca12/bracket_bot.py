# bracket_bot.py
# Tutorial 12: Take Your Profits! – Setting a Take-Profit Order

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame

# --- Constants ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 1
# --- THIS IS YOUR PROFIT GOAL ---
TAKE_PROFIT_PERCENTAGE = 5.0  # Goal: Secure a 5% profit
STOP_LOSS_PERCENTAGE = 2.0    # Safety Net: Limit loss to 2%

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
    WHY: We need the current price to calculate our profit target and stop-loss.
    """
    latest_trade = api.get_latest_trade(symbol)
    current_price = latest_trade.price
    return current_price


def calculate_take_profit_price(entry_price, profit_percentage):
    """
    Calculate the take-profit price based on desired profit percentage.
    Returns the calculated target price rounded to 2 decimal places.
    WHY: This converts your profit goal into a specific dollar amount.
    """
    # --- THIS IS THE TAKE-PROFIT CALCULATION ---
    # If we buy at $100 and want 5% profit, target is $100 * 1.05 = $105
    take_profit_price = entry_price * (1 + profit_percentage / 100)
    rounded_price = round(take_profit_price, 2)
    return rounded_price


def calculate_stop_loss_price(entry_price, loss_percentage):
    """
    Calculate the stop-loss price based on maximum acceptable loss.
    Returns the calculated stop price rounded to 2 decimal places.
    WHY: This protects you from losing more than you're comfortable with.
    """
    # If we buy at $100 and risk 2%, stop is $100 * 0.98 = $98
    stop_loss_price = entry_price * (1 - loss_percentage / 100)
    rounded_price = round(stop_loss_price, 2)
    return rounded_price


def submit_bracket_order(symbol, quantity, take_profit_price, stop_loss_price):
    """
    Submit a bracket order with integrated take-profit and stop-loss.
    The broker will automatically manage both exits.
    WHY: This automates the entire trade lifecycle - no emotions involved.
    """
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='day',
        order_class='bracket',  # This creates the bracket order
        # --- THIS IS WHERE YOU SET THE TAKE-PROFIT ORDER ---
        take_profit={'limit_price': take_profit_price},
        stop_loss={'stop_price': stop_loss_price}
    )


def run_bracket_bot():
    """
    Main function that runs the bracket order bot.
    This bot emphasizes the importance of setting profit targets.
    WHY: Complete risk management requires both protecting losses AND securing gains.
    """
    print("🚀 Bracket Order Bot with Take-Profit is starting...")
    print(f"Trading Symbol: {SYMBOL_TO_TRADE}")
    print(f"Quantity per Trade: {QTY_PER_TRADE}")
    print(f"🎯 Take-Profit Target: {TAKE_PROFIT_PERCENTAGE}%")
    print(f"🛡️  Stop-Loss Protection: {STOP_LOSS_PERCENTAGE}%")
    print(f"📊 Risk/Reward Ratio: 1:{TAKE_PROFIT_PERCENTAGE/STOP_LOSS_PERCENTAGE}")
    print("-" * 50)
    
    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {current_time} ---")

            # --- Step 1: Check if we have a position ---
            position = check_position_exists(SYMBOL_TO_TRADE)
            
            if position is not None:
                # We already have a position, let the bracket order handle it
                print(f"✅ Position exists: {position.qty} share(s)")
                print("ℹ️  Holding position. Bracket order managing exits:")
                print(f"   - Will sell at ${round(float(position.current_price) * (1 + TAKE_PROFIT_PERCENTAGE/100), 2)} (take-profit)")
                print(f"   - Or will sell at ${round(float(position.current_price) * (1 - STOP_LOSS_PERCENTAGE/100), 2)} (stop-loss)")
                
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
                    print("📈 Golden Cross Detected! Preparing bracket order...")

                    # --- Step 5: Get current price ---
                    last_price = get_current_price(SYMBOL_TO_TRADE)
                    print(f"💰 Last Price: ${last_price}")
                    
                    # --- Step 6: Calculate take-profit price ---
                    # --- THIS IS THE CORE OF THIS TUTORIAL ---
                    tp_price = calculate_take_profit_price(
                        last_price, 
                        TAKE_PROFIT_PERCENTAGE
                    )
                    
                    # --- Step 7: Calculate stop-loss price ---
                    sl_price = calculate_stop_loss_price(
                        last_price, 
                        STOP_LOSS_PERCENTAGE
                    )
                    
                    # --- This confirms your calculated targets ---
                    print(f"🎯 Take-Profit Target: ${tp_price} (+{TAKE_PROFIT_PERCENTAGE}%)")
                    print(f"🛡️  Stop-Loss Target: ${sl_price} (-{STOP_LOSS_PERCENTAGE}%)")
                    print(f"💵 Potential Profit: ${round((tp_price - last_price) * QTY_PER_TRADE, 2)}")
                    print(f"💵 Potential Loss: ${round((last_price - sl_price) * QTY_PER_TRADE, 2)}")
                    
                    # --- Step 8: Submit the bracket order ---
                    submit_bracket_order(
                        SYMBOL_TO_TRADE, 
                        QTY_PER_TRADE, 
                        tp_price, 
                        sl_price
                    )
                    print("✅ Bracket order with profit target submitted successfully!")
                    print("ℹ️  The broker will now automatically:")
                    print(f"   1. Buy {QTY_PER_TRADE} share(s) of {SYMBOL_TO_TRADE}")
                    print(f"   2. Sell at ${tp_price} if price goes up (PROFIT)")
                    print(f"   3. Sell at ${sl_price} if price goes down (PROTECTION)")
                
                else:
                    print("⏸️  No entry signal detected. Waiting...")
            
            # --- Step 9: Sleep before next iteration ---
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
    run_bracket_bot()

