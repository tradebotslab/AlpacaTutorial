# 📚 Alpaca Trading Course - Lesson 26

## ⏰ Time Travel – The Basics of Backtesting Your Strategy

### 🎯 What You Will Learn

In this lesson, you will learn how to **backtest your trading strategies** using historical market data. Backtesting is the process of simulating your trading strategy on past data to see how it would have performed. This allows you to:

- ✅ Test strategies before risking real money
- ✅ Understand strategy performance metrics
- ✅ Compare strategies against buy-and-hold
- ✅ Identify potential risks and drawdowns
- ✅ Optimize strategy parameters

By the end of this lesson, you'll be able to answer the critical question: **"Would my strategy have made money in the past?"**

---

## 📖 Why Backtest?

### The Problem: Trading Blind

Deploying an untested strategy, even with paper money, is like setting sail without a map. You might get lucky, but you're more likely to get lost.

### The Solution: Backtesting

Backtesting allows you to answer critical questions about your strategy:

- **Would it have made money over the last year? The last five years?**
- **How much risk did it involve? What was the largest loss it would have suffered?**
- **How does it perform compared to simply buying and holding the stock?**
- **How sensitive is it to small changes in its parameters?**

The key advantage of backtesting over live paper trading is **speed**. You can simulate years of trading in seconds, allowing for rapid iteration and refinement of your ideas.

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client for fetching historical data
- `pandas` - Data manipulation
- `backtesting` - Powerful backtesting library
- `bokeh` - Interactive plotting (required by backtesting)

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

### Step 3: Run the Backtest

```bash
python backtest_strategy.py
```

The script will:
1. Fetch historical data from Alpaca
2. Run the backtest
3. Display results in the terminal
4. Open an interactive plot in your browser

---

## 📊 What the Script Does

### Strategy: Moving Average Crossover

This tutorial implements a classic **trend-following strategy**:

- **Buy Signal (Golden Cross):** When a short-term moving average (10 days) crosses **above** a long-term moving average (30 days)
- **Sell Signal (Death Cross):** When the short-term MA crosses **below** the long-term MA

### Backtest Configuration

- **Symbol:** TSLA (Tesla)
- **Period:** January 1, 2020 to December 31, 2022
- **Initial Cash:** $10,000
- **Commission:** 0.2% per trade

You can modify these parameters in the `main()` function.

---

## 📁 Project Structure

```
Alpaca26/
├── backtest_strategy.py    # Main backtesting script
├── config.py               # Your API credentials (not tracked by git)
├── config.example.py       # Template configuration file
├── requirements.txt         # Python dependencies
├── .gitignore              # Protects your API keys
├── instructions.md         # Lesson instructions
└── README.md               # This file
```

---

## 🔍 Code Walkthrough

### 1. Fetching Historical Data

```python
def get_historical_data(symbol, start_date, end_date, api_key, secret_key):
    """
    Fetches historical OHLCV data from Alpaca.
    """
    client = StockHistoricalDataClient(api_key, secret_key)
    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date
    )
    bars = client.get_stock_bars(request_params)
    df = bars.df
    
    # Rename columns to match backtesting.py requirements
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)
    
    return df
```

**Key Points:**
- ✅ Uses Alpaca's Market Data API
- ✅ Fetches daily OHLCV (Open, High, Low, Close, Volume) data
- ✅ Formats data for backtesting.py library

### 2. Strategy Definition

```python
class SmaCross(Strategy):
    short_ma_period = 10
    long_ma_period = 30

    def init(self):
        # Pre-calculate indicators
        self.short_ma = self.I(SMA, self.data.Close, self.short_ma_period)
        self.long_ma = self.I(SMA, self.data.Close, self.long_ma_period)

    def next(self):
        # Trading logic
        if crossover(self.short_ma, self.long_ma):
            if not self.position:
                self.buy()
        elif crossover(self.long_ma, self.short_ma):
            if self.position:
                self.sell()
```

**Key Points:**
- ✅ `init()`: Called once at start, pre-calculates indicators
- ✅ `next()`: Called for each data point, implements trading logic
- ✅ `crossover()`: Helper function that detects when one series crosses another

### 3. Running the Backtest

```python
bt = Backtest(
    data,              # Historical data
    SmaCross,          # Strategy class
    cash=10000,        # Initial cash
    commission=0.002   # 0.2% commission
)

stats = bt.run()
bt.plot()  # Opens interactive plot
```

**Key Points:**
- ✅ Simple API: just pass data and strategy
- ✅ Automatically handles position sizing, commissions, and slippage
- ✅ Generates comprehensive performance metrics

---

## 📈 Understanding the Results

### Key Metrics Explained

| Metric | Description |
|--------|-------------|
| **Return** | Total percentage gain or loss for the strategy over the entire period |
| **Buy & Hold Return** | Return you would have gotten if you just bought the asset at the start and sold at the end. This is your benchmark. |
| **Max. Drawdown** | Largest percentage drop from a portfolio peak to a subsequent trough. This is a key measure of risk. |
| **Sharpe Ratio** | Measure of risk-adjusted return. Higher is generally better. It tells you how much return you got for the amount of risk you took. |
| **# Trades** | Total number of trades executed. Too few might mean results aren't statistically significant. Too many might mean you're losing a lot to commissions. |
| **Win Rate** | Percentage of profitable trades |
| **Avg. Trade** | Average return per trade |

### The Interactive Plot

The `bt.plot()` command generates and opens an interactive HTML file in your browser. This plot shows:

- **Equity Curve:** Portfolio value over time
- **Buy/Sell Signals:** Markers showing when trades were executed
- **Moving Averages:** Visual representation of the indicators
- **Price Chart:** Underlying asset price

---

## 🎯 Trading Strategy Details

### Moving Average Crossover (Golden Cross / Death Cross)

This is a classic trend-following strategy:

- **Golden Cross:** Short MA crosses above long MA → **BUY signal**
- **Death Cross:** Short MA crosses below long MA → **SELL signal**

### Strategy Parameters

You can modify the strategy parameters in the `SmaCross` class:

```python
class SmaCross(Strategy):
    short_ma_period = 10   # Try: 5, 10, 20
    long_ma_period = 30    # Try: 20, 30, 50, 100
```

**Experiment with different values** to see how they affect performance!

---

## 🔧 Customization

### Change the Symbol

Edit the `main()` function:

```python
SYMBOL = "SPY"  # Change from TSLA to SPY, AAPL, etc.
```

### Change the Time Period

```python
START_DATE = datetime(2018, 1, 1)  # Start earlier
END_DATE = datetime(2023, 12, 31)   # End later
```

### Change Initial Capital

```python
INITIAL_CASH = 50000  # Start with $50,000 instead of $10,000
```

### Change Commission

```python
COMMISSION = 0.001  # 0.1% commission (more realistic for some brokers)
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

### Problem: "Error fetching data"

**Possible Causes:**
1. Invalid API keys
2. Symbol not available on Alpaca
3. Network connection issues

**Solutions:**
1. Verify API keys in `config.py`
2. Check if symbol is valid (must be supported by Alpaca)
3. Check your internet connection
4. Verify Alpaca API status: https://status.alpaca.markets/

### Problem: "No module named 'backtesting'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Plot doesn't open in browser

**Solution:**
- The plot is saved as an HTML file
- Check the current directory for a file like `backtest_*.html`
- Open it manually in your browser

### Problem: "Not enough data" error

**Solution:**
- The strategy needs enough historical data to calculate moving averages
- Try a longer time period or shorter MA periods
- Ensure your date range has enough trading days

---

## 📊 Sample Output

```
======================================================================
📚 Alpaca Trading Course - Lesson 26
📖 Time Travel – The Basics of Backtesting Your Strategy
======================================================================

🔑 Loading API credentials...
✅ Configuration loaded!

📊 Backtest Configuration:
   Symbol: TSLA
   Period: 2020-01-01 to 2022-12-31
   Initial Cash: $10,000.00
   Commission: 0.20%
   Strategy: Moving Average Crossover (10/30)

📊 Fetching historical data for TSLA...
   From: 2020-01-01
   To: 2022-12-31
✅ Fetched 755 days of data

🚀 Running backtest...

📈 BUY signal at 2020-02-07 - Price: $149.97
📉 SELL signal at 2020-03-05 - Price: $140.00
📈 BUY signal at 2020-04-14 - Price: $158.00
...

======================================================================
📊 BACKTEST RESULTS
======================================================================

💰 Return: 45.23%
📈 Buy & Hold Return: 38.12%
📉 Max. Drawdown: -12.45%
📊 Sharpe Ratio: 1.85
🔢 # Trades: 24
✅ Win Rate: 58.33%
📊 Avg. Trade: 1.88%
📈 Best Trade: 15.23%
📉 Worst Trade: -8.45%

======================================================================
✅ Strategy outperformed Buy & Hold by 7.11%
======================================================================

📈 Generating interactive plot...
   (This will open in your default web browser)

✅ Backtest complete!
```

---

## 📈 Next Steps

### Lesson 27: Strategy Optimization
- Optimize strategy parameters
- Walk-forward analysis
- Parameter sensitivity testing

### Lesson 28: Advanced Backtesting
- Multiple timeframes
- Portfolio backtesting
- Risk-adjusted metrics

### Lesson 29: Live Trading Integration
- Deploy backtested strategies
- Paper trading validation
- Real-time monitoring

---

## 🎓 Key Takeaways

1. **Backtesting is Essential** – Never deploy a strategy without testing it first

2. **Speed Advantage** – Backtesting allows you to test years of trading in seconds

3. **Key Metrics Matter** – Focus on:
   - Return vs. Buy & Hold
   - Max Drawdown (risk)
   - Sharpe Ratio (risk-adjusted return)
   - Win Rate and Avg Trade

4. **Past Performance ≠ Future Results** – A positive backtest doesn't guarantee future profits, but a negative backtest is a strong signal to go back to the drawing board

5. **Iterate Quickly** – Use backtesting to rapidly test and refine ideas

6. **Visualization is Powerful** – The interactive plot helps you understand when and why trades were made

---

## 📚 Additional Resources

### Backtesting Library
- [backtesting.py Documentation](https://kernc.github.io/backtesting.py/)
- [backtesting.py GitHub](https://github.com/kernc/backtesting.py)

### Alpaca API
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca Market Data API](https://alpaca.markets/docs/api-documentation/market-data-api/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-py)

### Trading Strategy Resources
- [Moving Average Crossover Strategy](https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp)
- [Technical Analysis Basics](https://www.investopedia.com/technical-analysis-4689657)

### Performance Metrics
- [Sharpe Ratio Explained](https://www.investopedia.com/terms/s/sharperatio.asp)
- [Maximum Drawdown](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)

---

## 🔐 Security Best Practices

### ✅ What This Script Does Right

1. **No Hardcoded API Keys**
   - Keys stored in `config.py`
   - `config.py` is in `.gitignore`

2. **Paper Trading Data**
   - Uses Alpaca's free historical data
   - No real money at risk during backtesting

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
   - Always backtest first
   - Then paper trade
   - Only then consider live trading

---

## 📝 License

This is educational material for learning algorithmic trading with Alpaca API.

---

## ⚠️ Disclaimer

This script is for educational purposes only. Trading involves substantial risk of loss. Always:

- ✅ Test strategies thoroughly with backtesting
- ✅ Paper trade before using real money
- ✅ Never risk more than you can afford to lose
- ✅ Understand the strategy before deploying
- ✅ Monitor your strategies regularly

**Past performance does not guarantee future results.**

---

## 💬 Support

Found an issue? Have questions?

- Check the troubleshooting section above
- Review the code comments
- Check Alpaca API status: https://status.alpaca.markets/
- Review backtesting.py documentation

---

**"Risk comes from not knowing what you're doing." - Warren Buffett**

Backtesting is your map before you set sail. Use it wisely! ⏰

---

*Alpaca Trading Course - Lesson 26*  
*Time Travel – The Basics of Backtesting Your Strategy*

