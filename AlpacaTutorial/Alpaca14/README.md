# Lesson 14: **Trailing Stop-Loss Bot**

Welcome to Lesson 14 of the Alpaca Trading Course! This lesson teaches you how to protect your profits using a trailing stop-loss - one of the most powerful tools in algorithmic trading. This bot automatically locks in gains as your trade moves in your favor while giving winners room to run.

## The Problem: Fixed Stop-Losses Don't Protect Profits

A fixed stop-loss protects you from losses but has a critical flaw: it doesn't move up as your trade becomes profitable. If you buy at $100 with a stop at $98, and the stock rises to $150, your stop is still at $98. If the stock drops back to $99, your stop triggers and you lose $2 despite the stock reaching $150. You watched your entire $50 profit disappear!

| Problem/Challenge | Description |
|---|---|
| **Profit Erosion** | Fixed stops don't protect unrealized gains as price moves in your favor |
| **Missed Locked Profits** | Large paper profits can disappear before being realized |
| **No Adaptive Protection** | Stop-loss doesn't adjust to favorable price movements |
| **Emotional Exits** | Without automatic trailing stops, you might exit too early or too late |

## The Solution: Trailing Stop-Loss That Moves Up With Price

The solution is a trailing stop-loss that automatically moves up as the price increases but never moves down. For example, with a 10% trailing stop: if you enter at $100, the stop starts at $90. When price rises to $110, the stop moves to $99. When price rises to $140, the stop moves to $126. If price dips to $135, the stop stays at $126 (doesn't move down). If price falls to $126, the position closes with $26 profit locked in.

### Step 14.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 14.2: Configure API Keys

1. Copy the example config:
```bash
cp config.example.py config.py
```

2. Edit `config.py` and add your Alpaca API keys.

⚠️ **NEVER commit `config.py` to Git!**

### Step 14.3: Run the Trailing Stop Bot

Execute the bot:

```bash
python trailing_stop_bot.py
```

The bot will:
- Check account information
- Check for existing positions
- Place buy orders with automatic 5% trailing stop
- Monitor positions and display P/L in real-time

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Trail Percentage** | Volatile stocks (TSLA, NVDA): 8-10%; Blue chips (SPY, AAPL): 5-7%; Conservative: 3-5% |
| **Lets Winners Run** | Trailing stops stay in trades during uptrends while protecting profits |
| **Automatic Management** | Broker manages the trailing stop 24/7, even when your bot is offline |
| **Emotion-Free** | Automated, systematic exit strategy removes emotional decision-making |
| **Paper Trading First** | Always test thoroughly in paper trading before live trading |

## Conclusion

You've successfully learned how to implement trailing stop-losses! This powerful tool protects your unrealized profits and lets winning trades run while automatically locking in gains. Trailing stops convert paper profits into realized gains and are essential for professional trading systems. In the next lesson, you'll learn how to manually implement trailing stops for more advanced control and customization.
