# Lesson 26: **Time Travel – The Basics of Backtesting Your Strategy**

Welcome to Lesson 26 of the Alpaca Trading Course! This lesson teaches you how to backtest your trading strategies using historical market data. Backtesting is the process of simulating your trading strategy on past data to see how it would have performed, allowing you to test strategies before risking real money.

## The Problem: Trading Blind

Deploying an untested strategy, even with paper money, is like setting sail without a map. You might get lucky, but you're more likely to get lost. Without backtesting, you cannot answer critical questions: Would it have made money over the last year? How much risk did it involve? What was the largest loss? How does it perform compared to buy-and-hold?

| Problem/Challenge | Description |
|---|---|
| **No Performance History** | Cannot know if strategy would have been profitable in the past |
| **Unknown Risk Profile** | Don't know maximum drawdown or risk characteristics |
| **No Strategy Validation** | Cannot verify strategy logic works before risking capital |
| **Slow Testing** | Paper trading takes weeks/months to get meaningful results |

## The Solution: Backtesting on Historical Data

The solution is to backtest your strategy on historical data. This allows you to simulate years of trading in seconds, enabling rapid iteration and refinement. You can test strategy performance, compare against buy-and-hold, identify risks and drawdowns, and optimize strategy parameters - all before risking real money.

### Step 26.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client for fetching historical data
- `pandas` - Data manipulation
- `backtesting` - Powerful backtesting library
- `bokeh` - Interactive plotting (required by backtesting)

### Step 26.2: Configure Your API Credentials

Copy the example configuration and edit `config.py` with your Alpaca API credentials:

```bash
copy config.example.py config.py
```

⚠️ **IMPORTANT:** Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

### Step 26.3: Run the Backtest

Execute the backtest script:

```bash
python backtest_strategy.py
```

The script will:
1. Fetch historical data from Alpaca
2. Run the backtest on a moving average crossover strategy
3. Display results in the terminal
4. Open an interactive plot in your browser

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Use Sufficient Data** | Test on at least 1-2 years of data for meaningful results |
| **Compare to Buy-and-Hold** | Always compare strategy returns to simple buy-and-hold |
| **Understand Metrics** | Learn what return, drawdown, Sharpe ratio, and win rate mean |
| **Avoid Overfitting** | Don't optimize parameters too much on historical data |
| **Test Multiple Periods** | Test on different market conditions (bull, bear, sideways) |

## Conclusion

You've successfully learned how to backtest trading strategies! This powerful technique allows you to test strategies on historical data before risking real money. Backtesting provides fast feedback and helps you understand strategy performance and risk characteristics. In the next lesson, you'll learn how to analyze backtest results like a professional to determine if your strategy is genuinely robust.
