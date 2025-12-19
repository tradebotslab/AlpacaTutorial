# 1. Imports
import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# 2. Constants
SYMBOL_TO_TRADE = "BTC/USD"  # RSI works well with volatile assets like crypto
QTY_PER_TRADE = 0.01  # Small quantity for BTC
RSI_PERIOD = 14  # Standard RSI period
RSI_OVERBOUGHT = 70  # Threshold for overbought condition
RSI_OVERSOLD = 30  # Threshold for oversold condition
LOOP_SLEEP_SECONDS = 60  # Check every minute

# 3. API Connection
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.BASE_URL, api_version='v2')

# 4. Helper functions
def get_account_info():
    """
    Fetches and displays current account information.
    Returns the account object for further use.
    """
    try:
        account = api.get_account()
        print(f"\n=== Account Information ===")
        print(f"Account Status: {account.status}")
        print(f"Buying Power: ${float(account.buying_power):.2f}")
        print(f"Cash: ${float(account.cash):.2f}")
        print(f"Portfolio Value: ${float(account.portfolio_value):.2f}")
        return account
    except Exception as e:
        print(f"❌ Error fetching account info: {e}")
        return None


def check_position(symbol):
    """
    Checks if a position exists for the given symbol.
    Returns tuple: (position_exists, position_object)
    """
    try:
        position = api.get_position(symbol)
        return True, position
    except Exception:
        return False, None


def get_historical_data_with_rsi(symbol, limit=200):
    """
    Fetches historical bar data and calculates RSI.
    Returns DataFrame with price data and RSI column.
    """
    try:
        # Fetch minute bars for active trading
        barset = api.get_bars(symbol, tradeapi.TimeFrame.Minute, limit=limit)
        
        # Convert to DataFrame
        df = barset.df
        
        # Calculate RSI using pandas-ta library
        # The ta.rsi() method automatically adds RSI column to DataFrame
        df['rsi'] = ta.rsi(df['close'], length=RSI_PERIOD)
        
        return df
    except Exception as e:
        print(f"❌ Error fetching historical data: {e}")
        return None


def place_buy_order(symbol, quantity):
    """
    Places a market buy order for the given symbol.
    Returns True if successful, False otherwise.
    """
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='day'
        )
        print(f"✅ BUY order placed: {quantity} of {symbol}")
        print(f"   Order ID: {order.id}")
        return True
    except Exception as e:
        print(f"❌ Error placing buy order: {e}")
        return False


def place_sell_order(symbol, quantity):
    """
    Places a market sell order for the given symbol.
    Returns True if successful, False otherwise.
    """
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"✅ SELL order placed: {quantity} of {symbol}")
        print(f"   Order ID: {order.id}")
        return True
    except Exception as e:
        print(f"❌ Error placing sell order: {e}")
        return False


def check_rsi_signals(df, position_exists):
    """
    Analyzes RSI data to generate buy/sell signals.
    
    Buy Signal: RSI crosses UP from below oversold level (< 30 to > 30)
    This indicates potential recovery from oversold conditions.
    
    Sell Signal: RSI crosses DOWN from above overbought level (> 70 to < 70)
    This indicates potential decline from overbought conditions.
    
    Returns: 'BUY', 'SELL', or 'HOLD'
    """
    # Get current and previous RSI values
    current_rsi = df.iloc[-1]['rsi']
    previous_rsi = df.iloc[-2]['rsi']
    current_price = df.iloc[-1]['close']
    
    print(f"📊 Current Price: ${current_price:.2f}")
    print(f"📊 Current RSI: {current_rsi:.2f} | Previous RSI: {previous_rsi:.2f}")
    
    # Check for BUY signal: RSI crosses UP through oversold level
    if not position_exists:
        if previous_rsi < RSI_OVERSOLD and current_rsi > RSI_OVERSOLD:
            print(f"📈 BUY Signal! RSI crossed above {RSI_OVERSOLD} (oversold → recovery)")
            return 'BUY'
    
    # Check for SELL signal: RSI crosses DOWN through overbought level
    if position_exists:
        if previous_rsi > RSI_OVERBOUGHT and current_rsi < RSI_OVERBOUGHT:
            print(f"📉 SELL Signal! RSI crossed below {RSI_OVERBOUGHT} (overbought → correction)")
            return 'SELL'
    
    # No signal
    print("⏸️  No RSI crossover signal. Holding position.")
    return 'HOLD'


# 5. Main logic
def run_rsi_bot():
    """
    Main function that runs the RSI trading bot.
    
    This bot implements a mean-reversion strategy:
    - Buys when RSI recovers from oversold conditions (< 30)
    - Sells when RSI drops from overbought conditions (> 70)
    """
    print("🚀 RSI Trading Bot is starting...")
    print(f"📋 Configuration:")
    print(f"   Symbol: {SYMBOL_TO_TRADE}")
    print(f"   Quantity per trade: {QTY_PER_TRADE}")
    print(f"   RSI Period: {RSI_PERIOD}")
    print(f"   Oversold Level: {RSI_OVERSOLD}")
    print(f"   Overbought Level: {RSI_OVERBOUGHT}")
    print(f"   Check Interval: {LOOP_SLEEP_SECONDS} seconds")
    
    # Display account information
    get_account_info()
    
    while True:
        try:
            # Display current timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n{'='*60}")
            print(f"🕐 Loop running at {current_time}")
            print(f"{'='*60}")
            
            # Step 1: Check for existing position
            position_exists, position = check_position(SYMBOL_TO_TRADE)
            
            if position_exists:
                print(f"✅ Position exists: {position.qty} of {SYMBOL_TO_TRADE}")
                print(f"   Entry Price: ${float(position.avg_entry_price):.2f}")
                print(f"   Current Value: ${float(position.market_value):.2f}")
                print(f"   Unrealized P&L: ${float(position.unrealized_pl):.2f}")
            else:
                print("ℹ️  No position currently held.")
            
            # Step 2: Fetch historical data and calculate RSI
            df = get_historical_data_with_rsi(SYMBOL_TO_TRADE, limit=200)
            
            if df is None or len(df) < RSI_PERIOD + 1:
                print("⚠️  Not enough data to calculate RSI. Waiting...")
                time.sleep(LOOP_SLEEP_SECONDS)
                continue
            
            # Step 3: Check for trading signals
            signal = check_rsi_signals(df, position_exists)
            
            # Step 4: Execute trades based on signals
            if signal == 'BUY':
                place_buy_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)
            elif signal == 'SELL':
                # Sell the entire position
                if position:
                    place_sell_order(SYMBOL_TO_TRADE, abs(float(position.qty)))
            
            # Sleep before next iteration
            print(f"\n💤 Sleeping for {LOOP_SLEEP_SECONDS} seconds...")
            time.sleep(LOOP_SLEEP_SECONDS)
        
        except KeyboardInterrupt:
            print("\n🛑 Bot shutting down by user request.")
            print("👋 Goodbye!")
            break
        
        except Exception as e:
            print(f"\n❌ Unexpected error occurred: {e}")
            print(f"⏰ Waiting {LOOP_SLEEP_SECONDS} seconds before retry...")
            time.sleep(LOOP_SLEEP_SECONDS)


# 6. Run
if __name__ == '__main__':
    run_rsi_bot()

