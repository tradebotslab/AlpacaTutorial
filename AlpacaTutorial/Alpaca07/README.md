# Lesson 7: **Simple Moving Average (SMA)**

Welcome to Lesson 7 of the Alpaca Trading Course! This lesson demonstrates how to calculate Simple Moving Average (SMA) technical indicators using pandas and Alpaca API. Moving averages are fundamental tools in technical analysis and form the basis for many trading strategies.

## The Problem: Raw Price Data is Too Noisy

Raw price data contains a lot of short-term fluctuations and "noise" that can obscure the underlying trend. Without smoothing techniques, it's difficult to identify trends, make trading decisions, or build reliable trading strategies.

| Problem/Challenge | Description |
|---|---|
| **Price Noise** | Daily price movements are volatile and can obscure the underlying trend direction |
| **No Trend Identification** | Cannot easily determine if a stock is in an uptrend, downtrend, or moving sideways |
| **Difficult Decision Making** | Hard to make trading decisions based on noisy, unpredictable price movements |
| **No Signal Generation** | Cannot generate buy/sell signals without tools to identify trends and momentum |

## The Solution: Calculate Simple Moving Averages to Smooth Price Data

The solution is to calculate Simple Moving Averages (SMA), which smooth out short-term price fluctuations by averaging prices over a specific number of periods. A 20-day SMA is the average of the closing prices over the last 20 days. This helps identify trends and can be used to generate trading signals.

### Step 7.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `alpaca-py` or `alpaca-trade-api` - Alpaca API client
- `pandas` - Data manipulation library (essential for calculating SMAs)

### Step 7.2: Configure API Credentials

1. Copy `config.py.template` to `config.py`
2. Edit `config.py` and add your Alpaca API credentials
3. Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

**Important:** Never commit `config.py` to version control!

### Step 7.3: Run the SMA Calculation Script

Execute the script:

```bash
python calculate_sma.py
```

The script will:
- Fetch 100 days of historical data for AAPL
- Calculate 20-day and 50-day Simple Moving Averages
- Display the results with price data and SMA values

Notice how the SMA values are much "smoother" than the daily closing prices.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Choose Appropriate Periods** | Short SMAs (10-20 days) react quickly; long SMAs (50-200 days) show long-term trends |
| **Understand NaN Values** | The first N-1 rows will have NaN values for an N-day SMA (not enough historical data) |
| **Combine Multiple SMAs** | Using short and long SMAs together can generate crossover signals |
| **Consider Market Context** | SMAs work better in trending markets than in choppy, sideways markets |
| **Use Rolling Windows** | The `.rolling(window=N).mean()` method is the standard way to calculate SMAs in pandas |

## Conclusion

You've successfully learned how to calculate Simple Moving Averages! SMAs are powerful tools that smooth out price noise and help identify trends. The relationship between short-term and long-term SMAs can be used to generate trading signals (like Golden Cross and Death Cross). In the next lesson, you'll learn how to detect when these moving averages cross over each other, which is a common trading signal.
