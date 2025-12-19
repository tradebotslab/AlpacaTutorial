"""
Alpaca Trading Course - Lesson 28
Faster Than HTTP – Streaming Real-Time Data with WebSockets

This script demonstrates how to stream real-time market data using WebSockets
instead of polling the API. This is the professional, event-driven approach
that allows your bot to react instantly to market changes.

Key Concepts:
- WebSocket connections for real-time data streaming
- Asynchronous programming with asyncio
- Event-driven architecture
- Trade data streaming from Alpaca
"""

import asyncio
from alpaca.data.live import StockDataStream
import os
import sys


# Configuration
CONFIG_FILE = 'config.py'


def load_config():
    """
    Load API credentials from config.py file.
    
    Returns:
        tuple: (API_KEY, SECRET_KEY) if successful, exits otherwise
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Error: {CONFIG_FILE} not found!")
        print(f"   Please copy config.example.py to {CONFIG_FILE} and add your API keys.")
        sys.exit(1)
    
    try:
        # Import config as module
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", CONFIG_FILE)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return config.API_KEY, config.SECRET_KEY
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        sys.exit(1)


async def trade_handler(trade):
    """
    This function is called for every new trade data point.
    
    This is an async handler (callback) that receives trade data
    from the WebSocket stream in real-time.
    
    Args:
        trade: Trade object containing symbol, price, size, timestamp, etc.
    """
    print("=" * 60)
    print("📊 NEW TRADE RECEIVED")
    print("=" * 60)
    print(f"Symbol:    {trade.symbol}")
    print(f"Price:     ${trade.price:.2f}")
    print(f"Volume:    {trade.size:,}")
    print(f"Timestamp: {trade.timestamp}")
    print("=" * 60)
    print()


async def quote_handler(quote):
    """
    Optional handler for quote data (bid/ask prices).
    
    This demonstrates how to subscribe to quotes in addition to trades.
    Quotes show the best bid and ask prices at any moment.
    
    Args:
        quote: Quote object containing bid, ask, bid_size, ask_size, etc.
    """
    print("=" * 60)
    print("💬 NEW QUOTE RECEIVED")
    print("=" * 60)
    print(f"Symbol:    {quote.symbol}")
    print(f"Bid Price: ${quote.bid_price:.2f} (Size: {quote.bid_size:,})")
    print(f"Ask Price: ${quote.ask_price:.2f} (Size: {quote.ask_size:,})")
    print(f"Spread:    ${quote.ask_price - quote.bid_price:.2f}")
    print(f"Timestamp: {quote.timestamp}")
    print("=" * 60)
    print()


async def bar_handler(bar):
    """
    Optional handler for bar data (OHLCV - Open, High, Low, Close, Volume).
    
    Bars aggregate trades into time periods (e.g., 1-minute bars).
    
    Args:
        bar: Bar object containing open, high, low, close, volume, etc.
    """
    print("=" * 60)
    print("📈 NEW BAR RECEIVED")
    print("=" * 60)
    print(f"Symbol:    {bar.symbol}")
    print(f"Open:      ${bar.open:.2f}")
    print(f"High:      ${bar.high:.2f}")
    print(f"Low:       ${bar.low:.2f}")
    print(f"Close:     ${bar.close:.2f}")
    print(f"Volume:    {bar.volume:,}")
    print(f"Timestamp: {bar.timestamp}")
    print("=" * 60)
    print()


async def main():
    """
    Main function that sets up and runs the WebSocket data stream.
    
    This function:
    1. Loads API credentials
    2. Creates a StockDataStream client
    3. Subscribes to the data we want (trades, quotes, or bars)
    4. Starts the stream (blocking call that runs forever)
    """
    print("=" * 70)
    print("📚 Alpaca Trading Course - Lesson 28")
    print("🚀 WebSocket Real-Time Data Streaming")
    print("=" * 70)
    print()
    
    # Load API credentials
    print("🔑 Loading API credentials...")
    API_KEY, SECRET_KEY = load_config()
    print("✅ Configuration loaded!")
    print()
    
    # Instantiate the stream client
    print("🔌 Connecting to Alpaca WebSocket stream...")
    stream = StockDataStream(API_KEY, SECRET_KEY)
    print("✅ Stream client created!")
    print()
    
    # Subscribe to the data we want
    # You can subscribe to trades, quotes, or bars for one or more symbols
    print("📡 Subscribing to market data...")
    
    # Subscribe to trades for SPY and TSLA
    # Every time a trade occurs for these symbols, trade_handler will be called
    stream.subscribe_trades(trade_handler, "SPY", "TSLA")
    print("   ✅ Subscribed to TRADES for: SPY, TSLA")
    
    # Uncomment the lines below to also subscribe to quotes or bars:
    # stream.subscribe_quotes(quote_handler, "SPY", "TSLA")
    # print("   ✅ Subscribed to QUOTES for: SPY, TSLA")
    
    # stream.subscribe_bars(bar_handler, "SPY", "TSLA")
    # print("   ✅ Subscribed to BARS for: SPY, TSLA")
    
    print()
    print("=" * 70)
    print("🎯 STREAM IS NOW ACTIVE")
    print("=" * 70)
    print("Waiting for market data...")
    print("(Press Ctrl+C to stop)")
    print("=" * 70)
    print()
    
    # Start the stream
    # This is a blocking call that will run forever,
    # calling our handler functions as new data arrives
    try:
        await stream.run()
    except KeyboardInterrupt:
        print()
        print("=" * 70)
        print("🛑 Stream stopped by user")
        print("=" * 70)
    except Exception as e:
        print()
        print("=" * 70)
        print(f"❌ Error in stream: {e}")
        print("=" * 70)


if __name__ == '__main__':
    """
    Entry point for the script.
    
    asyncio.run() is used to run the async main() function.
    This handles the event loop setup and teardown automatically.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


