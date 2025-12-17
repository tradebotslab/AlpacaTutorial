# Tutorial 15: Implementing a Trailing Stop-Loss in Code

## 🎯 Manual Trailing Stop – Understanding Order Management

This is an advanced tutorial that shows you how to build your own trailing stop-loss mechanism from scratch. Instead of using the broker's built-in trailing stop, you will write the code to manually monitor your trade and adjust a standard stop-loss order upwards as the price moves in your favor.

## 📚 What You'll Learn

- How to manually implement a trailing stop-loss from scratch
- Order state management and why it's critical
- How to replace orders atomically using the Alpaca API
- The mechanics of what happens "under the hood" with trailing stops
- How to handle graceful shutdown to prevent orphaned orders
- When to use manual logic vs. broker-native order types
- Advanced order management techniques for production bots

## 💡 Why Manually Implement a Trailing Stop?

While using the broker's native `trailing_stop` order class is simpler and more reliable, manually implementing the logic can offer more flexibility and control. For example, you could create a trailing stop that moves based on a moving average or another indicator, not just price.

**This tutorial is a valuable exercise in understanding the mechanics of order management and what happens "under the hood."**

### The Manual Logic:

1. **Enter a trade** with a standard market order
2. **Immediately place** a separate, standard stop order and save its ID
3. **In the main loop**, if the position is profitable, check if the stop-loss can be moved up
4. **If it can**, cancel the old stop order and submit a new one at the higher price level
5. **Repeat this process**, ratcheting the stop-loss up to protect profits

## 🧠 The Challenge: Managing State

This is more complex because the bot now needs to manage its **"state"**. It must remember the ID of its active stop-loss order to be able to modify it. If the bot restarts, this state is lost. For this tutorial, we will store the ID in a simple variable while the bot is running.

**Key Insight**: A production-grade bot would need a database or file to persist its state across restarts.

## 🔍 How It Works

### State Management (`active_stop_order_id`)
We use a global variable to store the ID of our stop-loss order. When we have a position, this variable is our key to finding and modifying the correct order. When the position is closed, we reset it to `None`.

### Managing the Trail (`if new_stop_price > existing_stop_price`)
This is the core logic. In each loop where we have a position, we calculate a potential new stop price based on the current market price. We only act if this new price is **higher** than our existing stop price. This ensures the stop only moves up, never down.

### Replacing the Order (`api.replace_order`)
Instead of manually canceling and then submitting, the Alpaca API provides a convenient `replace_order` method. This **atomically** replaces an existing order with a new one. Here, we use it to change just the `stop_price` of our existing stop-loss order to the new, higher value.

### Placing the Initial Stop (`api.submit_order(type='stop')`)
After the bot buys shares, it immediately submits a separate sell order with `type='stop'`. This is our initial safety net. We immediately save its ID to our `active_stop_order_id` variable so the next loop can begin monitoring it. We use `'gtc'` (Good 'til Canceled) so it doesn't expire at the end of the day.

### Graceful Shutdown (`KeyboardInterrupt`)
It's crucial to handle shutdown gracefully. If you stop the bot with Ctrl+C, it now attempts to cancel any active stop-loss order so you aren't left with an orphaned order in your account.

## ⚠️ Important Considerations

### Complexity and Risk
This manual approach is significantly more complex and has more potential points of failure than using a native, broker-side trailing stop. Network issues, API errors, or bugs in your code could lead to your stop-loss not being updated correctly.

### Statelessness
If this bot script stops and restarts, it will lose the `active_stop_order_id` and will not be able to manage the existing trade. A production-grade bot would need a database or file to persist its state.

### Educational Purpose
**This tutorial is a powerful demonstration of order management concepts.** For most real-world use cases, the native `'trailing_stop'` order class is the safer and more reliable choice.

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Understanding of stop-loss orders
- Basic knowledge of moving averages (Golden Cross strategy)

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API keys

Copy the example config file:

```bash
copy config.example.py config.py
```

Then edit `config.py` and add your Alpaca Paper Trading API keys:

```python
API_KEY = "YOUR_PAPER_TRADING_API_KEY"
SECRET_KEY = "YOUR_PAPER_TRADING_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"
```

⚠️ **Never commit your `config.py` file!** It's already in `.gitignore`.

### 3. Run the bot

```bash
python manual_trail_bot.py
```

### 4. Stop the bot safely

Press `Ctrl+C` to shut down the bot gracefully. The bot will automatically cancel any active stop-loss orders.

## 📊 Bot Configuration

The bot uses several constants that you can adjust:

```python
SYMBOL_TO_TRADE = "AAPL"              # Stock symbol to trade
QTY_PER_TRADE = 10                    # Number of shares per trade
TRAIL_PERCENTAGE = 3.0                # Trailing stop distance (3%)
LOOP_SLEEP_SECONDS = 30               # Check price every 30 seconds
```

## 🎓 Understanding the Code Flow

### When No Position Exists:
1. Bot checks for Golden Cross signal (20 SMA crosses above 50 SMA)
2. If signal detected, places market buy order
3. Waits for order to fill
4. Immediately places initial stop-loss order 3% below entry price
5. Saves the stop order ID for future management

### When Position Exists:
1. Gets current market price
2. Calculates potential new stop price (3% below current price)
3. Compares with existing stop price
4. If new stop is higher, replaces the old stop order
5. If not, leaves the stop unchanged
6. Repeats every 30 seconds

### Visual Example:

```
Entry Price: $100
Initial Stop: $97 (3% below)

Price moves to $105 → New Stop: $101.85 (3% below $105) ✅ Updated
Price moves to $110 → New Stop: $106.70 (3% below $110) ✅ Updated
Price drops to $108 → New Stop would be $104.76, but existing is $106.70 ❌ Not updated
Price drops to $106.70 → Stop is hit, position closed automatically
```

## 🔧 Key Functions Explained

### `check_for_golden_cross_signal(symbol)`
Checks if a Golden Cross (bullish signal) has occurred by comparing 20-day and 50-day SMAs.

### `place_initial_stop_loss(symbol, quantity, entry_price, trail_percentage)`
Places the first protective stop-loss order immediately after entering a position.

### `update_trailing_stop(symbol, stop_order_id, current_price, trail_percentage)`
The core trailing logic - checks if the stop should move up and updates it if necessary.

### `manage_existing_position(symbol, stop_order_id, trail_percentage)`
Orchestrates the management of an active position and its trailing stop.

### `enter_long_position(symbol, quantity, trail_percentage)`
Handles the complete entry process: buy order + initial stop placement.

## 📈 Example Output

```
============================================================
🚀 Manual Trailing Stop Bot is starting...
📊 Symbol: AAPL
📏 Trail Percentage: 3.0%
⏱️ Loop Interval: 30 seconds
============================================================

============================================================
🕐 Loop running at 2024-01-15 10:00:00
============================================================
ℹ️ No position held. Analyzing for entry signal...
📈 Golden Cross Detected! Placing BUY order for 10 shares.
✅ Buy order submitted: abc123
⏳ Waiting 5 seconds for buy order to fill...
✅ Position entered at $150.00
📍 Placing initial stop-loss at $145.50
✅ Initial stop-loss order placed with ID: stop123

============================================================
🕐 Loop running at 2024-01-15 10:00:30
============================================================
✅ Position exists: 10 shares at $150.00
💵 Current price: $152.00
📈 Adjusting stop-loss upwards: $145.50 → $147.44
✅ Stop-loss successfully updated to $147.44

============================================================
🕐 Loop running at 2024-01-15 10:01:00
============================================================
✅ Position exists: 10 shares at $150.00
💵 Current price: $151.50
ℹ️ Price has not moved up enough. Stop remains at $147.44
```

## 🛡️ Risk Management Features

- **Immediate Stop Placement**: Stop-loss is placed within 5 seconds of entry
- **Always Protected**: You're never in a position without a stop-loss
- **Profit Locking**: Stop moves up automatically as price increases
- **Never Moves Down**: Stop can only increase, never decrease
- **Graceful Shutdown**: Ctrl+C cancels orphaned orders
- **Error Recovery**: Bot resets state and continues on errors

## 🎯 When to Use Manual vs. Native Trailing Stops

### Use Native `trailing_stop` Order When:
- ✅ You want the simplest, most reliable solution
- ✅ Your trailing logic is based purely on price
- ✅ You need the broker to manage the stop 24/7
- ✅ You want to minimize code complexity

### Use Manual Trailing Stop When:
- ✅ You need custom trailing logic (e.g., based on indicators)
- ✅ You want to learn order management mechanics
- ✅ You need complex conditions for stop adjustments
- ✅ You're building a sophisticated portfolio management system

## 🔬 Extending This Bot

This manual trailing stop bot can be extended in many ways:

1. **Indicator-Based Trailing**: Move stop based on moving averages or ATR
2. **Multiple Positions**: Manage stops for multiple symbols simultaneously
3. **Partial Profit Taking**: Close portions of position at different levels
4. **State Persistence**: Save state to a database for restart capability
5. **Time-Based Stops**: Implement time-based stop adjustments
6. **Volatility-Adjusted Trails**: Adjust trail percentage based on market volatility

## 📚 Related Tutorials

- **Tutorial 12**: Bracket Orders (simpler stop-loss implementation)
- **Tutorial 13**: Dynamic Position Sizing (proper risk management)
- **Tutorial 14**: Native Trailing Stops (broker-side implementation)

## ⚠️ Disclaimer

This bot is for **educational purposes only** and uses **paper trading**. Never trade with real money until you fully understand the risks and have thoroughly tested your strategy. Past performance does not guarantee future results.

**Key Risks:**
- This manual approach has more failure points than native trailing stops
- Network issues could prevent stop updates
- Bot restarts lose state and cannot manage existing trades
- Code bugs could result in incorrect stop placement

## 🐛 Troubleshooting

### "No position held" but I have shares
- Check if you're using the correct symbol
- Verify you're connected to the right account (paper vs. live)

### Stop-loss isn't updating
- Check that the price is actually moving up
- Verify the bot is running and not sleeping
- Check for API errors in the console output

### "Position exists but no stop order ID"
- This means state was lost (e.g., bot restarted)
- Manually close the position or cancel the orphaned stop
- Restart the bot to begin fresh

### Bot crashes on startup
- Verify your API keys in `config.py`
- Check that dependencies are installed: `pip install -r requirements.txt`
- Ensure you have an active internet connection

## 💡 Learning Objectives

After completing this tutorial, you should understand:

- ✅ How to track and manage order state in a trading bot
- ✅ The mechanics of order replacement and atomic updates
- ✅ Why broker-native order types are often preferable
- ✅ How to implement graceful shutdown procedures
- ✅ The trade-offs between flexibility and reliability
- ✅ How professional trading systems manage order lifecycles

## 📖 Further Reading

- [Alpaca API Order Documentation](https://alpaca.markets/docs/api-references/trading-api/orders/)
- [Order Lifecycle Management](https://alpaca.markets/learn/order-lifecycle/)
- [Trailing Stop Order Types](https://alpaca.markets/learn/trailing-stop-orders/)

## 📄 License

This tutorial is provided as-is for educational purposes. Use at your own risk.

---

**"The goal of a successful trader is to make the best trades. Money is secondary." - Alexander Elder**

---

## 🙋 Questions or Issues?

If you encounter any problems or have questions about this tutorial, please check:
1. Your API keys are correct in `config.py`
2. You're using the paper trading URL
3. All dependencies are installed
4. The market is open for trading

Happy learning! 🚀

