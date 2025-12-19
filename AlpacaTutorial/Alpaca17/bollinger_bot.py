# bollinger_bot.py
# Tutorial 17: The Magic of Volatility – A Bollinger Bands® Bot
# This bot uses Bollinger Bands to detect volatility squeezes and trade breakouts

# --- 1. Imports ---
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime

# --- 2. Constants ---
SYMBOL_TO_TRADE = "NVDA"
BB_PERIOD = 20
BB_STD_DEV = 2.0
# The 'squeeze' is identified when the Bandwidth is below this threshold
SQUEEZE_THRESHOLD = 4.0  # This value may need tuning based on the asset
QTY_PER_TRADE = 5
LOOP_SLEEP_SECONDS = 60  # Check every minute

# --- 3. API Connection ---
api = tradeapi.REST(
    config.API_KEY,
    config.SECRET_KEY,
    config.BASE_URL,
    api_version='v2'
)


# --- 4. Helper Functions ---

def get_current_position(symbol):
    """
    Check if we have an existing position for the given symbol.
    
    Args:
        symbol: Stock symbol to check
        
    Returns:
        tuple: (position_exists: bool, position_qty: int)
    """
    try:
        position = api.get_position(symbol)
        position_qty = int(position.qty)
        print(f"✅ Position exists: {position_qty} shares of {symbol}.")
        return True, position_qty
    except Exception:
        print("ℹ️ No position currently held.")
        return False, 0


def fetch_price_data(symbol, timeframe, limit):
    """
    Fetch historical price data for a symbol.
    
    Args:
        symbol: Stock symbol to fetch data for
        timeframe: TimeFrame object (e.g., TimeFrame.Hour)
        limit: Number of bars to fetch
        
    Returns:
        pandas.DataFrame: DataFrame with OHLCV data
    """
    try:
        barset = api.get_bars(
            symbol,
            timeframe,
            limit=limit,
            adjustment='raw'
        )
        df = barset.df
        
        if df.empty:
            raise ValueError(f"No data returned for {symbol}")
            
        print(f"📊 Fetched {len(df)} bars for {symbol}.")
        return df
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        raise


def calculate_bollinger_bands(df, period, std_dev):
    """
    Calculate Bollinger Bands using pandas-ta.
    
    Args:
        df: DataFrame with price data
        period: Period for the moving average
        std_dev: Number of standard deviations for the bands
        
    Returns:
        pandas.DataFrame: DataFrame with Bollinger Bands columns added
    """
    try:
        # Calculate Bollinger Bands
        # This adds columns: BBL_20_2.0, BBM_20_2.0, BBU_20_2.0, BBB_20_2.0, BBP_20_2.0
        df.ta.bbands(length=period, std=std_dev, append=True)
        
        # Rename columns for easier access
        df.rename(columns={
            f'BBL_{period}_{std_dev}': 'lower',
            f'BBM_{period}_{std_dev}': 'middle',
            f'BBU_{period}_{std_dev}': 'upper',
            f'BBB_{period}_{std_dev}': 'bandwidth'
        }, inplace=True)
        
        print("✅ Bollinger Bands calculated successfully.")
        return df
        
    except Exception as e:
        print(f"❌ Error calculating Bollinger Bands: {e}")
        raise


def place_buy_order(symbol, quantity):
    """
    Place a market buy order.
    
    Args:
        symbol: Stock symbol to buy
        quantity: Number of shares to buy
    """
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='buy',
            type='market',
            time_in_force='day'
        )
        print(f"✅ BUY order placed: {quantity} shares of {symbol}")
        return order
        
    except Exception as e:
        print(f"❌ Error placing BUY order: {e}")
        raise


def place_sell_order(symbol, quantity):
    """
    Place a market sell order.
    
    Args:
        symbol: Stock symbol to sell
        quantity: Number of shares to sell
    """
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='market',
            time_in_force='day'
        )
        print(f"✅ SELL order placed: {quantity} shares of {symbol}")
        return order
        
    except Exception as e:
        print(f"❌ Error placing SELL order: {e}")
        raise


def check_squeeze_breakout(current_bar, previous_bar, squeeze_threshold):
    """
    Check if there is a breakout from a Bollinger Band squeeze.
    
    A breakout occurs when:
    1. Previous bar had low volatility (bandwidth < threshold)
    2. Current price breaks above the upper band
    
    Args:
        current_bar: Current bar data
        previous_bar: Previous bar data
        squeeze_threshold: Bandwidth threshold to identify a squeeze
        
    Returns:
        bool: True if breakout detected, False otherwise
    """
    was_in_squeeze = previous_bar['bandwidth'] < squeeze_threshold
    breaks_upper_band = current_bar['close'] > current_bar['upper']
    
    return was_in_squeeze and breaks_upper_band


def check_mean_reversion(current_bar):
    """
    Check if price has reverted back to the mean (middle band).
    
    Args:
        current_bar: Current bar data
        
    Returns:
        bool: True if price is below middle band, False otherwise
    """
    return current_bar['close'] < current_bar['middle']


# --- 5. Main Logic ---

def run_bollinger_bot():
    """
    The main function for the Bollinger Bands Squeeze Bot.
    
    This bot continuously monitors for:
    - BUY Signal: Breakout from a volatility squeeze
    - SELL Signal: Mean reversion back to the middle band
    """
    print("=" * 60)
    print("🚀 Bollinger Bands Squeeze Bot is starting...")
    print(f"📈 Trading: {SYMBOL_TO_TRADE}")
    print(f"📊 BB Period: {BB_PERIOD}, Std Dev: {BB_STD_DEV}")
    print(f"🔍 Squeeze Threshold: {SQUEEZE_THRESHOLD}%")
    print(f"💰 Quantity per trade: {QTY_PER_TRADE} shares")
    print("=" * 60)
    
    while True:
        try:
            # Print timestamp
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- Check for existing position ---
            position_exists, position_qty = get_current_position(SYMBOL_TO_TRADE)

            # --- Fetch historical data ---
            df = fetch_price_data(
                SYMBOL_TO_TRADE,
                TimeFrame.Hour,
                limit=100
            )
            
            # --- Calculate Bollinger Bands ---
            df = calculate_bollinger_bands(df, BB_PERIOD, BB_STD_DEV)
            
            # --- Extract latest data points ---
            current_bar = df.iloc[-1]
            previous_bar = df.iloc[-2]

            # Display current market conditions
            print(f"💵 Price: ${current_bar['close']:.2f}")
            print(f"📊 Upper Band: ${current_bar['upper']:.2f}")
            print(f"📊 Middle Band: ${current_bar['middle']:.2f}")
            print(f"📊 Lower Band: ${current_bar['lower']:.2f}")
            print(f"📏 Bandwidth: {current_bar['bandwidth']:.2f}%")

            # --- Implement Bollinger Band Squeeze Breakout Logic ---
            
            # BUY Signal: Breakout from a squeeze
            if not position_exists:
                if check_squeeze_breakout(current_bar, previous_bar, SQUEEZE_THRESHOLD):
                    print(f"📈 BUY Signal! Breakout from squeeze detected.")
                    print(f"   Previous bandwidth: {previous_bar['bandwidth']:.2f}%")
                    print(f"   Current price: ${current_bar['close']:.2f} > Upper band: ${current_bar['upper']:.2f}")
                    place_buy_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)
                else:
                    print("⏳ Signal: No breakout signal. Waiting for squeeze breakout.")

            # SELL Signal: Price reverts back to the mean (middle band)
            elif position_exists:
                if check_mean_reversion(current_bar):
                    print(f"📉 SELL Signal! Price reverted to the middle band.")
                    print(f"   Current price: ${current_bar['close']:.2f} < Middle band: ${current_bar['middle']:.2f}")
                    place_sell_order(SYMBOL_TO_TRADE, position_qty)
                else:
                    print("💎 Signal: Holding position. Waiting for mean reversion.")

            # --- Sleep until next iteration ---
            print(f"😴 Sleeping for {LOOP_SLEEP_SECONDS} seconds...")
            time.sleep(LOOP_SLEEP_SECONDS)

        except KeyboardInterrupt:
            print("\n" + "=" * 60)
            print("🛑 Bot shutting down gracefully...")
            print("=" * 60)
            break
            
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print(f"⏳ Waiting 60 seconds before retrying...")
            time.sleep(60)


# --- 6. Entry Point ---
if __name__ == '__main__':
    run_bollinger_bot()

