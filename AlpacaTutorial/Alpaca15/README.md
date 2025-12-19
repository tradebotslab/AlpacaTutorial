# Lesson 15: **Implementing a Trailing Stop-Loss in Code**

Welcome to Lesson 15 of the Alpaca Trading Course! This is an advanced lesson that shows you how to build your own trailing stop-loss mechanism from scratch. Instead of using the broker's built-in trailing stop, you'll write code to manually monitor your trade and adjust a standard stop-loss order upwards as the price moves in your favor.

## The Problem: Limited Control with Broker-Native Trailing Stops

While using the broker's native `trailing_stop` order class is simpler, manually implementing the logic offers more flexibility and control. For example, you could create a trailing stop that moves based on a moving average or another indicator, not just price. Understanding the mechanics of order management is also valuable for building sophisticated trading systems.

| Problem/Challenge | Description |
|---|---|
| **Limited Customization** | Broker-native trailing stops only move based on price percentage |
| **No Indicator-Based Logic** | Cannot create trailing stops based on moving averages, ATR, or other indicators |
| **Lack of Understanding** | Don't understand what happens "under the hood" with trailing stops |
| **No Advanced Control** | Cannot implement complex conditions for stop adjustments |

## The Solution: Manual Trailing Stop Implementation

The solution is to manually implement trailing stop logic: (1) enter a trade with a standard market order, (2) immediately place a separate standard stop order and save its ID, (3) in the main loop, if the position is profitable, check if the stop-loss can be moved up, (4) if it can, replace the old stop order with a new one at the higher price level, (5) repeat this process, ratcheting the stop-loss up to protect profits.

### Step 15.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 15.2: Configure Your API Keys

Copy the example config file and add your Alpaca Paper Trading API keys:

```bash
copy config.example.py config.py
```

⚠️ **Never commit your `config.py` file!**

### Step 15.3: Run the Manual Trailing Stop Bot

Execute the bot:

```bash
python manual_trail_bot.py
```

The bot will:
- Check for Golden Cross signals
- Place buy orders when signals occur
- Immediately place initial stop-loss order
- Monitor position and update stop-loss upwards as price increases
- Never move stop-loss down (only up)

### Step 15.4: Stop the Bot Safely

Press `Ctrl+C` to shut down the bot gracefully. The bot will automatically cancel any active stop-loss orders.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **State Management** | Bot needs to remember stop order ID; production bots use databases for persistence |
| **Order Replacement** | Use `api.replace_order()` for atomic updates instead of cancel + submit |
| **Only Move Up** | Critical: stop-loss can only increase, never decrease |
| **Graceful Shutdown** | Always handle Ctrl+C to cancel orphaned orders |
| **Complexity Trade-off** | Manual approach is more complex but offers more flexibility than native trailing stops |

## Conclusion

You've successfully learned how to manually implement trailing stop-losses! This advanced technique gives you complete control over stop-loss logic and helps you understand the mechanics of order management. While broker-native trailing stops are simpler and more reliable for most use cases, manual implementation is valuable for learning and for building sophisticated, custom trailing stop strategies. In the next lesson, you'll learn about using RSI (Relative Strength Index) for mean-reversion trading strategies.
