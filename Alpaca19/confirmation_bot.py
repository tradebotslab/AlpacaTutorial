# confirmation_bot.py
# Tutorial 19: Signal Confirmation - Combining RSI and MACD

import alpaca_trade_api as tradeapi
import config
import time
import pandas as pd
import pandas_ta as ta
from datetime import datetime
from alpaca_trade_api.rest import TimeFrame

# --- API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

# --- Bot Configuration ---
SYMBOL_TO_TRADE = "AMD"
QTY_PER_TRADE = 10

# RSI Configuration
RSI_PERIOD = 14
RSI_OVERSOLD = 30

# MACD Configuration
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# General Configuration
LOOP_SLEEP_SECONDS = 60


def run_confirmation_bot():
    """Main function for the RSI + MACD Confirmation Bot."""
    print("🚀 Confirmation Bot (RSI + MACD) is starting...")
    print(f"📊 Trading: {SYMBOL_TO_TRADE}")
    print(f"📈 Strategy: RSI + MACD Signal Confirmation")
    print(f"⏱️  Loop interval: {LOOP_SLEEP_SECONDS} seconds\n")
    
    while True:
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Loop running at {now} ---")

            # --- 1. Check for existing position ---
            try:
                position = api.get_position(SYMBOL_TO_TRADE)
                position_exists = True
                print(f"✅ Position exists: {position.qty} shares of {SYMBOL_TO_TRADE}.")
            except Exception:
                position_exists = False
                print("ℹ️  No position currently held.")

            # --- 2. Fetch Historical Data ---
            barset = api.get_bars(
                SYMBOL_TO_TRADE, 
                TimeFrame.Hour, 
                limit=200, 
                adjustment='raw'
            )
            df = barset.df
            
            # --- 3. Calculate BOTH Indicators ---
            df.ta.rsi(length=RSI_PERIOD, append=True)
            df.ta.macd(
                fast=MACD_FAST, 
                slow=MACD_SLOW, 
                signal=MACD_SIGNAL, 
                append=True
            )
            
            # --- 4. Rename Columns for Clarity ---
            df.rename(columns={
                f'RSI_{RSI_PERIOD}': 'rsi',
                f'MACD_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'macd_line',
                f'MACDs_{MACD_FAST}_{MACD_SLOW}_{MACD_SIGNAL}': 'signal_line'
            }, inplace=True)
            
            # Get current and previous bars
            current_bar = df.iloc[-1]
            previous_bar = df.iloc[-2]

            # Display current market data
            print(f"💰 Price: ${current_bar['close']:.2f}")
            print(f"📊 RSI: {current_bar['rsi']:.2f}")
            print(f"📈 MACD Line: {current_bar['macd_line']:.4f}")
            print(f"📉 Signal Line: {current_bar['signal_line']:.4f}")

            # --- 5. Signal Confirmation Logic ---
            # Define the individual signals first for clarity
            rsi_buy_signal = (
                previous_bar['rsi'] < RSI_OVERSOLD and 
                current_bar['rsi'] > RSI_OVERSOLD
            )
            
            macd_buy_signal = (
                previous_bar['macd_line'] < previous_bar['signal_line'] and 
                current_bar['macd_line'] > current_bar['signal_line']
            )
            
            # Display signal status
            print(f"🔍 RSI Buy Signal: {'✅ YES' if rsi_buy_signal else '❌ NO'}")
            print(f"🔍 MACD Buy Signal: {'✅ YES' if macd_buy_signal else '❌ NO'}")
            
            # BUY Signal (Entry with Confirmation)
            if not position_exists and rsi_buy_signal and macd_buy_signal:
                print(f"\n🎯 CONFIRMED BUY SIGNAL!")
                print(f"   ✅ RSI crossed above {RSI_OVERSOLD} (oversold exit)")
                print(f"   ✅ MACD bullish crossover detected")
                print(f"   📝 Placing market buy order for {QTY_PER_TRADE} shares...")
                
                try:
                    order = api.submit_order(
                        symbol=SYMBOL_TO_TRADE,
                        qty=QTY_PER_TRADE,
                        side='buy',
                        type='market',
                        time_in_force='day'
                    )
                    print(f"   ✅ Order placed successfully! Order ID: {order.id}")
                except Exception as e:
                    print(f"   ❌ Error placing buy order: {e}")

            # SELL Signal (Exit)
            elif position_exists and \
                 previous_bar['macd_line'] > previous_bar['signal_line'] and \
                 current_bar['macd_line'] < current_bar['signal_line']:
                
                print(f"\n📉 SELL SIGNAL!")
                print(f"   ⚠️  MACD bearish crossover detected")
                print(f"   📝 Placing market sell order...")
                
                try:
                    position_qty = api.get_position(SYMBOL_TO_TRADE).qty
                    order = api.submit_order(
                        symbol=SYMBOL_TO_TRADE,
                        qty=position_qty,
                        side='sell',
                        type='market',
                        time_in_force='day'
                    )
                    print(f"   ✅ Order placed successfully! Order ID: {order.id}")
                except Exception as e:
                    print(f"   ❌ Error placing sell order: {e}")
            
            else:
                print("⏸️  Signal: No confirmed signal. Holding current position.")

            # --- Sleep ---
            print(f"\n💤 Sleeping for {LOOP_SLEEP_SECONDS} seconds...")
            time.sleep(LOOP_SLEEP_SECONDS)

        except KeyboardInterrupt:
            print("\n\n🛑 Bot shutting down gracefully...")
            print("👋 Goodbye!")
            break
            
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            print(f"⏳ Waiting 60 seconds before retrying...")
            time.sleep(60)


# --- Entry point of the script ---
if __name__ == '__main__':
    run_confirmation_bot()

