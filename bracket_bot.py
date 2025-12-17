# bracket_bot.py
# Tutorial 11: Bracket Orders with Stop-Loss and Take-Profit

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame

# --- Constants ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 1
TAKE_PROFIT_PERCENTAGE = 5.0  # 5% profit target
STOP_LOSS_PERCENTAGE = 2.0    # 2% loss limit

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
    """
    try:
        position = api.get_position(symbol)
        return position
    except Exception:
        # No position exists
        return None


def get_historical_bars(symbol, limit):
    """
    Fetch historical daily bars for analysis.
    Returns a pandas DataFrame with OHLCV data.
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
    """
    dataframe['sma_20'] = dataframe['close'].rolling(window=20).mean()
    dataframe['sma_50'] = dataframe['close'].rolling(window=50).mean()
    return dataframe


def detect_golden_cross(dataframe):
    """
    Detect if a Golden Cross signal occurred.
    Golden Cross = 20 SMA crosses above 50 SMA.
    Returns True if signal detected, False otherwise.
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
    """
    latest_trade = api.get_latest_trade(symbol)
    current_price = latest_trade.price
    return current_price


def calculate_exit_prices(entry_price, take_profit_pct, stop_loss_pct):
    """
    Calculate the take-profit and stop-loss prices.
    Returns a tuple: (take_profit_price, stop_loss_price)
    """
    take_profit_price = round(entry_price * (1 + take_profit_pct / 100), 2)
    stop_loss_price = round(entry_price * (1 - stop_loss_pct / 100), 2)
    return take_profit_price, stop_loss_price


def submit_bracket_order(symbol, quantity, take_profit_price, stop_loss_price):
    """
    Submit a bracket order with integrated take-profit and stop-loss.
    The broker will automatically manage the exit.
    """
    api.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        type='market',
        time_in_force='day',
        order_class='bracket',  # This creates the bracket order
        take_profit={'limit_price': take_profit_price},
        stop_loss={'stop_price': stop_loss_price}
    )


def run_bracket_bot():
    """
    Main function that runs the bracket order bot.
    This bot uses bracket orders to automatically manage risk.
    """
    print("🚀 Bracket Order Bot is starting...")
    print(f"Trading Symbol: {SYMBOL_TO_TRADE}")
    print(f"Quantity per Trade: {QTY_PER_TRADE}")
    print(f"Take-Profit: {TAKE_PROFIT_PERCENTAGE}%")
    print(f"Stop-Loss: {STOP_LOSS_PERCENTAGE}%")
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
                print("ℹ️  Holding position. Bracket order will manage the exit.")
                
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
                    
                    # --- Step 6: Calculate exit prices ---
                    tp_price, sl_price = calculate_exit_prices(
                        last_price, 
                        TAKE_PROFIT_PERCENTAGE, 
                        STOP_LOSS_PERCENTAGE
                    )
                    
                    print(f"🎯 Take-Profit Target: ${tp_price} (+{TAKE_PROFIT_PERCENTAGE}%)")
                    print(f"🛡️  Stop-Loss Target: ${sl_price} (-{STOP_LOSS_PERCENTAGE}%)")
                    
                    # --- Step 7: Submit the bracket order ---
                    submit_bracket_order(
                        SYMBOL_TO_TRADE, 
                        QTY_PER_TRADE, 
                        tp_price, 
                        sl_price
                    )
                    print("✅ Bracket order submitted successfully!")
                    print("ℹ️  The broker will now automatically manage this trade.")
                
                else:
                    print("⏸️  No entry signal detected. Waiting...")
            
            # --- Step 8: Sleep before next iteration ---
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

