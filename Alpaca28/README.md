# 📚 Alpaca Trading Course - Lesson 28

## 🚀 Faster Than HTTP – Streaming Real-Time Data with WebSockets

### 🎯 What You Will Learn

In this lesson, you will learn how to **upgrade your bot from polling to professional, event-driven architecture** using WebSockets. You'll discover:

- ✅ Why polling is inefficient and slow
- ✅ How WebSockets enable real-time data streaming
- ✅ Setting up async handlers for market data
- ✅ Subscribing to trades, quotes, and bars
- ✅ Building event-driven trading bots

By the end of this lesson, your bot will react to market changes **instantly** instead of waiting for the next polling cycle.

---

## 📖 Why This Matters

### The Problem: Polling (HTTP Request/Response)

When your bot makes standard API calls, it follows this pattern:

1. Open a connection to the Alpaca server
2. Ask: "What's the latest price for SPY?"
3. Receive the answer
4. Close the connection
5. Wait 60 seconds
6. Repeat

**This has major drawbacks:**

- **Latency:** You only get new information when you ask for it. If the price spikes and crashes within your 60-second wait period, your bot will be completely oblivious.
- **Inefficiency:** Each request has overhead (establishing connections, sending headers). Most of the time, the price hasn't changed, making the request wasteful.
- **API Rate Limits:** Many services limit the number of requests you can make per minute. Polling aggressively can get you temporarily blocked.

### The Solution: WebSockets for Real-Time Streaming

A WebSocket connection is a **persistent, two-way communication channel** between your bot and the Alpaca server.

Instead of your bot repeatedly asking for data, **the server pushes the data to your bot the instant it becomes available.**

It's like telling the driver, "Just let me know the moment we arrive." You can relax until you get the information you need.

This is how modern, real-time applications work, and it's essential for any trading strategy that needs to react quickly to market changes.

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client with WebSocket support

### Step 2: Configure Your API Credentials

Copy the example configuration:

```bash
# Windows
copy config.example.py config.py

# macOS/Linux
cp config.example.py config.py
```

Edit `config.py` with your Alpaca API credentials:

```python
API_KEY = "YOUR_API_KEY_HERE"
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
```

⚠️ **IMPORTANT:** Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

### Step 3: Run the Stream

```bash
python websocket_stream.py
```

The script will:
1. Connect to Alpaca's WebSocket stream
2. Subscribe to real-time trade data for SPY and TSLA
3. Print trade information as it arrives in real-time
4. Run until you press Ctrl+C

---

## 📊 What the Script Does

### WebSocket Connection

The script establishes a persistent WebSocket connection to Alpaca's real-time data feed. This connection stays open and allows the server to push data to your bot instantly.

### Data Types

You can subscribe to three types of real-time data:

1. **Trades** - Individual trade executions (price, volume, timestamp)
2. **Quotes** - Best bid and ask prices (bid/ask spread)
3. **Bars** - Aggregated OHLCV data (Open, High, Low, Close, Volume)

### Current Configuration

- **Symbols:** SPY, TSLA
- **Data Type:** Trades (you can modify to include quotes and bars)
- **Handler:** Prints trade details to console in real-time

You can modify these parameters in the `main()` function.

---

## 📁 Project Structure

```
Alpaca28/
├── websocket_stream.py    # Main WebSocket streaming script
├── config.py               # Your API credentials (not tracked by git)
├── config.example.py       # Template configuration file
├── requirements.txt         # Python dependencies
├── .gitignore              # Protects your API keys
├── instructions.md         # Lesson instructions
└── README.md               # This file
```

---

## 🔍 Key Concepts Explained

### 1. Asynchronous Programming (async/await)

WebSocket streams use Python's `asyncio` library for asynchronous programming. This allows your bot to handle multiple events concurrently without blocking.

**Key Points:**
- Functions that handle stream data must be `async`
- Use `await` to wait for async operations
- `asyncio.run()` starts the event loop

**Example:**
```python
async def trade_handler(trade):
    # This function runs whenever new trade data arrives
    print(f"New trade: {trade.symbol} @ ${trade.price}")
```

### 2. Event-Driven Architecture

Instead of a `while True:` loop with `sleep()`, your bot now uses an event-driven model:

- **Old Way (Polling):**
  ```python
  while True:
      price = get_latest_price()
      check_strategy(price)
      time.sleep(60)  # Wait 60 seconds
  ```

- **New Way (WebSocket):**
  ```python
  async def trade_handler(trade):
      # This runs instantly when new data arrives
      check_strategy(trade.price)
  ```

### 3. Handler Functions (Callbacks)

Handler functions are called automatically by the stream when new data arrives. They receive the data as a parameter and execute your trading logic.

**Trade Handler:**
- Receives: `trade` object with `symbol`, `price`, `size`, `timestamp`
- Use for: Real-time price updates, volume analysis

**Quote Handler:**
- Receives: `quote` object with `bid_price`, `ask_price`, `bid_size`, `ask_size`
- Use for: Spread analysis, order book depth

**Bar Handler:**
- Receives: `bar` object with `open`, `high`, `low`, `close`, `volume`
- Use for: Technical analysis, OHLCV patterns

---

## 🔧 Customization

### Change the Symbols

Edit the `main()` function:

```python
# Subscribe to different symbols
stream.subscribe_trades(trade_handler, "AAPL", "MSFT", "GOOGL")
```

### Subscribe to Quotes

Uncomment and modify the quote subscription:

```python
stream.subscribe_quotes(quote_handler, "SPY", "TSLA")
```

### Subscribe to Bars

Uncomment and modify the bar subscription:

```python
stream.subscribe_bars(bar_handler, "SPY", "TSLA")
```

### Integrate with Your Trading Strategy

Move your strategy logic into the handler:

```python
# Global variables or a class to hold state
current_price = 0.0
moving_average = 0.0
is_in_position = False  # Loaded from state file at startup

async def trade_handler(trade):
    global current_price, moving_average, is_in_position

    # 1. Update your indicators with the new price
    current_price = trade.price
    # ... code to recalculate moving_average ...

    # 2. Check your strategy rules
    if current_price > moving_average and not is_in_position:
        print("BUY SIGNAL!")
        # ... code to submit a buy order ...
        # ... update state file and send Discord notification ...
    
    elif current_price < moving_average and is_in_position:
        print("SELL SIGNAL!")
        # ... code to submit a sell order ...
        # ... update state file and send Discord notification ...
```

---

## 🐛 Troubleshooting

### Problem: "config.py not found"

**Solution:**
```bash
# Copy the example file
copy config.example.py config.py  # Windows
cp config.example.py config.py    # macOS/Linux

# Then edit config.py with your API keys
```

### Problem: "Error connecting to stream"

**Possible Causes:**
1. Invalid API keys
2. Network connection issues
3. Alpaca API service outage

**Solutions:**
1. Verify API keys in `config.py`
2. Check your internet connection
3. Verify Alpaca API status: https://status.alpaca.markets/
4. Ensure you're using paper trading keys (not live trading keys)

### Problem: "No data is being received"

**Possible Causes:**
1. Market is closed
2. Symbols are not trading
3. Subscription not set up correctly

**Solutions:**
1. Check if market is open (9:30 AM - 4:00 PM ET, weekdays)
2. Verify symbols are valid and actively trading
3. Check that subscription is called before `stream.run()`

### Problem: "ModuleNotFoundError: No module named 'alpaca'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "RuntimeWarning: coroutine was never awaited"

**Solution:**
- Make sure handler functions are `async`
- Use `await` for async operations
- Don't call async functions directly (use `await` or `asyncio.run()`)

---

## 📊 Sample Output

```
======================================================================
📚 Alpaca Trading Course - Lesson 28
🚀 WebSocket Real-Time Data Streaming
======================================================================

🔑 Loading API credentials...
✅ Configuration loaded!

🔌 Connecting to Alpaca WebSocket stream...
✅ Stream client created!

📡 Subscribing to market data...
   ✅ Subscribed to TRADES for: SPY, TSLA

======================================================================
🎯 STREAM IS NOW ACTIVE
======================================================================
Waiting for market data...
(Press Ctrl+C to stop)
======================================================================

============================================================
📊 NEW TRADE RECEIVED
============================================================
Symbol:    SPY
Price:     $450.23
Volume:    1,500
Timestamp: 2024-01-15 14:23:45.123456+00:00
============================================================

============================================================
📊 NEW TRADE RECEIVED
============================================================
Symbol:    TSLA
Price:     $245.67
Volume:    2,300
Timestamp: 2024-01-15 14:23:45.234567+00:00
============================================================
```

---

## 📈 Next Steps

### Lesson 29: Building a Live Trading Strategy
- Integrate WebSocket data with your trading logic
- Real-time signal generation
- Order execution on live data

### Lesson 30: Advanced WebSocket Features
- Multiple symbol subscriptions
- Custom data filtering
- Error handling and reconnection logic

---

## 🎓 Key Takeaways

1. **WebSockets > Polling** – Real-time data streaming is faster and more efficient

2. **Event-Driven Architecture** – Your bot reacts to events instead of checking periodically

3. **Async/Await** – Essential for handling WebSocket streams in Python

4. **Handler Functions** – Your trading logic lives in these callback functions

5. **Instant Reaction** – Your bot can now respond to market changes the moment they happen

6. **Professional Approach** – This is how real trading systems work

7. **Foundation for Live Trading** – WebSocket streaming is required for any serious short-term trading strategy

---

## 📚 Additional Resources

### WebSocket Technology
- [WebSocket Protocol (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Async/Await Tutorial](https://realpython.com/async-io-python/)

### Alpaca API
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca Market Data API](https://alpaca.markets/docs/api-documentation/market-data-api/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-py)
- [Alpaca WebSocket Streaming](https://alpaca.markets/docs/api-documentation/market-data-api/streaming/)

### Trading Strategy Resources
- [Event-Driven Trading Systems](https://www.investopedia.com/articles/trading/08/event-driven-trading.asp)
- [Real-Time Data in Algorithmic Trading](https://www.investopedia.com/articles/active-trading/091415/real-time-data-algorithmic-trading.asp)

---

## 🔐 Security Best Practices

### ✅ What This Script Does Right

1. **No Hardcoded API Keys**
   - Keys stored in `config.py`
   - `config.py` is in `.gitignore`

2. **Paper Trading Data**
   - Uses Alpaca's paper trading environment
   - No real money at risk during testing

3. **Clear Documentation**
   - Well-commented code
   - Comprehensive README

### ⚠️ Additional Recommendations

1. **Never Commit API Keys**
   - Always use `config.example.py` as template
   - Keep `config.py` in `.gitignore`

2. **Rotate API Keys Regularly**
   - Generate new keys every 90 days

3. **Test Before Live Trading**
   - Always test WebSocket connections in paper trading first
   - Monitor for connection stability
   - Only then consider live trading

4. **Handle Disconnections**
   - Implement reconnection logic for production
   - Monitor connection health
   - Log connection events

---

## 📝 License

This is educational material for learning algorithmic trading with Alpaca API.

---

## ⚠️ Disclaimer

This script is for educational purposes only. Trading involves substantial risk of loss. Always:

- ✅ Test strategies thoroughly with paper trading
- ✅ Never risk more than you can afford to lose
- ✅ Understand the strategy before deploying
- ✅ Monitor your strategies regularly
- ✅ Be aware that WebSocket connections can drop and need reconnection logic

**Past performance does not guarantee future results.**

---

## 💬 Support

Found an issue? Have questions?

- Check the troubleshooting section above
- Review the code comments
- Check Alpaca API status: https://status.alpaca.markets/
- Review Alpaca WebSocket documentation

---

**"Risk comes from not knowing what you're doing." - Warren Buffett**

Upgrading to WebSocket streaming is a massive leap forward. Your bot is now a nimble, event-driven system capable of acting on market information the instant it becomes available! 🚀

---

*Alpaca Trading Course - Lesson 28*  
*Faster Than HTTP – Streaming Real-Time Data with WebSockets*

