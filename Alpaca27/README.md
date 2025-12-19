# 📚 Alpaca Trading Course - Lesson 27

## 📊 Understanding Your Results – Analyzing a Backtest Report

### 🎯 What You Will Learn

In this lesson, you will learn how to **analyze backtest results like a professional**. Running a backtest is only the first step—understanding what the numbers mean is what separates successful traders from gamblers. You'll learn to:

- ✅ Calculate and interpret **Annual Return**
- ✅ Understand **Max Drawdown** and its psychological impact
- ✅ Evaluate **Sharpe Ratio** for risk-adjusted performance
- ✅ Analyze **Win Rate** in context of **Profit Factor**
- ✅ Make holistic assessments of strategy quality

By the end of this lesson, you'll be able to answer: **"Is my strategy genuinely robust, or just a lucky gamble?"**

---

## 📖 Why This Matters

### The Problem: Misleading Numbers

A backtest report shows "Return: 150%" and you think you've struck gold. But hold on—the total return is only a tiny part of the story. A profitable strategy might be so risky that it's psychologically impossible to follow.

### The Solution: Deep Analysis

Looking only at the final return is a classic beginner's mistake. You must ask:

- **How long did it take to achieve that return?**
- **How much did the portfolio value swing up and down along the way?**
- **Would I have panicked and abandoned the strategy during a losing streak?**

This lesson teaches you to answer these questions and paint a complete picture of your strategy's performance and risk profile.

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

### Step 3: Run the Analysis

```bash
python analyze_backtest.py
```

The script will:
1. Fetch historical data from Alpaca
2. Run the backtest
3. Display basic results
4. Provide detailed analysis of key metrics
5. Open an interactive plot in your browser

---

## 📊 What the Script Does

### Strategy: Moving Average Crossover

This tutorial uses the same strategy from Lesson 26:

- **Buy Signal (Golden Cross):** When a short-term moving average (10 days) crosses **above** a long-term moving average (30 days)
- **Sell Signal (Death Cross):** When the short-term MA crosses **below** the long-term MA

### Backtest Configuration

- **Symbol:** TSLA (Tesla)
- **Period:** January 1, 2020 to December 31, 2022
- **Initial Cash:** $10,000
- **Commission:** 0.2% per trade

You can modify these parameters in the `main()` function.

### Analysis Features

The script provides comprehensive analysis of:

1. **Annual Return** - Normalized return for comparison
2. **Max Drawdown** - Largest portfolio drop (psychological pain metric)
3. **Sharpe Ratio** - Risk-adjusted return measure
4. **Win Rate & Profit Factor** - Trade quality analysis
5. **Overall Assessment** - Holistic strategy evaluation

---

## 📁 Project Structure

```
Alpaca27/
├── analyze_backtest.py    # Main analysis script
├── config.py               # Your API credentials (not tracked by git)
├── config.example.py       # Template configuration file
├── requirements.txt         # Python dependencies
├── .gitignore              # Protects your API keys
├── instructions.md         # Lesson instructions
└── README.md               # This file
```

---

## 🔍 Key Metrics Explained

### 1. Annual Return

**What it is:**
The geometric average amount of money the strategy earned per year.

**Why it matters:**
- Provides a normalized basis for comparison
- A 50% return over 5 years (≈8.4% annually) is very different from a 50% return in 1 year (50% annually)
- Helps you compare your strategy against benchmarks like the S&P 500's average annual return

**Rule of Thumb:**
Your strategy's Annual Return should be meaningfully higher than the "Buy & Hold Return" for the same period. If it's not, you took on a lot of complexity and risk for nothing.

### 2. Max Drawdown

**What it is:**
The maximum "paper loss" your portfolio experienced during the backtest. It measures the largest single drop from a portfolio's peak value to its subsequent lowest point (the trough).

**Why it matters:**
- This is the metric of psychological pain
- Answers: "What is the worst losing streak I would have had to endure?"
- If a strategy has a 50% Max Drawdown, it means at one point, your $10,000 portfolio would have dropped to $5,000
- Could you stomach that without panicking and selling everything at the bottom?
- A low drawdown = more stable, less stressful strategy

**Example:**
If your portfolio grows from $10k to $15k, then drops to $7.5k before recovering:
- Drawdown = ($15,000 - $7,500) / $15,000 = 50%

**Interpretation:**
- < 10%: Low risk - Manageable drawdown
- 10-20%: Moderate risk - Requires discipline
- 20-40%: High risk - Very difficult to stick with psychologically
- > 40%: Extreme risk - Would wipe out most retail traders

### 3. Sharpe Ratio

**What it is:**
The average return earned in excess of the risk-free rate per unit of volatility. It tells you how much return you are getting for each unit of risk you take on.

**Why it matters:**
- Helps you compare different strategies
- A strategy with a 20% return and wild price swings might be worse than a strategy with a 15% return and a smooth, steady equity curve
- The second strategy will have a higher Sharpe Ratio
- Higher Sharpe Ratio = better return per unit of risk

**General Interpretation:**
- **< 1.0:** Not considered great. The returns do not justify the risk taken.
- **1.0 - 1.99:** Considered good.
- **2.0 - 2.99:** Considered very good.
- **> 3.0:** Considered excellent (and may be a sign of a "too good to be true" backtest).

**A higher Sharpe Ratio is almost always better.**

### 4. Win Rate & Profit Factor

**Win Rate:**
The percentage of trades that closed with a profit.

**Why it matters:**
- Gives you an idea of the strategy's consistency
- A high win rate can be psychologically comforting
- **However, it says nothing about the size of the wins versus the size of the losses**

**Profit Factor:**
Total profit from winning trades / Total loss from losing trades.

**Why it matters:**
- This is why you must look at win rate alongside profit factor
- A high win rate with small wins and large losses = losing strategy
- A low win rate with large wins and small losses = winning strategy

**Example Scenarios:**

**Scenario A (Bad):**
- Win Rate: 90%
- Average Win: $10
- Average Loss: $100
- Result: You win 9 out of 10 trades, making 9 × $10 = $90. But your one losing trade costs you $100. **Net loss of $10.**

**Scenario B (Good):**
- Win Rate: 40%
- Average Win: $100
- Average Loss: $20
- Result: You win 4 out of 10 trades, making 4 × $100 = $400. Your six losing trades cost you 6 × $20 = $120. **Net profit of $280.**

**Conclusion:**
A low win rate is perfectly acceptable if your winning trades are significantly larger than your losing trades.

---

## 📈 Putting It All Together

### Never Judge by a Single Number

Analyze the metrics together to understand the full story:

| Metric | Strategy A ("Slow & Steady") | Strategy B ("Gambler") | Analysis |
|--------|------------------------------|------------------------|----------|
| Annual Return | 15% | 25% | B looks better on the surface |
| Max Drawdown | -10% | -60% | A is far less risky and easier to stick with. A 60% loss would wipe out most retail traders |
| Sharpe Ratio | 1.8 | 0.7 | A provides excellent return for its low risk. B's returns do not justify its extreme volatility |
| Win Rate | 55% | 30% | B has very few winning trades, which can be psychologically difficult |

**Verdict:** Strategy A is vastly superior for almost any real-world investor, even though its annual return is lower. It provides good returns with manageable, predictable risk.

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

### Modify Strategy Parameters

```python
class SmaCross(Strategy):
    short_ma_period = 10   # Try: 5, 10, 20
    long_ma_period = 30    # Try: 20, 30, 50, 100
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
📚 Alpaca Trading Course - Lesson 27
📖 Understanding Your Results – Analyzing a Backtest Report
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

======================================================================
📊 BASIC BACKTEST RESULTS
======================================================================

💰 Return: 45.23%
📈 Buy & Hold Return: 38.12%
📉 Max. Drawdown: -12.45%
📊 Sharpe Ratio: 1.85
🔢 # Trades: 24
✅ Win Rate: 58.33%
📊 Profit Factor: 1.65
📊 Avg. Trade: 1.88%
📈 Best Trade: 15.23%
📉 Worst Trade: -8.45%
======================================================================

======================================================================
📊 DETAILED BACKTEST ANALYSIS
======================================================================

──────────────────────────────────────────────────────────────────────
1️⃣  ANNUAL RETURN
──────────────────────────────────────────────────────────────────────
   Total Return: 45.23%
   Annual Return: 13.21%
   Buy & Hold Annual Return: 11.34%
   ✅ Strategy outperforms Buy & Hold by 1.87% annually

   📝 Why it matters:
      Annual Return standardizes performance for comparison.
      A 50% return over 5 years (≈8.4% annually) is very different
      from a 50% return in 1 year (50% annually).

──────────────────────────────────────────────────────────────────────
2️⃣  MAX DRAWDOWN
──────────────────────────────────────────────────────────────────────
   Max Drawdown: -12.45%
   ⚠️ Moderate risk - Requires discipline to hold through

   📊 Example:
      If your portfolio peaked at $14,523.00,
      it would have dropped to $12,714.00 at the worst point.
      That's a loss of $1,809.00.

   📝 Why it matters:
      This is the metric of psychological pain.
      Could you stomach this loss without panicking and selling?
      A low drawdown = more stable, less stressful strategy.

──────────────────────────────────────────────────────────────────────
3️⃣  SHARPE RATIO
──────────────────────────────────────────────────────────────────────
   Sharpe Ratio: 1.85
   ✅✅ Very good - Excellent risk-adjusted returns

   📝 Why it matters:
      Measures risk-adjusted return.
      A 20% return with wild swings might be worse than
      a 15% return with smooth, steady growth.
      Higher Sharpe Ratio = better return per unit of risk.

──────────────────────────────────────────────────────────────────────
4️⃣  WIN RATE & PROFIT FACTOR
──────────────────────────────────────────────────────────────────────
   Win Rate: 58.33%
   Profit Factor: 1.65
   Average Win: 4.23%
   Average Loss: -2.56%

   📊 Analysis:
   ✅ Moderate win rate (58.3%) - Acceptable
   ✅ Good profit factor (1.65) - Wins outweigh losses
   ✅ Wins larger than losses - Positive expectancy

   📝 Why it matters:
      Win rate alone can be misleading!
      Scenario A: 90% win rate, but avg loss ($100) > avg win ($10)
      → Net loss despite high win rate
      Scenario B: 40% win rate, but avg win ($100) > avg loss ($20)
      → Net profit despite low win rate
      Always look at win rate WITH profit factor!

──────────────────────────────────────────────────────────────────────
5️⃣  OVERALL ASSESSMENT
──────────────────────────────────────────────────────────────────────
   Strategy Score: 100% (4/4 key metrics positive)
   ✅✅ STRONG STRATEGY - Multiple positive indicators
      This strategy shows promise. Consider paper trading next.

======================================================================
💡 KEY TAKEAWAY
======================================================================
Never judge a strategy by a single number!
Analyze all metrics together to understand the full story.
A strategy with lower returns but better risk metrics
may be superior to a high-return, high-risk strategy.
======================================================================
```

---

## 📈 Next Steps

### Lesson 28: Strategy Optimization
- Optimize strategy parameters
- Walk-forward analysis
- Parameter sensitivity testing

### Lesson 29: Advanced Backtesting
- Multiple timeframes
- Portfolio backtesting
- Risk-adjusted metrics

### Lesson 30: Live Trading Integration
- Deploy backtested strategies
- Paper trading validation
- Real-time monitoring

---

## 🎓 Key Takeaways

1. **Never Judge by One Number** – Total return is only part of the story

2. **Annual Return Matters** – Standardizes performance for fair comparison

3. **Max Drawdown = Psychological Pain** – Can you stick with the strategy during the worst drawdown?

4. **Sharpe Ratio = Risk-Adjusted Return** – Higher is better, measures efficiency

5. **Win Rate Can Be Misleading** – Always check it with Profit Factor

6. **Holistic Analysis** – Look at all metrics together to understand the full picture

7. **Past Performance ≠ Future Results** – But negative backtests are strong signals to improve

---

## 📚 Additional Resources

### Performance Metrics
- [Sharpe Ratio Explained](https://www.investopedia.com/terms/s/sharperatio.asp)
- [Maximum Drawdown](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)
- [Profit Factor](https://www.investopedia.com/terms/p/profit-factor.asp)
- [Win Rate vs Profit Factor](https://www.investopedia.com/articles/trading/08/trading-strategy-metrics.asp)

### Backtesting Library
- [backtesting.py Documentation](https://kernc.github.io/backtesting.py/)
- [backtesting.py GitHub](https://github.com/kernc/backtesting.py)

### Alpaca API
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca Market Data API](https://alpaca.markets/docs/api-documentation/market-data-api/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-py)

### Trading Strategy Resources
- [Risk Management in Trading](https://www.investopedia.com/articles/trading/09/risk-management.asp)
- [Evaluating Trading Strategies](https://www.investopedia.com/articles/trading/08/trading-strategy-metrics.asp)

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

Understanding your backtest results is the key to building strategies you can trust! 📊

---

*Alpaca Trading Course - Lesson 27*  
*Understanding Your Results – Analyzing a Backtest Report*

