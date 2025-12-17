# Tutorial 18: The Power of Momentum – Implementing a MACD Strategy

## 📈 MACD Crossover Trading – Catching Momentum Shifts

In this tutorial, you'll learn how to use one of the most popular and powerful momentum indicators in technical analysis: the **Moving Average Convergence Divergence (MACD)**. You'll build an automated trading bot that detects trend reversals and momentum shifts to generate buy and sell signals.

## 📚 What You'll Learn

- What the MACD indicator is and how it works
- The three components of MACD: MACD Line, Signal Line, and Histogram
- How to detect bullish and bearish crossovers
- How to implement MACD calculations using pandas-ta
- How to build a complete trend-following trading system
- Why MACD is more responsive than simple moving average strategies

## 💡 What is the MACD Indicator?

The MACD is a versatile **trend-following momentum indicator** that shows the relationship between two moving averages of a security's price. Unlike simple moving average crossovers, MACD uses exponential moving averages (EMAs) which are more responsive to recent price changes.

### The Three Components of MACD:

#### 1. The MACD Line (Fast)
```
MACD Line = 12-period EMA - 26-period EMA
```
This line reacts quickly to price changes and represents short-term momentum.

#### 2. The Signal Line (Slow)
```
Signal Line = 9-period EMA of MACD Line
```
This line is slower and smooths out the MACD Line, providing a clearer picture of the trend.

#### 3. The Histogram
```
Histogram = MACD Line - Signal Line
```
Visually represents the distance between the two lines. When the histogram grows, momentum is increasing.

### How MACD Generates Trading Signals:

#### Bullish Crossover (Buy Signal) 📈
When the **MACD Line crosses ABOVE the Signal Line**, it suggests momentum is shifting to the upside.
- Indicates potential start of an uptrend
- Entry signal for long positions
- Shows increasing bullish momentum

#### Bearish Crossover (Sell Signal) 📉
When the **MACD Line crosses BELOW the Signal Line**, it suggests momentum is shifting to the downside.
- Indicates potential start of a downtrend
- Exit signal for long positions
- Shows increasing bearish momentum

## 📊 Visual Understanding

```
Price going up:
MACD Line ↗️ (moving up faster)
Signal Line → (following slower)
→ BULLISH CROSSOVER → BUY

Price going down:
MACD Line ↘️ (moving down faster)
Signal Line → (following slower)
→ BEARISH CROSSOVER → SELL
```

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Basic understanding of moving averages
- Familiarity with trend-following strategies

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

**Note**: This tutorial requires `pandas-ta` library for MACD calculations.

### 2. Configure your API keys

Copy the example config file:

```bash
# Windows PowerShell
copy config.example.py config.py

# Linux/Mac
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
python macd_bot.py
```

## 📊 Trading Strategy

The bot implements a pure momentum-based trend-following system:

- **Data Timeframe**: Hourly bars (200 bars for MACD calculation)
- **Entry Signal**: Bullish MACD Crossover (MACD crosses above Signal)
- **Exit Signal**: Bearish MACD Crossover (MACD crosses below Signal)
- **Order Type**: Market orders (immediate execution)
- **Position Management**: One position at a time
- **Check Interval**: 60 seconds (configurable)

### Strategy Logic:

```
IF no position held AND bullish crossover detected:
    → BUY (enter long position)

IF position held AND bearish crossover detected:
    → SELL (exit position)

ELSE:
    → WAIT (no action)
```

## 🎯 MACD Parameters

### Standard MACD Settings (Used in this bot):

```python
MACD_FAST = 12    # Fast EMA period
MACD_SLOW = 26    # Slow EMA period
MACD_SIGNAL = 9   # Signal line EMA period
```

These are the **industry-standard parameters** developed by Gerald Appel and used by traders worldwide.

### Why These Numbers?

- **12 periods**: Captures short-term momentum (~2.5 weeks in daily data)
- **26 periods**: Captures longer-term trend (~1 month in daily data)
- **9 periods**: Smooths the MACD line to reduce false signals

⚠️ **Recommendation**: Start with standard parameters. Only adjust after extensive testing!

## ⚙️ Configuration

Edit these constants in `macd_bot.py`:

```python
SYMBOL_TO_TRADE = "MSFT"          # Stock symbol to trade
MACD_FAST = 12                     # Fast EMA (default: 12)
MACD_SLOW = 26                     # Slow EMA (default: 26)
MACD_SIGNAL = 9                    # Signal EMA (default: 9)
QTY_PER_TRADE = 10                 # Number of shares per trade
LOOP_SLEEP_SECONDS = 60            # Check interval in seconds
```

### Recommended Symbols for MACD:

- **MSFT** - Microsoft (default, steady trending)
- **AAPL** - Apple (highly liquid, clear trends)
- **SPY** - S&P 500 ETF (smooth, diversified)
- **QQQ** - Nasdaq 100 ETF (tech momentum)

MACD works best on **liquid stocks with clear trending behavior**.

## 📖 Code Structure

The code follows educational best practices with clear, descriptive functions:

### Key Functions:

#### 1. **`get_position_status(symbol)`**
- Checks if you currently hold a position
- Returns position existence and quantity
- Handles API errors gracefully

#### 2. **`fetch_market_data(symbol, timeframe, limit)`**
- Fetches historical bar data from Alpaca
- Uses hourly timeframe for MACD calculation
- Returns pandas DataFrame

#### 3. **`calculate_macd_indicator(df, fast, slow, signal)`** ← **CORE**
- Calculates MACD using pandas-ta library
- Adds MACD Line, Signal Line, and Histogram to DataFrame
- Renames columns for clarity

#### 4. **`detect_bullish_crossover(previous_bar, current_bar)`**
- Detects when MACD crosses above Signal Line
- Compares previous and current bar
- Returns True if bullish crossover occurred

#### 5. **`detect_bearish_crossover(previous_bar, current_bar)`**
- Detects when MACD crosses below Signal Line
- Compares previous and current bar
- Returns True if bearish crossover occurred

#### 6. **`place_buy_order(symbol, quantity)`**
- Submits market buy order
- Includes error handling

#### 7. **`place_sell_order(symbol, quantity)`**
- Submits market sell order
- Includes error handling

#### 8. **`run_macd_bot()`** ← **MAIN LOOP**
- Orchestrates the entire trading logic
- Continuously monitors market
- Displays detailed information about MACD values and signals

### Educational Principles:
- **Full variable names**: `current_macd`, `signal_line`, not `m`, `s`
- **WHY comments**: Explains reasoning behind the strategy
- **One action per line**: No complex nested logic
- **Extensive output**: Shows MACD values, prices, and decisions
- **Separate functions**: Each function does one thing well

## 🎓 Understanding the Output

When the bot runs, you'll see detailed information:

```
🚀 MACD Crossover Bot is starting...
📊 Trading: MSFT
⚙️ MACD Parameters: Fast=12, Slow=26, Signal=9
💰 Quantity per trade: 10 shares
⏱️ Check interval: 60 seconds

============================================================
⏰ Loop running at 2025-12-17 14:30:00
============================================================
ℹ️  No position currently held
📥 Fetching market data...

📊 Current Market Data:
   Price: $425.50
   MACD Line: 1.2345
   Signal Line: 0.9876
   Difference: 0.2469

⏸️  Signal: No bullish crossover. Waiting for entry signal.

💤 Sleeping for 60 seconds...
```

### When a Buy Signal is Detected:

```
📈 BUY SIGNAL DETECTED!
   MACD crossed above Signal Line
   Previous: MACD 0.9500 < Signal 1.0200
   Current:  MACD 1.2345 > Signal 0.9876
✅ BUY order placed: 10 shares of MSFT
```

### When a Sell Signal is Detected:

```
📉 SELL SIGNAL DETECTED!
   MACD crossed below Signal Line
   Previous: MACD 1.2000 > Signal 1.1000
   Current:  MACD 0.8500 < Signal 0.9500
✅ SELL order placed: 10 shares of MSFT
```

## 🧮 How Crossover Detection Works

### The Logic Behind Crossover Detection:

A **bullish crossover** occurs when:
1. On the **previous bar**: MACD Line < Signal Line
2. On the **current bar**: MACD Line > Signal Line
3. This means the MACD Line **crossed above** the Signal Line

A **bearish crossover** occurs when:
1. On the **previous bar**: MACD Line > Signal Line
2. On the **current bar**: MACD Line < Signal Line
3. This means the MACD Line **crossed below** the Signal Line

### Code Implementation:

```python
# Bullish Crossover Detection
def detect_bullish_crossover(previous_bar, current_bar):
    previous_macd_below = previous_bar['macd_line'] < previous_bar['signal_line']
    current_macd_above = current_bar['macd_line'] > current_bar['signal_line']
    return previous_macd_below and current_macd_above
```

This ensures we catch the **precise moment** of the cross, not just when MACD is above/below Signal.

## 📈 MACD vs Simple Moving Average Crossover

### Simple MA Crossover:
- Uses two simple moving averages (e.g., 20-day and 50-day)
- Slower to react to price changes
- More lag in signals
- Good for long-term trends

### MACD Crossover:
- Uses exponential moving averages (more weight to recent prices)
- Faster reaction to price changes
- Less lag in signals
- Better for catching momentum shifts early
- More signals (can be good or bad depending on market conditions)

**MACD is generally more responsive and catches trend changes earlier.**

## 🔒 Risk Management Considerations

This tutorial focuses on **signal generation**, not position sizing. For complete risk management, consider:

### Enhancements for Live Trading:

1. **Add Stop-Loss Orders** (Tutorial 11)
   - Protect against adverse moves
   - Limit maximum loss per trade

2. **Add Take-Profit Orders** (Tutorial 12)
   - Lock in profits at target levels
   - Ensure good risk/reward ratios

3. **Implement Dynamic Position Sizing** (Tutorial 13)
   - Risk fixed percentage of capital
   - Adapt position size to account equity

4. **Add Trailing Stops** (Tutorial 14)
   - Protect profits as trade moves in your favor
   - Let winners run while limiting losses

### Current Bot Protection:

- ✅ **Paper Trading Only** - No real money at risk
- ✅ **Single Position** - Only one trade at a time
- ✅ **Clear Entry/Exit** - Well-defined signals
- ⚠️ **No Stop-Loss** - Exits only on reverse crossover
- ⚠️ **Fixed Quantity** - Same number of shares each trade

## 🧪 Testing and Experimentation

### Experiment 1: Different Symbols

Try trending vs choppy stocks:

```python
SYMBOL_TO_TRADE = "AAPL"  # Strong trends
# vs
SYMBOL_TO_TRADE = "XYZ"   # Choppy, range-bound
```

**Observation**: MACD works best in trending markets and generates false signals in sideways markets.

### Experiment 2: Different Timeframes

```python
# In fetch_market_data() call:
TimeFrame.Hour    # Default: Better for day trading
TimeFrame.Day     # Longer trends, fewer signals
TimeFrame.Minute  # Very short-term (requires more data)
```

**Observation**: Longer timeframes = fewer but more reliable signals.

### Experiment 3: Adjust MACD Parameters

```python
# More sensitive (more signals, more noise)
MACD_FAST = 8
MACD_SLOW = 17
MACD_SIGNAL = 9

# Less sensitive (fewer signals, less noise)
MACD_FAST = 19
MACD_SLOW = 39
MACD_SIGNAL = 9
```

**Observation**: Faster parameters catch moves earlier but produce more false signals.

⚠️ **Warning**: Optimizing parameters on past data leads to overfitting. Use standard settings!

## 💡 When MACD Works Best

### ✅ Good Conditions for MACD:

- **Trending markets** (up or down)
- **Liquid stocks** (high volume)
- **Clear momentum shifts**
- **Volatile stocks** (more price movement)

### ❌ Poor Conditions for MACD:

- **Sideways markets** (range-bound)
- **Low volatility periods**
- **Extremely choppy price action**
- **News-driven sudden moves**

**Key Insight**: MACD is a trend-following indicator, so it performs best when trends are present!

## 📊 Real Example Walkthrough

Let's walk through a complete MACD trade:

### Initial State:
- Symbol: MSFT
- Price: $420
- MACD Line: -0.50
- Signal Line: 0.30
- Position: None

### Hour 1: Momentum Shifts
- Price: $422
- MACD Line: 0.10
- Signal Line: 0.25
- **Still below Signal** → Wait

### Hour 2: Bullish Crossover! 📈
- Price: $425
- MACD Line: **0.80** ← Crossed above
- Signal Line: 0.50
- **Crossover detected** → **BUY 10 shares at $425**

### Hour 3-10: Holding Position
- MACD stays above Signal
- Trend continues
- **No action** → Hold position

### Hour 11: Bearish Crossover! 📉
- Price: $438
- MACD Line: **1.20** ← Crossed below
- Signal Line: 1.50
- **Crossover detected** → **SELL 10 shares at $438**

### Trade Result:
- Entry: $425
- Exit: $438
- Profit: $13 per share × 10 shares = **$130 profit** 💰

## 🎓 Educational Philosophy

This project prioritizes **clarity over cleverness**:

- Every line is understandable for beginners
- No "magic" or hidden complexity
- Verbose, explicit code with detailed comments
- Functions named to explain their purpose
- Perfect for learning momentum trading

**Goal**: You should understand every line of code and every trading decision.

## ⚠️ Important Warnings

- **Paper Trading Only** - Uses fake money for learning
- **Not Financial Advice** - Educational purposes only
- **No Stop-Loss** - This bot doesn't limit losses (add one for live trading!)
- **Markets Are Risky** - You can lose money in real trading
- **MACD Lags** - It's a lagging indicator; signals come after moves start
- **False Signals** - MACD generates whipsaws in choppy markets

## 🔧 Troubleshooting

**Problem**: "Insufficient data" message
- **Cause**: Not enough historical bars for MACD calculation
- **Solution**: MACD needs at least 35+ bars (26 slow + 9 signal). Wait for more data or increase `limit` parameter.

**Problem**: No signals detected
- **Cause**: No crossovers occurring
- **Solution**: MACD signals are not frequent. Be patient or test during trending periods.

**Problem**: Bot connects but doesn't trade
- **Cause**: Check if market is open (U.S. stock market hours: 9:30 AM - 4:00 PM ET, Monday-Friday)
- **Solution**: Run during market hours or test with symbols that trade 24/7 (crypto, if supported).

**Problem**: "Module 'pandas_ta' not found"
- **Cause**: pandas-ta not installed
- **Solution**: Run `pip install -r requirements.txt` again.

**Problem**: API connection errors
- **Cause**: Invalid API keys
- **Solution**: Verify keys in `config.py` are correct and from Paper Trading account.

## 📚 Related Tutorials

- **Tutorial 09**: Simple Moving Average Crossover Bot
- **Tutorial 10**: Enhanced Crossover Bot
- **Tutorial 11**: Bracket Orders with Stop-Loss
- **Tutorial 12**: Take-Profit Orders
- **Tutorial 13**: Dynamic Position Sizing
- **Tutorial 14**: Trailing Stop-Loss
- **Tutorial 18**: MACD Strategy ← **You are here**

## 📝 Files in This Tutorial

- `macd_bot.py` - Main bot with MACD crossover logic
- `config.example.py` - Configuration template
- `instructions.md` - Detailed tutorial instructions
- `requirements.txt` - Python dependencies (includes pandas-ta)
- `README.md` - This comprehensive guide
- `.gitignore` - Protects your API keys

## 💡 Key Concepts Learned

1. **MACD Indicator** - Understanding the three components
2. **Exponential Moving Averages** - More responsive than simple MAs
3. **Crossover Detection** - Identifying momentum shifts
4. **Trend Following** - Riding trends until they reverse
5. **pandas-ta Library** - Using technical analysis tools in Python
6. **Signal Logic** - Translating indicators into trading decisions

## 🎯 Next Steps

After mastering MACD:
1. Combine MACD with other indicators (RSI, Volume)
2. Add proper risk management (stop-loss, position sizing)
3. Test on different timeframes and symbols
4. Learn about MACD histogram divergence
5. Study MACD zero-line crossovers
6. Backtest the strategy on historical data

## 🏆 The Professional Approach

**Amateur Trader:**
- "MACD crossed, I'll trade!"
- No risk management
- No position sizing
- Trades every signal

**Professional Trader:**
- Uses MACD as ONE input in trading system
- Combines with risk management
- Sizes positions appropriately
- Filters signals based on market conditions

**This tutorial teaches the foundation. Build on it with proper risk controls!**

## 📦 Publishing to GitHub

See `HOW_TO_PUBLISH.md` for detailed instructions on publishing this tutorial to GitHub.

Quick summary:
```powershell
cd "C:\Users\tcieslar004\OneDrive - PwC\Desktop\Projekty\AlpacaTradingCourse\AlpacaTutorial"
Remove-Item -Recurse -Force "Alpaca18\.git"
git add Alpaca18/
git commit -m "Add Tutorial 18 (Alpaca18) - MACD Strategy"
git push origin main
```

## 📞 Support

Questions or issues? Open an issue in the repository!

---

**Remember**: MACD is a powerful momentum indicator, but it's not perfect. It works best in trending markets and can generate false signals in choppy conditions. Always use proper risk management and never trade with money you can't afford to lose! 📈💰

**"The trend is your friend until the end when it bends." - Ed Seykota**


