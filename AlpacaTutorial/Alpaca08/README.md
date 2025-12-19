# Lesson 8: **Moving Average Crossover Detector**

Welcome to Lesson 8 of the Alpaca Trading Course! This lesson implements a simple trading signal detector that identifies moving average crossovers using the Alpaca API. Crossover signals are fundamental to many trend-following trading strategies.

## The Problem: No Systematic Way to Identify Trend Changes

While moving averages help identify trends, you need a systematic way to detect when trends are changing. Without a crossover detection mechanism, you cannot automatically identify potential buy or sell signals based on moving average relationships.

| Problem/Challenge | Description |
|---|---|
| **Manual Signal Detection** | Cannot automatically identify when moving averages cross, requiring manual chart analysis |
| **Missed Opportunities** | Without automated detection, you might miss important crossover signals |
| **No Systematic Approach** | No consistent method to identify trend reversals or momentum shifts |
| **Subjective Interpretation** | Manual analysis is subjective and can lead to inconsistent trading decisions |

## The Solution: Automatically Detect Moving Average Crossovers

The solution is to programmatically compare the relationship between short-term and long-term moving averages on consecutive days. When a short-term SMA crosses above a long-term SMA (Golden Cross), it signals potential upward momentum. When it crosses below (Death Cross), it signals potential downward momentum.

### Step 8.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 8.2: Configure Your Alpaca API Credentials

1. Copy `config.py` and add your API keys
2. Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
3. **Important**: Never commit `config.py` to version control

### Step 8.3: Run the Crossover Detector

Execute the script:

```bash
python crossover_detector.py
```

The script will:
1. Fetch the last 51 days of price data for a symbol (default: AAPL)
2. Calculate 20-day and 50-day Simple Moving Averages
3. Compare the relationship between SMAs on the previous day vs. the current day
4. Detect if a crossover occurred (Golden Cross or Death Cross)
5. Print the signal result

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Golden Cross (Bullish)** | 20-day SMA crosses above 50-day SMA - potential buy signal |
| **Death Cross (Bearish)** | 20-day SMA crosses below 50-day SMA - potential sell signal |
| **False Signals** | Crossovers can occur in choppy markets; use additional confirmation |
| **Compare Consecutive Days** | Check if relationship changed from previous day to current day to detect crossovers |
| **Use Multiple Timeframes** | Crossovers on daily charts are more reliable than on shorter timeframes |

## Conclusion

You've successfully built a moving average crossover detector! This is a fundamental component of many trading strategies. Golden Cross and Death Cross signals are widely used by traders to identify trend changes. In the next lesson, you'll learn how to combine this signal detection with order execution to build a complete trading bot that automatically buys and sells based on crossover signals.
