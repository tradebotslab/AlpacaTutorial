# Tutorial 20: The Bigger Picture – Analyzing Multiple Timeframes

## 🎯 Multi-Timeframe Analysis (MTF) – Trading Like a Professional

In this advanced tutorial, you'll learn one of the most powerful techniques used by professional traders: **Multi-Timeframe Analysis**. You will build a bot that first identifies the primary trend on a high timeframe (the Daily chart) and then looks for precise entry points on a lower timeframe (the Hourly chart).

## 📚 What You'll Learn

- What Multi-Timeframe Analysis (MTF) is and why professionals use it
- The "top-down" trading approach: Map + Compass methodology
- How to analyze Daily charts to determine the primary trend
- How to use Hourly charts for precise entry timing
- Why "trading with the trend" dramatically increases win rate
- How to implement a dual-timeframe trading bot in Python
- The concept of a "gatekeeper" filter for trade quality

## 💡 Why Multi-Timeframe Analysis is Essential

**The Problem**: Trading on a single timeframe is like navigating with only a compass. You know your immediate direction, but you can't see the overall landscape. You might be buying in what looks like a small uptrend on the hourly chart, while completely ignoring that you're in the middle of a massive, long-term downtrend on the daily chart.

**The Solution**: Use a "top-down" approach. First, identify the dominant trend on a higher timeframe. Then, use a lower timeframe to find the optimal entry point within that trend.

### Three Reasons MTF Matters:

1. **Filters Low-Probability Trades** - Eliminates trades that go against the "main current" of the market
2. **Increases Win Rate** - Trading with the primary trend significantly improves your odds
3. **Provides Context** - You understand both the big picture AND the precise timing

## 🗺️ The Two-Timeframe Strategy

Our bot uses two distinct timeframes, each with a specific purpose:

### Higher Timeframe (HTF) - The Map
**Daily Chart (D1)** - Establishes the dominant, primary trend

- **Indicator**: 50-day Simple Moving Average (SMA)
- **Rule**: If Price > 50-day SMA → Primary trend is UP
- **Rule**: If Price < 50-day SMA → Primary trend is DOWN
- **Purpose**: Tells us which direction we should be trading

### Lower Timeframe (LTF) - The Compass
**Hourly Chart (H1)** - Finds the best moment to enter

- **Indicator**: 14-period Relative Strength Index (RSI)
- **Rule**: Wait for RSI to cross above 30 (oversold recovery)
- **Purpose**: Identifies temporary "dips" or pullbacks within the primary trend

### The Trading Mantra
> **"Trade with the trend, enter on the pullback."**

This strategy only looks for BUY signals when:
1. ✅ The Daily trend is UP (price above 50-day SMA)
2. ✅ The Hourly chart shows a dip recovery (RSI crosses above 30)

## 🧮 How the Bot Works

### Step 1: Daily Chart Analysis (The Gatekeeper)
```
Fetch Daily bars → Calculate 50-day SMA → Compare current price to SMA
```

If price < SMA → **STOP**. No trades allowed. Wait for trend reversal.

If price > SMA → **PROCEED** to Step 2.

### Step 2: Check for Existing Position
```
Query API for open position → If exists, hold and wait
```

### Step 3: Hourly Chart Analysis (The Entry Signal)
```
Fetch Hourly bars → Calculate 14-period RSI → Check for oversold recovery
```

Entry Signal: Previous RSI < 30 AND Current RSI > 30

### Step 4: Execute Trade
```
Place market BUY order for configured quantity
```

## 📊 Real Example

**Scenario: TSLA on January 15, 2024**

**Daily Chart Analysis:**
- TSLA current price: $220
- 50-day SMA: $200
- **Result**: Price > SMA → Primary trend is UP ✅

**Hourly Chart Analysis:**
- Previous hour RSI: 28 (oversold)
- Current hour RSI: 33 (recovering)
- **Result**: RSI crossed above 30 → Entry signal ✅

**Bot Action:**
Both conditions are met → Place BUY order for 5 shares of TSLA

**Why This is High-Probability:**
- The overall trend is bullish (Daily chart)
- We're buying a temporary dip, not chasing a rally (Hourly chart)
- We have the "main current" of the market in our favor

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Understanding of moving averages (Tutorial 03 recommended)
- Understanding of RSI (Tutorial 10 recommended)
- Basic knowledge of timeframes

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API keys

Copy the example config file:

**Windows:**
```bash
copy config.example.py config.py
```

**Mac/Linux:**
```bash
cp config.example.py config.py
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
python mtf_bot.py
```

## 📁 File Structure

```
Alpaca20/
├── mtf_bot.py           # Main bot script
├── config.example.py    # Template for API keys
├── config.py            # Your actual keys (DO NOT COMMIT)
├── requirements.txt     # Python dependencies
├── .gitignore          # Protects your API keys
├── instructions.md     # Detailed tutorial instructions
└── README.md           # This file
```

## ⚙️ Configuration Options

You can customize the bot by editing constants in `mtf_bot.py`:

```python
# Which stock to trade
SYMBOL_TO_TRADE = "TSLA"  # Change to any symbol (SPY, AAPL, etc.)

# How many shares to buy per trade
QTY_PER_TRADE = 5  # Adjust based on your account size

# Higher Timeframe (Daily) configuration
HTF_SMA_PERIOD = 50  # Days for trend-following SMA

# Lower Timeframe (Hourly) configuration
LTF_RSI_PERIOD = 14  # Hours for RSI calculation
LTF_RSI_OVERSOLD = 30  # RSI level considered oversold

# How often to check for signals
LOOP_SLEEP_SECONDS = 300  # 5 minutes
```

## 🔍 Understanding the Code

### The Gatekeeper Pattern
The most critical part of the code is this structure:

```python
if primary_trend_is_up:
    # Only this code runs if Daily trend is bullish
    # Check hourly chart for entry
else:
    # Skip everything and wait
    continue
```

This "gatekeeper" ensures the bot NEVER buys when the primary trend is against it.

### Separate Data Fetches
The bot makes two distinct API calls:

```python
# Call 1: Daily timeframe
daily_bars = api.get_bars(SYMBOL, TimeFrame.Day, ...)

# Call 2: Hourly timeframe  
hourly_bars = api.get_bars(SYMBOL, TimeFrame.Hour, ...)
```

This separation is essential to keep the analyses independent.

### Helper Functions for Clarity
Following the "one function = one purpose" principle:

- `get_daily_trend_direction()` - Analyzes HTF
- `get_hourly_rsi_values()` - Analyzes LTF
- `check_existing_position()` - Position management
- `place_buy_order()` - Order execution

## 📈 Example Output

```
============================================================
🚀 Multi-Timeframe Bot (D1 Trend + H1 Entry) is starting...
============================================================
Symbol: TSLA
Quantity per trade: 5
HTF SMA Period: 50 days
LTF RSI Period: 14 hours
RSI Oversold Level: 30
Loop interval: 300 seconds
============================================================

--- Loop running at 2024-01-15 14:30:00 ---
📊 Analyzing Daily chart for primary trend...
✅ Primary Trend is UP (Price > 50-Day SMA).
   Looking for BUY signals on Hourly chart...
🔍 Analyzing Hourly chart for entry point...
   Previous RSI: 28.45
   Current RSI: 33.12
============================================================
📈 CONFIRMED BUY SIGNAL!
   ✅ Primary trend is UP (Daily chart)
   ✅ RSI crossed above 30 (Hourly chart)
   Placing BUY order for 5 shares of TSLA...
============================================================
✅ Order placed successfully! Order ID: 12345678-abcd-...
```

## 🎓 Educational Notes

### Why 50-Day SMA for the Daily Chart?
The 50-day SMA is a widely-watched indicator that represents the intermediate-term trend. It's slow enough to filter out noise but fast enough to catch meaningful trends.

### Why RSI on the Hourly Chart?
RSI measures momentum. On the hourly timeframe, an oversold RSI reading (< 30) often indicates a temporary pullback within a larger trend. When RSI crosses back above 30, it suggests the pullback is over and the trend is resuming.

### Why Not Exit Signals?
This tutorial focuses on the ENTRY side of multi-timeframe analysis. In a real trading system, you would add exit logic (stop-loss, take-profit, or trend reversal signals).

### The "Buy the Dip" Strategy
This bot implements a classic "buy the dip" strategy:
- It only works in an uptrend (confirmed by Daily chart)
- It waits for a temporary weakness (oversold on Hourly chart)
- It enters when the weakness shows signs of ending (RSI recovery)

## ⚠️ Risk Warnings

- ⚠️ **This bot only places BUY orders. It does NOT automatically close positions.**
- ⚠️ **Use Paper Trading first. This is an educational tool, not production-ready.**
- ⚠️ **Past performance does not guarantee future results.**
- ⚠️ **Multi-timeframe analysis improves probability but doesn't eliminate risk.**
- ⚠️ **You should add stop-loss and take-profit logic before live trading.**

## 🧪 Testing Recommendations

### Test with Different Symbols
Try symbols with different characteristics:
- **SPY** - Smooth, liquid, trending market
- **TSLA** - Volatile, momentum-driven
- **AAPL** - Large-cap, less volatile

### Test with Different Timeframes
The concept works with any two timeframes:
- **Weekly + Daily** - Swing trading
- **Daily + Hourly** - Position trading (our example)
- **4-Hour + 15-Minute** - Active trading

### Observe in Paper Trading
Let the bot run for several days and observe:
- How often does the Daily trend filter out trades?
- What's the accuracy of the Hourly entry signals?
- How many false signals occur during choppy markets?

## 🔧 Extending This Bot

### Add Exit Logic
Implement a stop-loss and take-profit:
```python
# When placing order:
api.submit_order(
    symbol=SYMBOL,
    qty=QTY,
    side='buy',
    type='market',
    time_in_force='gtc',
    order_class='bracket',
    stop_loss={'stop_price': entry_price * 0.98},  # 2% stop
    take_profit={'limit_price': entry_price * 1.05}  # 5% profit
)
```

### Add a Third Timeframe
Professional traders often use THREE timeframes:
- **Weekly** - Long-term direction
- **Daily** - Intermediate trend
- **Hourly** - Precise entry

### Add Multiple Confirmations
Require multiple LTF signals:
- RSI recovery (current)
- MACD crossover
- Volume spike

### Add Position Sizing
Integrate Tutorial 13's dynamic position sizing instead of fixed quantity.

## 📖 Related Tutorials

- **Tutorial 03** - Moving Averages (the HTF indicator)
- **Tutorial 10** - RSI Indicator (the LTF indicator)
- **Tutorial 13** - Dynamic Position Sizing (recommended addition)
- **Tutorial 14** - Trailing Stop Loss (recommended addition)

## 🐛 Troubleshooting

### Bot says "Could not determine daily trend"
**Cause**: Not enough historical data available  
**Solution**: Check if the market is open and data is available for your symbol

### Bot never finds entry signals
**Cause**: Either the Daily trend is DOWN, or the Hourly RSI never crosses 30  
**Solution**: This is normal! The bot is designed to be selective. Wait for proper conditions.

### "No position found" error when checking position
**Cause**: This is actually expected behavior (not an error)  
**Solution**: The code handles this with a try-except block

### Order is rejected
**Cause**: Market is closed, insufficient buying power, or symbol not tradeable  
**Solution**: Check Alpaca dashboard and ensure you're using paper trading

## 📚 Additional Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Multi-Timeframe Analysis Guide](https://www.investopedia.com/articles/trading/09/multiple-timeframe-analysis.asp)
- [Understanding RSI](https://www.investopedia.com/terms/r/rsi.asp)
- [Moving Average Strategies](https://www.investopedia.com/terms/m/movingaverage.asp)

## 💬 Key Takeaways

1. **Context is Everything** - A single timeframe tells only part of the story
2. **Trend is Your Friend** - Trading with the primary trend increases win rate
3. **Timing Matters** - Enter on pullbacks within the trend, not at extremes
4. **Filters Improve Quality** - The Daily trend acts as a gatekeeper for trade quality
5. **Separation of Concerns** - Use higher timeframes for direction, lower timeframes for timing

## 🎯 Next Steps

After mastering this tutorial:

1. **Let it Run** - Observe the bot in paper trading for 2-3 weeks
2. **Keep a Journal** - Document which signals work and which don't
3. **Add Exits** - Implement stop-loss and take-profit logic
4. **Test Different Parameters** - Try 20-day SMA, or different RSI levels
5. **Combine with Position Sizing** - Integrate Tutorial 13's risk management

---

## 📄 License

This is an educational project. Use at your own risk. Not financial advice.

---

**"The trend is your friend, but the pullback is your entry." - Trading Proverb**

Happy Trading! 📊🚀

