# 📊 Tutorial 17: The Magic of Volatility – A Bollinger Bands® Bot

## 🎯 What You'll Learn

In this tutorial, you'll build an advanced trading bot that capitalizes on **volatility changes** using **Bollinger Bands®**. You'll implement a powerful "squeeze breakout" strategy that aims to catch explosive price moves right as they begin.

### Key Concepts Covered:
- ✅ Understanding Bollinger Bands® and volatility measurement
- ✅ Identifying volatility "squeezes" (consolidation periods)
- ✅ Detecting breakouts from low-volatility periods
- ✅ Implementing mean reversion exits
- ✅ Using the `pandas-ta` library for technical indicators

---

## 📚 What are Bollinger Bands®?

Bollinger Bands® are a volatility indicator consisting of **three lines**:

1. **Middle Band**: A Simple Moving Average (SMA) of the price
2. **Upper Band**: The middle band + 2 standard deviations
3. **Lower Band**: The middle band - 2 standard deviations

### The "Squeeze" Phenomenon

A **squeeze** occurs when volatility contracts (bands narrow). This typically happens before significant price moves.

- **Bands Narrow** → Low volatility → Consolidation → **Potential breakout incoming**
- **Bands Widen** → High volatility → Strong trending move

---

## 🎲 The Strategy

### Entry Signal (BUY):
1. **Previous bar** showed low volatility (bandwidth < threshold)
2. **Current price** breaks above the upper band
3. **Action**: Buy to catch the breakout momentum

### Exit Signal (SELL):
1. Price reverts below the middle band (mean reversion)
2. **Action**: Sell to lock in profits or cut losses

---

## 🛠️ Prerequisites

### Python Libraries:
- `alpaca-trade-api` - For executing trades
- `pandas` - For data manipulation
- `pandas-ta` - For technical indicators

### Alpaca Account:
- Paper trading account (recommended for learning)
- API keys (get them from [alpaca.markets](https://alpaca.markets))

---

## 📁 Project Setup

### Step 1: Clone or Download This Tutorial

```bash
cd alpaca_bot_project
# This folder should contain all Tutorial 17 files
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Your API Keys

1. Copy the example configuration:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` with your API credentials:
   ```python
   API_KEY = "your_actual_api_key_here"
   SECRET_KEY = "your_actual_secret_key_here"
   BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading
   ```

⚠️ **IMPORTANT**: Never commit `config.py` to Git! It's protected by `.gitignore`.

---

## 🚀 Running the Bot

### Start the bot:

```bash
python bollinger_bot.py
```

### What you'll see:

```
============================================================
🚀 Bollinger Bands Squeeze Bot is starting...
📈 Trading: NVDA
📊 BB Period: 20, Std Dev: 2.0
🔍 Squeeze Threshold: 4.0%
💰 Quantity per trade: 5 shares
============================================================

--- Loop running at 2025-12-17 14:30:00 ---
ℹ️ No position currently held.
📊 Fetched 100 bars for NVDA.
✅ Bollinger Bands calculated successfully.
💵 Price: $145.32
📊 Upper Band: $147.50
📊 Middle Band: $143.00
📊 Lower Band: $138.50
📏 Bandwidth: 3.2%
⏳ Signal: No breakout signal. Waiting for squeeze breakout.
😴 Sleeping for 60 seconds...
```

### Stop the bot:
Press `Ctrl+C` to gracefully shut down the bot.

---

## 🔧 Configuration Parameters

You can adjust these constants in `bollinger_bot.py`:

```python
SYMBOL_TO_TRADE = "NVDA"           # Stock to trade
BB_PERIOD = 20                      # Bollinger Band period (bars)
BB_STD_DEV = 2.0                    # Standard deviations
SQUEEZE_THRESHOLD = 4.0             # Bandwidth % to identify squeeze
QTY_PER_TRADE = 5                   # Shares per trade
LOOP_SLEEP_SECONDS = 60             # Seconds between checks
```

### 💡 Tuning Tips:

- **SQUEEZE_THRESHOLD**: Lower values = stricter squeeze detection
  - Try `3.0` for more signals (more trades)
  - Try `5.0` for fewer signals (higher quality setups)
  
- **BB_PERIOD**: Shorter = more sensitive to recent prices
  - `10-15`: Scalping / intraday
  - `20`: Standard (most common)
  - `50+`: Longer-term trend following

- **TimeFrame**: Adjust the timeframe in the code
  - `TimeFrame.Minute` - Very short-term
  - `TimeFrame.Hour` - Medium-term (current)
  - `TimeFrame.Day` - Swing trading

---

## 📖 Understanding the Code

### Main Components:

#### 1. **Position Checking**
```python
position_exists, position_qty = get_current_position(SYMBOL_TO_TRADE)
```
Checks if we already have a position open.

#### 2. **Data Fetching**
```python
df = fetch_price_data(SYMBOL_TO_TRADE, TimeFrame.Hour, limit=100)
```
Fetches 100 hourly bars to calculate indicators.

#### 3. **Bollinger Bands Calculation**
```python
df = calculate_bollinger_bands(df, BB_PERIOD, BB_STD_DEV)
```
Uses `pandas-ta` to calculate all Bollinger Band components.

#### 4. **Squeeze Breakout Detection**
```python
if check_squeeze_breakout(current_bar, previous_bar, SQUEEZE_THRESHOLD):
    place_buy_order(SYMBOL_TO_TRADE, QTY_PER_TRADE)
```
Buys when price breaks out from a low-volatility squeeze.

#### 5. **Mean Reversion Exit**
```python
if check_mean_reversion(current_bar):
    place_sell_order(SYMBOL_TO_TRADE, position_qty)
```
Sells when price reverts to the middle band.

---

## ⚠️ Risk Warnings

### This is an Educational Bot:
- ✅ Use **paper trading** to learn without risk
- ✅ Understand the strategy before using real money
- ✅ Test extensively with different parameters

### Important Considerations:
- ⚠️ **Volatility strategies can have whipsaws** (false breakouts)
- ⚠️ **Not all squeezes lead to breakouts**
- ⚠️ **Always use position sizing appropriate for your account**
- ⚠️ Consider adding stop-loss protection
- ⚠️ Monitor for extended drawdowns

---

## 🎓 Learning Exercises

### Beginner:
1. Run the bot in paper trading for 1 week
2. Observe which squeeze breakouts succeed vs. fail
3. Experiment with different `SQUEEZE_THRESHOLD` values

### Intermediate:
1. Add a stop-loss exit (e.g., 2% below entry)
2. Track win rate and average profit/loss per trade
3. Test on different symbols (SPY, QQQ, TSLA)

### Advanced:
1. Implement a "failed breakout" detection (reversal signal)
2. Add volume confirmation (high volume on breakout)
3. Combine with another indicator (RSI, MACD)
4. Add a trailing stop instead of fixed mean reversion exit

---

## 📊 Performance Tracking

Monitor these metrics to evaluate the strategy:

- **Win Rate**: % of profitable trades
- **Average Win vs. Average Loss**: Profit factor
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted returns
- **Total Trades**: Sample size for statistical significance

---

## 🐛 Troubleshooting

### Error: "No data returned"
- Check if the market is open
- Verify the symbol exists and is tradable
- Try a different symbol

### Error: "Insufficient buying power"
- Reduce `QTY_PER_TRADE`
- Check your paper trading account balance

### Bot not finding squeezes:
- Increase `SQUEEZE_THRESHOLD` (e.g., from 4.0 to 5.0)
- Try a more volatile symbol
- Change timeframe to a shorter period

### False breakouts:
- Decrease `SQUEEZE_THRESHOLD` (more restrictive)
- Add volume confirmation
- Require multiple consecutive bars above the band

---

## 📚 Next Steps

After mastering this tutorial, explore:

- **Tutorial 18**: Combining multiple indicators (pending)
- **Tutorial 19**: Machine learning for trade filtering (pending)
- **Tutorial 20**: Portfolio management and multi-asset strategies (pending)

---

## 🔐 Security Reminders

- ✅ `config.py` is in `.gitignore` (your keys are safe)
- ✅ Never share your API keys
- ✅ Use paper trading for all educational purposes
- ✅ Regenerate keys if accidentally exposed

---

## 📞 Support & Resources

- **Alpaca Documentation**: [alpaca.markets/docs](https://alpaca.markets/docs)
- **pandas-ta Documentation**: [github.com/twopirllc/pandas-ta](https://github.com/twopirllc/pandas-ta)
- **Bollinger Bands®**: Original work by John Bollinger

---

## 📝 License

This is educational content. Use at your own risk.

**"The stock market is filled with individuals who know the price of everything, but the value of nothing." - Philip Fisher**

---

## 🎉 Congratulations!

You've built a sophisticated volatility-based trading bot! You now understand:
- How to measure and use volatility in trading
- The power of squeeze breakout strategies
- Mean reversion concepts
- Technical indicator libraries in Python

Keep learning, keep testing, and most importantly—manage your risk! 🚀

