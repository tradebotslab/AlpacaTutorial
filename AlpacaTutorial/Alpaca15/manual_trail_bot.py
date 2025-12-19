# manual_trail_bot.py
# Tutorial 15: Implementing a Trailing Stop-Loss in Code

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame

# --- Constants ---
SYMBOL_TO_TRADE = "AAPL"
QTY_PER_TRADE = 10
TRAIL_PERCENTAGE = 3.0  # The trailing stop will be 3% below the high price
LOOP_SLEEP_SECONDS = 30  # Check the price every 30 seconds

# --- API Connection ---
api = tradeapi.REST(
    config.API_KEY, 
    config.SECRET_KEY, 
    config.BASE_URL, 
    api_version='v2'
)

# --- State Management ---
# WHY: We need to store the ID of our active stop-loss order
# so we can modify it as the price moves in our favor
active_stop_order_id = None


def check_for_golden_cross_signal(symbol):
    """
    Check if a Golden Cross (20 SMA crosses above 50 SMA) has occurred.
    Returns True if signal detected, False otherwise.
    WHY: This is our entry signal - a classic bullish indicator.
    """
    try:
        # Get enough bars to calculate both moving averages
        barset = api.get_bars(
            symbol, 
            TimeFrame.Day, 
            limit=51, 
            adjustment='raw'
        )
        df = barset.df
        
        # Calculate moving averages
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['sma_50'] = df['close'].rolling(window=50).mean()
        
        current_day = df.iloc[-1]
        previous_day = df.iloc[-2]
        
        # Check if crossover occurred
        golden_cross_detected = (
            previous_day['sma_20'] < previous_day['sma_50'] and 
            current_day['sma_20'] > current_day['sma_50']
        )
        
        return golden_cross_detected
    
    except Exception as e:
        print(f"⚠️ Error checking for signal: {e}")
        return False


def place_initial_stop_loss(symbol, quantity, entry_price, trail_percentage):
    """
    Place the initial stop-loss order after entering a position.
    Returns the order ID.
    WHY: This protects us from catastrophic losses immediately after entry.
    """
    try:
        # Calculate stop price based on entry price and trail percentage
        initial_stop_price = round(entry_price * (1 - trail_percentage / 100), 2)
        
        print(f"📍 Placing initial stop-loss at ${initial_stop_price}")
        
        # Submit a standard stop order (NOT a trailing stop)
        stop_order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='stop',
            time_in_force='gtc',  # Good 'til Canceled
            stop_price=initial_stop_price
        )
        
        print(f"✅ Initial stop-loss order placed with ID: {stop_order.id}")
        return stop_order.id
    
    except Exception as e:
        print(f"❌ Error placing initial stop-loss: {e}")
        return None


def update_trailing_stop(symbol, stop_order_id, current_price, trail_percentage):
    """
    Check if the stop-loss should be moved up and update it if necessary.
    Returns True if updated, False otherwise.
    WHY: This locks in profits as the trade moves in our favor.
    """
    try:
        # Get the existing stop order
        existing_stop_order = api.get_order(stop_order_id)
        existing_stop_price = float(existing_stop_order.stop_price)
        
        # Calculate the new potential stop price based on current market price
        new_stop_price = round(current_price * (1 - trail_percentage / 100), 2)
        
        # Only move the stop UP, never down
        if new_stop_price > existing_stop_price:
            print(f"📈 Adjusting stop-loss upwards: ${existing_stop_price} → ${new_stop_price}")
            
            # Replace the old order with the new stop price
            # WHY: replace_order is atomic - prevents race conditions
            api.replace_order(
                order_id=stop_order_id,
                stop_price=new_stop_price
            )
            
            print(f"✅ Stop-loss successfully updated to ${new_stop_price}")
            return True
        else:
            print(f"ℹ️ Price has not moved up enough. Stop remains at ${existing_stop_price}")
            return False
    
    except Exception as e:
        print(f"⚠️ Error updating trailing stop: {e}")
        return False


def check_position_exists(symbol):
    """
    Check if we currently have a position in the given symbol.
    Returns the position object if it exists, None otherwise.
    WHY: We need to know our current position state before making decisions.
    """
    try:
        position = api.get_position(symbol)
        return position
    except Exception:
        # No position exists - this is expected when we have no shares
        return None


def enter_long_position(symbol, quantity, trail_percentage):
    """
    Enter a long position and immediately place a protective stop-loss.
    Returns the stop order ID if successful, None otherwise.
    WHY: Combining entry and stop placement ensures we're always protected.
    """
    try:
        print(f"📈 Golden Cross Detected! Placing BUY order for {quantity} shares.")
        
        # Submit market buy order
        buy_order = api.submit_order(
            symbol=symbol, 
            qty=quantity, 
            side='buy', 
            type='market', 
            time_in_force='day'
        )
        
        print(f"✅ Buy order submitted: {buy_order.id}")
        
        # Wait for the order to fill
        # WHY: We need the actual entry price to calculate the initial stop
        print("⏳ Waiting 5 seconds for buy order to fill...")
        time.sleep(5)
        
        # Get the position to find our entry price
        position = api.get_position(symbol)
        entry_price = float(position.avg_entry_price)
        
        print(f"✅ Position entered at ${entry_price}")
        
        # Place the initial protective stop-loss
        stop_order_id = place_initial_stop_loss(
            symbol, 
            quantity, 
            entry_price, 
            trail_percentage
        )
        
        return stop_order_id
    
    except Exception as e:
        print(f"❌ Error entering position: {e}")
        return None


def manage_existing_position(symbol, stop_order_id, trail_percentage):
    """
    Manage an existing position by updating the trailing stop if needed.
    WHY: This is the core of our manual trailing stop logic.
    """
    try:
        position = check_position_exists(symbol)
        
        if position is None:
            print("ℹ️ Position was closed (likely by stop-loss).")
            return None
        
        print(f"✅ Position exists: {position.qty} shares at ${position.avg_entry_price}")
        
        if stop_order_id is None:
            print("⚠️ Position exists but no stop order ID. This shouldn't happen.")
            return None
        
        # Get the current market price
        last_trade = api.get_latest_trade(symbol)
        current_price = float(last_trade.price)
        
        print(f"💵 Current price: ${current_price}")
        
        # Update the trailing stop if necessary
        update_trailing_stop(symbol, stop_order_id, current_price, trail_percentage)
        
        return stop_order_id
    
    except Exception as e:
        print(f"⚠️ Error managing position: {e}")
        return None


def run_manual_trail_bot():
    """
    The main function for the manual trailing stop bot.
    WHY: This orchestrates the entire bot's logic in an infinite loop.
    """
    global active_stop_order_id
    
    print("=" * 60)
    print("🚀 Manual Trailing Stop Bot is starting...")
    print(f"📊 Symbol: {SYMBOL_TO_TRADE}")
    print(f"📏 Trail Percentage: {TRAIL_PERCENTAGE}%")
    print(f"⏱️ Loop Interval: {LOOP_SLEEP_SECONDS} seconds")
    print("=" * 60)
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"🕐 Loop running at {now}")
            print(f"{'='*60}")
            
            # Check if we currently have a position
            position = check_position_exists(SYMBOL_TO_TRADE)
            
            if position:
                # We have a position - manage the trailing stop
                active_stop_order_id = manage_existing_position(
                    SYMBOL_TO_TRADE, 
                    active_stop_order_id, 
                    TRAIL_PERCENTAGE
                )
            else:
                # No position - look for entry signal
                print("ℹ️ No position held. Analyzing for entry signal...")
                active_stop_order_id = None  # Clean up state
                
                # Check for Golden Cross signal
                if check_for_golden_cross_signal(SYMBOL_TO_TRADE):
                    # Signal detected - enter position
                    active_stop_order_id = enter_long_position(
                        SYMBOL_TO_TRADE, 
                        QTY_PER_TRADE, 
                        TRAIL_PERCENTAGE
                    )
                else:
                    print("📊 No Golden Cross signal detected yet.")
            
            # Sleep until the next loop
            print(f"\n😴 Sleeping for {LOOP_SLEEP_SECONDS} seconds...")
            time.sleep(LOOP_SLEEP_SECONDS)
        
        except KeyboardInterrupt:
            # User pressed Ctrl+C
            print("\n" + "="*60)
            print("🛑 Bot shutting down gracefully...")
            
            # Cancel any active stop-loss orders
            # WHY: Prevents orphaned orders from lingering in the account
            if active_stop_order_id:
                try:
                    print(f"Canceling active stop-loss order: {active_stop_order_id}")
                    api.cancel_order(active_stop_order_id)
                    print("✅ Stop-loss order canceled.")
                except Exception as e:
                    print(f"⚠️ Could not cancel stop-loss: {e}")
            
            print("="*60)
            break
        
        except Exception as e:
            # Unexpected error occurred
            print(f"❌ An error occurred: {e}")
            print("⚠️ Resetting state and retrying in 60 seconds...")
            active_stop_order_id = None
            time.sleep(60)


if __name__ == '__main__':
    run_manual_trail_bot()

