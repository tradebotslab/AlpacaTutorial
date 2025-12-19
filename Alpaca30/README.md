# 📚 Alpaca Trading Course - Lesson 30

## 🚀 A Step Towards PRO – Statistical Arbitrage (Pairs Trading)

### 🎯 What You Will Learn

In this final lesson, you will learn about **pairs trading**, a market-neutral statistical arbitrage strategy used by professional quantitative traders. Unlike directional strategies that bet on market direction, pairs trading profits from temporary distortions in the price relationship between two highly correlated assets.

You'll discover:

- ✅ What pairs trading is and why it's market-neutral
- ✅ The concept of cointegration and how to test for it
- ✅ How to calculate and trade the "spread" between two assets
- ✅ Implementing a complete pairs trading bot
- ✅ Risk management for pairs trading strategies

By the end of this lesson, you'll have a working pairs trading bot that can identify and trade cointegrated pairs.

---

## 📖 Why Pairs Trading?

### The Limitation of Directional Trading

Directional strategies (like moving average crossovers) have a fundamental weakness: **if you predict the market's direction incorrectly, you lose money**. If the market goes sideways for months, you make no money. Your profitability is entirely dependent on being right about the market's future direction.

### The Solution: Market-Neutral Pairs Trading

Pairs trading is a **market-neutral strategy**. It doesn't care if the overall market is bullish or bearish. Instead, it profits from temporary distortions in the price relationship between two highly correlated assets.

**Key Benefits:**
- ✅ **Market Neutrality:** Profit from relative performance, not market direction
- ✅ **Reduced Risk:** Losses on one position are buffered by gains on the other
- ✅ **Statistical Foundation:** Based on quantitative analysis, not gut feelings
- ✅ **Works in Sideways Markets:** Can profit even when markets don't trend

---

## 🔬 The Core Concepts

### Cointegration: The "Leash" Between Assets

Think of two companies in the same industry, like **Coca-Cola (KO)** and **Pepsi (PEP)**:

- Their businesses are very similar
- They are affected by the same broad economic factors
- Historically, their stock prices tend to move together

This tendency to move together is called **cointegration**. Imagine the two stocks are two dogs on a single leash. They can wander apart from each other, but the leash (their economic relationship) always pulls them back together eventually.

**Pairs trading is the art of betting that the leash will hold.**

### The Spread: Your Trading Instrument

Instead of trading KO or PEP individually, a pairs trader trades the **spread** between them:

- **Spread = Price(KO) - Price(PEP)** (price difference)
- Or **Spread = Price(KO) / Price(PEP)** (price ratio)

This spread has a historical "normal" level, or a **mean**. When the spread temporarily deviates far from this mean, the strategy assumes it will eventually return. This is called **mean reversion**.

### Z-Score: Measuring Deviation

The **Z-score** tells us how many standard deviations the current spread is from its historical mean:

- **Z-score = (Current Spread - Mean Spread) / Standard Deviation**

**Trading Rules:**
- **Enter Long Spread** when Z-score < -2 (spread is too narrow, will widen)
- **Enter Short Spread** when Z-score > +2 (spread is too wide, will narrow)
- **Exit** when Z-score returns to near 0 (spread has reverted to mean)

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `statsmodels` - Statistical analysis (cointegration tests)

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
BASE_URL = "https://paper-api.alpaca.markets"
```

⚠️ **IMPORTANT:** Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

### Step 3: Run the Bot

```bash
python pairs_trading_bot.py
```

The bot will:
1. Fetch historical data for both assets
2. Test for cointegration
3. Calculate current spread and Z-score
4. Generate trading signals
5. Execute pairs trades when appropriate

---

## 📊 How the Strategy Works

### Finding a Pair

The bot uses **Coca-Cola (KO)** and **Pepsi (PEP)** as an example pair. These are:
- In the same industry (beverages)
- Affected by similar economic factors
- Historically cointegrated

**To find your own pairs:**
1. Look for companies in the same industry
2. Test historical cointegration using statistical tests
3. Verify the relationship is stable over time

### Analyzing the Spread

The bot calculates:
- **Rolling mean** of the spread (60-day window)
- **Rolling standard deviation** of the spread
- **Current Z-score** (how many std devs from mean)

### Generating Trading Signals

| Scenario | What It Means | Your Action | The Bet |
|----------|---------------|-------------|---------|
| **Spread Widens** (Z > +2) | Asset A is "overpriced" relative to Asset B | **Short the spread:** SELL A, BUY B | Spread will narrow (revert to mean) |
| **Spread Narrows** (Z < -2) | Asset A is "underpriced" relative to Asset B | **Long the spread:** BUY A, SELL B | Spread will widen (revert to mean) |

### Executing Trades

When a signal is generated:
1. Calculate position size (2% of account value per leg)
2. Execute **both trades simultaneously**
3. Store position state for tracking

### Exiting Positions

The bot exits when:
- Z-score returns to near zero (spread has reverted)
- Or manually close positions

---

## ⚙️ Configuration

### Default Settings

```python
SYMBOL_A = "KO"          # Coca-Cola
SYMBOL_B = "PEP"         # Pepsi
LOOKBACK_DAYS = 252      # ~1 year of data
Z_SCORE_ENTRY = 2.0      # Enter when |Z| > 2
Z_SCORE_EXIT = 0.5       # Exit when |Z| < 0.5
RISK_PER_TRADE = 0.02    # 2% of account per trade
```

### Customizing the Strategy

**To use different pairs:**
```python
SYMBOL_A = "AAPL"  # Apple
SYMBOL_B = "MSFT"  # Microsoft
```

**To adjust sensitivity:**
```python
Z_SCORE_ENTRY = 2.5  # More conservative (fewer trades)
Z_SCORE_EXIT = 0.0   # Exit at exact mean
```

**To change risk:**
```python
RISK_PER_TRADE = 0.01  # 1% per trade (more conservative)
```

---

## 📈 Understanding the Output

### Cointegration Test

```
Testing cointegration...
✅ Assets are cointegrated (p-value: 0.0234)
```

- **p-value < 0.05:** Assets are cointegrated (good for pairs trading)
- **p-value >= 0.05:** Assets may not be cointegrated (proceed with caution)

### Spread Statistics

```
Current spread: $15.23
Spread mean: $12.45
Spread std: $2.89
Current Z-score: 0.96
```

- **Spread:** Current price difference
- **Mean:** Historical average spread
- **Std:** Standard deviation of spread
- **Z-score:** How many std devs from mean

### Trading Signals

```
Entry signal: Z-score (2.15) >= 2.0
Executing SHORT SPREAD: SELL 10 KO, BUY 8 PEP
✅ Pairs trade executed successfully
```

---

## ⚠️ Important Considerations

### 1. Cointegration Can Break Down

The historical relationship between two assets can permanently break down due to:
- Company acquisitions or mergers
- Major scandals or business changes
- Industry disruption

**Solution:** Regularly re-test cointegration and monitor pair stability.

### 2. Execution Risk

Pairs trading requires **simultaneous execution** of two trades. If one leg executes but the other doesn't, you're exposed to directional risk.

**Solution:** The bot uses market orders for both legs, but in production, consider:
- Limit orders with price limits
- Order routing optimization
- Monitoring for partial fills

### 3. Capital Requirements

Pairs trading requires capital for **both positions**:
- Long leg: Requires buying power
- Short leg: Requires margin (in margin accounts)

**Solution:** Ensure you have sufficient buying power and margin available.

### 4. Transaction Costs

Two trades = double the commissions. Make sure your expected profit exceeds transaction costs.

---

## 🔬 Advanced Topics

### Finding Your Own Pairs

1. **Industry Analysis:** Look for companies in the same sector
2. **Correlation Analysis:** Calculate correlation coefficient
3. **Cointegration Testing:** Use Augmented Dickey-Fuller test
4. **Stability Testing:** Verify relationship holds over time

### Alternative Spread Calculations

**Price Ratio:**
```python
spread = series_a / series_b
```

**Log Ratio:**
```python
spread = np.log(series_a) - np.log(series_b)
```

**Hedge Ratio (Beta):**
```python
beta = np.cov(series_a, series_b)[0,1] / np.var(series_b)
spread = series_a - beta * series_b
```

### Dynamic Position Sizing

Instead of fixed 2% risk, consider:
- **Volatility-based sizing:** Adjust based on spread volatility
- **Kelly Criterion:** Optimal position sizing based on win rate
- **Risk parity:** Equal risk contribution from both legs

---

## 🧪 Testing and Validation

### Paper Trading First

**Always test pairs trading strategies in paper trading first!**

1. Start with well-known pairs (KO/PEP, XOM/CVX)
2. Monitor for at least 1-2 months
3. Track performance metrics
4. Verify cointegration holds

### Key Metrics to Track

- **Win Rate:** Percentage of profitable trades
- **Average Profit per Trade:** Expected value
- **Maximum Drawdown:** Largest peak-to-trough decline
- **Sharpe Ratio:** Risk-adjusted returns
- **Pair Stability:** How often cointegration breaks down

---

## 🎓 Course Conclusion

Congratulations on completing the **Alpaca Trading Course!**

You started with nothing and have now built:
- ✅ A complete, resilient, 24/7 trading bot
- ✅ Multiple trading strategies (directional and market-neutral)
- ✅ Risk management and position sizing
- ✅ Backtesting capabilities
- ✅ Real-time data streaming
- ✅ Cloud deployment
- ✅ Advanced statistical arbitrage

**You have the skills and foundation to tackle almost any algorithmic trading project.**

The world of quantitative finance is vast, and pairs trading is just one of many advanced concepts awaiting you. Continue learning, experimenting, and building!

---

## 📚 Further Reading

### Books
- **"Pairs Trading" by Ganapathy Vidyamurthy** - Comprehensive guide to pairs trading
- **"Quantitative Trading" by Ernest Chan** - Advanced quantitative strategies
- **"Algorithmic Trading" by Ernie Chan** - Practical implementation guide

### Research Papers
- **"Pairs Trading: Performance of a Relative-Value Arbitrage Rule"** - Gatev et al.
- **"Statistical Arbitrage in the US Equities Market"** - Avellaneda & Lee

### Online Resources
- Alpaca API Documentation: https://alpaca.markets/docs/
- Statsmodels Documentation: https://www.statsmodels.org/
- QuantConnect: https://www.quantconnect.com/ (for backtesting)

---

## 🆘 Troubleshooting

### Problem: "Assets are NOT cointegrated"

**Solution:**
- Try different pairs
- Use longer lookback periods
- Consider using price ratios instead of differences
- Some pairs simply aren't suitable for pairs trading

### Problem: "No data returned for SYMBOL"

**Solution:**
- Check if symbols are valid and tradeable on Alpaca
- Verify API credentials are correct
- Check if market is open (data may be delayed)

### Problem: "Position size too small"

**Solution:**
- Increase account value (paper trading)
- Reduce minimum share requirements
- Adjust `RISK_PER_TRADE` parameter

### Problem: "Error executing pairs trade"

**Solution:**
- Check account has sufficient buying power
- Verify both symbols are tradeable
- Check for market hours restrictions
- Ensure API keys have trading permissions

---

## 📝 File Structure

```
Alpaca30/
├── pairs_trading_bot.py    # Main bot script
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── config.example.py       # Configuration template
├── .gitignore             # Git ignore rules
├── instructions.md        # Lesson instructions
└── pairs_trading_state.json  # Bot state (auto-generated)
```

---

## 🎯 Next Steps

1. **Experiment with Different Pairs:**
   - Try other industry pairs (XOM/CVX, JPM/BAC, etc.)
   - Test cross-industry pairs
   - Explore ETF pairs

2. **Optimize Parameters:**
   - Test different Z-score thresholds
   - Adjust lookback periods
   - Experiment with position sizing

3. **Add Features:**
   - Multiple pairs simultaneously
   - Dynamic pair selection
   - Portfolio-level risk management
   - Real-time monitoring dashboard

4. **Backtest:**
   - Use historical data to test strategy
   - Compare different pairs
   - Optimize entry/exit thresholds

---

**Happy building, and may your strategies be profitable!** 🚀

---

**"Risk comes from not knowing what you're doing." - Warren Buffett**

