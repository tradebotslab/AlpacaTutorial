# Tutorial 16: Relative Strength – Building an RSI-Based Bot

## 📊 Mean-Reversion Trading with the RSI Indicator

In this tutorial, you'll learn how to build a **mean-reversion trading bot** using one of the most popular momentum indicators: the **Relative Strength Index (RSI)**. The bot identifies overbought and oversold market conditions and trades the expected price reversals.

## 📚 What You'll Learn

- What the Relative Strength Index (RSI) is and how it works
- How to identify overbought and oversold market conditions
- The difference between mean-reversion and trend-following strategies
- How to use the `pandas-ta` library to calculate technical indicators
- How to detect RSI crossover signals for precise entry and exit
- How to implement a complete RSI-based trading bot in Python

## 💡 What is the Relative Strength Index (RSI)?

The **RSI** is a momentum oscillator that measures the speed and change of price movements. It oscillates between 0 and 100 and is typically used to identify overbought or oversold conditions.

### RSI Readings Explained:

- **RSI > 70** → **Overbought**: The asset has moved up too far, too fast, and might be due for a corrective pullback (potential SELL signal)
- **RSI < 30** → **Oversold**: The asset has moved down too far, too fast, and might be due for a rally (potential BUY signal)
- **RSI around 50** → **Neutral**: No extreme condition, market in balance

### Our Trading Strategy:

- **BUY** when RSI crosses UP from below 30 (recovery from oversold)
- **SELL** when RSI crosses DOWN from above 70 (correction from overbought)

This is a **mean-reversion** strategy: we bet on the price returning to its average after extreme moves.

## 🎯 How the Bot Works

The bot follows this logic every minute:

1. **Check Position** - Determine if we currently hold the asset
2. **Fetch Data** - Get recent price bars (200 minutes of data)
3. **Calculate RSI** - Use `pandas-ta` to compute the 14-period RSI
4. **Detect Crossovers** - Look for RSI crossing the 30 or 70 thresholds
5. **Execute Trades** - Buy on oversold recovery, sell on overbought decline

### The Crossover Logic (Critical):

We don't just trade when RSI is below 30 or above 70. We trade when it **crosses** these levels:

- **Buy Signal**: `previous_rsi < 30` AND `current_rsi > 30` (crossing UP)
- **Sell Signal**: `previous_rsi > 70` AND `current_rsi < 70` (crossing DOWN)

This approach catches the moment momentum shifts, providing more precise entries and exits.

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Understanding of basic trading concepts
- Completion of earlier tutorials (recommended but not required)

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `alpaca-trade-api-python` - For API connection
- `pandas` - For data manipulation
- `pandas-ta` - For technical indicator calculations

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
python rsi_bot.py
```

The bot will:
- Display your account information
- Start monitoring BTC/USD every minute
- Print current price and RSI values
- Execute trades when RSI crossover signals occur
- Run continuously until you stop it (Ctrl+C)

## 📊 Bot Configuration

You can customize the bot's behavior by editing the constants at the top of `rsi_bot.py`:

```python
SYMBOL_TO_TRADE = "BTC/USD"  # Asset to trade (crypto works well with RSI)
QTY_PER_TRADE = 0.01  # Quantity per trade
RSI_PERIOD = 14  # RSI calculation period (standard is 14)
RSI_OVERBOUGHT = 70  # Overbought threshold
RSI_OVERSOLD = 30  # Oversold threshold
LOOP_SLEEP_SECONDS = 60  # Check interval in seconds
```

### Recommended Assets for RSI Strategy:

- **BTC/USD** (Bitcoin) - Volatile, reacts well to RSI signals
- **ETH/USD** (Ethereum) - High volatility, good for mean-reversion
- **SPY** (S&P 500 ETF) - Lower volatility, fewer signals
- **QQQ** (Nasdaq ETF) - Tech-heavy, moderate volatility

## 🔧 Code Structure

The script follows a clean, modular structure:

```python
# 1. Imports - All required libraries
# 2. Constants - Configuration variables
# 3. API Connection - Initialize Alpaca REST API
# 4. Helper Functions:
#    - get_account_info() - Display account details
#    - check_position() - Check if position exists
#    - get_historical_data_with_rsi() - Fetch data and calculate RSI
#    - place_buy_order() - Execute buy order
#    - place_sell_order() - Execute sell order
#    - check_rsi_signals() - Analyze RSI for trading signals
# 5. Main Logic - run_rsi_bot() orchestrates everything
# 6. Run - Entry point of the script
```

## 📈 Understanding Mean-Reversion vs Trend-Following

This RSI bot implements a **mean-reversion** strategy, which is different from **trend-following**:

| Aspect | Mean-Reversion (RSI) | Trend-Following (SMA) |
|--------|---------------------|----------------------|
| Philosophy | Price returns to average | Trend continues |
| Buy when | Oversold (low RSI) | Price crosses above average |
| Sell when | Overbought (high RSI) | Price crosses below average |
| Works best in | Range-bound markets | Trending markets |
| Typical hold time | Short (hours/days) | Longer (days/weeks) |

## 📐 The RSI Calculation

RSI is calculated using this formula:

```
RSI = 100 - (100 / (1 + RS))

Where:
RS = Average Gain / Average Loss over N periods
N = RSI period (typically 14)
```

**Good news**: You don't need to implement this! The `pandas-ta` library handles it:

```python
df['rsi'] = ta.rsi(df['close'], length=RSI_PERIOD)
```

## ⚠️ Important Trading Considerations

### Advantages of RSI Strategy:
- ✅ Works well in sideways/range-bound markets
- ✅ Identifies potential reversal points
- ✅ Simple to understand and implement
- ✅ Popular indicator with well-documented behavior

### Limitations of RSI Strategy:
- ❌ Can give false signals in strong trending markets
- ❌ RSI can stay overbought/oversold for extended periods
- ❌ Requires volatile assets to generate enough signals
- ❌ No stop-loss protection (can be added)

### Risk Management Recommendations:
1. **Start with paper trading** - Test thoroughly before using real money
2. **Use small position sizes** - Don't risk more than 1-2% per trade
3. **Add stop-losses** - Protect against extreme moves (see Tutorial 14)
4. **Combine with other indicators** - RSI works best with confirmations
5. **Monitor market conditions** - Mean-reversion fails in strong trends

## 🎓 Learning Exercises

To deepen your understanding, try these modifications:

### Beginner:
1. Change the RSI thresholds (try 80/20 instead of 70/30)
2. Adjust the RSI period (try 7 or 21 instead of 14)
3. Test with different symbols (SPY, QQQ, ETH/USD)

### Intermediate:
4. Add stop-loss orders using bracket orders (Tutorial 14)
5. Implement position sizing based on account equity (Tutorial 13)
6. Add logging to track all trades and performance

### Advanced:
7. Combine RSI with moving averages for trend confirmation
8. Implement different entry/exit thresholds (buy at 30, sell at 65)
9. Add a filter to only trade during specific market hours
10. Create a backtesting module to test historical performance

## 📝 Example Output

When running, you'll see output like this:

```
🚀 RSI Trading Bot is starting...
📋 Configuration:
   Symbol: BTC/USD
   Quantity per trade: 0.01
   RSI Period: 14
   Oversold Level: 30
   Overbought Level: 70
   Check Interval: 60 seconds

=== Account Information ===
Account Status: ACTIVE
Buying Power: $100000.00
Cash: $100000.00
Portfolio Value: $100000.00

============================================================
🕐 Loop running at 2025-12-17 14:30:00
============================================================
ℹ️  No position currently held.
📊 Current Price: $42150.50
📊 Current RSI: 28.45 | Previous RSI: 32.10
⏸️  No RSI crossover signal. Holding position.

💤 Sleeping for 60 seconds...

============================================================
🕐 Loop running at 2025-12-17 14:31:00
============================================================
ℹ️  No position currently held.
📊 Current Price: $42350.25
📊 Current RSI: 31.20 | Previous RSI: 28.45
📈 BUY Signal! RSI crossed above 30 (oversold → recovery)
✅ BUY order placed: 0.01 of BTC/USD
   Order ID: 6f7a8b9c-1d2e-3f4g-5h6i-7j8k9l0m1n2o
```

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'pandas_ta'"
**Solution**: Install the library: `pip install pandas-ta`

### "APIError: position does not exist"
**Solution**: This is expected! The bot checks for positions, and this error means there isn't one (which is fine).

### RSI values are NaN
**Solution**: Not enough data. The bot needs at least 14 bars + 1 to calculate RSI. Wait a few minutes.

### No signals are generated
**Solution**: 
- The market might not be hitting oversold/overbought levels
- Try a more volatile asset (BTC/USD, ETH/USD)
- Adjust the RSI thresholds (try 80/20 or 75/25)

### Bot stops with "insufficient buying power"
**Solution**: 
- Reduce `QTY_PER_TRADE` (try 0.001 for BTC)
- Check your account balance
- Make sure you're using paper trading URL

## 📚 Additional Resources

- [RSI on Investopedia](https://www.investopedia.com/terms/r/rsi.asp)
- [pandas-ta Documentation](https://github.com/twopirllc/pandas-ta)
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Mean-Reversion Strategies](https://www.investopedia.com/terms/m/meanreversion.asp)

## 🎯 Next Steps

After mastering this tutorial, you can:

1. **Combine Strategies** - Use RSI alongside moving averages
2. **Add Multiple Timeframes** - Check RSI on different intervals
3. **Implement Backtesting** - Test historical performance
4. **Create Alerts** - Get notified of RSI signals without auto-trading
5. **Optimize Parameters** - Find the best RSI thresholds for your asset

## 🤝 Contributing

Found a bug or have a suggestion? Feel free to open an issue or submit a pull request!

## ⚖️ Legal Disclaimer

This code is for **educational purposes only**. Trading involves substantial risk of loss. This bot:

- ❌ Is NOT investment advice
- ❌ Is NOT guaranteed to be profitable
- ❌ Should be tested thoroughly in paper trading
- ❌ May lose money in live trading

**Always use paper trading first. Never risk money you cannot afford to lose.**

## 📄 License

This project is open source and available for educational use.

---

**"The goal of a successful trader is to make the best trades. Money is secondary." - Alexander Elder**

Happy Trading! 🚀📈

