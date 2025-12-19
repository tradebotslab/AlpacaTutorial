# Lesson 27: **Understanding Your Results – Analyzing a Backtest Report**

Welcome to Lesson 27 of the Alpaca Trading Course! This lesson teaches you how to analyze backtest results like a professional. Running a backtest is only the first step—understanding what the numbers mean is what separates successful traders from gamblers.

## The Problem: Misleading Numbers

A backtest report shows "Return: 150%" and you think you've struck gold. But hold on—the total return is only a tiny part of the story. A profitable strategy might be so risky that it's psychologically impossible to follow. Looking only at the final return is a classic beginner's mistake.

| Problem/Challenge | Description |
|---|---|
| **Incomplete Analysis** | Total return alone doesn't tell the full story |
| **Ignored Risk Metrics** | Don't understand drawdown, volatility, or risk-adjusted returns |
| **Misleading Performance** | High returns might come with unacceptable risk |
| **No Context** | Don't know if results are good compared to alternatives |

## The Solution: Deep Analysis of Key Metrics

The solution is to analyze multiple metrics holistically: Annual Return (how much per year), Max Drawdown (largest peak-to-trough decline - can you handle it?), Sharpe Ratio (risk-adjusted returns - is risk worth the reward?), Win Rate (percentage of profitable trades), and Profit Factor (gross profit ÷ gross loss). You must ask: How long did it take? How much did the portfolio swing? Would I have panicked during a losing streak?

### Step 27.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client for fetching historical data
- `pandas` - Data manipulation
- `backtesting` - Powerful backtesting library
- `bokeh` - Interactive plotting

### Step 27.2: Configure Your API Credentials

Copy the example configuration and edit `config.py` with your Alpaca API credentials.

### Step 27.3: Run the Analysis

Execute the analysis script:

```bash
python analyze_backtest.py
```

The script will:
1. Fetch historical data from Alpaca
2. Run the backtest
3. Display basic results
4. Provide detailed analysis of key metrics
5. Open an interactive plot in your browser

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Annual Return** | Convert total return to annualized return for fair comparison |
| **Max Drawdown** | Ensure you can psychologically handle the largest loss period |
| **Sharpe Ratio** | Aim for > 1.0; > 2.0 is excellent (higher is better) |
| **Win Rate vs Profit Factor** | High win rate with low profit factor may not be profitable |
| **Holistic Assessment** | Consider all metrics together, not just one number |

## Conclusion

You've successfully learned how to analyze backtest results like a professional! Understanding metrics like annual return, max drawdown, and Sharpe ratio helps you determine if your strategy is genuinely robust or just a lucky gamble. This analysis is essential for making informed decisions about which strategies to deploy. In the next lesson, you'll learn about WebSockets for streaming real-time market data.
