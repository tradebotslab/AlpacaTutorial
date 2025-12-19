# Lesson 3: **Fetching Market Data – Your First Candlestick**

Welcome to Lesson 3 of the Alpaca Trading Course! This lesson demonstrates how to fetch historical OHLCV (Open, High, Low, Close, Volume) candlestick data from the Alpaca API. You'll learn how to retrieve market data programmatically, which is the foundation for any trading strategy.

## The Problem: No Access to Historical Price Data

Without the ability to fetch historical market data, you cannot analyze price trends, calculate technical indicators, or make informed trading decisions. You would be limited to current prices only, with no context about historical price movements.

| Problem/Challenge | Description |
|---|---|
| **No Historical Context** | Cannot analyze past price movements to identify trends or patterns |
| **No Technical Analysis** | Cannot calculate moving averages, RSI, or other indicators that require historical data |
| **Limited Trading Decisions** | Cannot make data-driven trading decisions without understanding price history |
| **No Strategy Development** | Cannot backtest or develop strategies that rely on historical price patterns |

## The Solution: Fetch Historical OHLCV Data Using Alpaca Market Data API

The solution is to use Alpaca's Market Data API to retrieve historical candlestick (OHLCV) data. This data includes Open, High, Low, Close prices, Volume, and other metrics for any time period and timeframe you specify. This historical data is essential for technical analysis and strategy development.

### Step 3.1: Install Required Dependencies

Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This installs:
- `alpaca-py` - Official Alpaca Python SDK (new version with market data support)
- `pandas` - Data manipulation library (used for handling DataFrames)

### Step 3.2: Configure Your API Keys

1. Copy the example configuration file:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` and add your Alpaca API keys:
   ```python
   API_KEY = "YOUR_PAPER_API_KEY_HERE"
   SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"
   ```

⚠️ **Important:** Never share your API keys publicly or commit `config.py` to version control.

### Step 3.3: Fetch and Display Historical Data

Run the script to fetch historical data for a stock symbol:

```bash
python fetch_data.py
```

The script will fetch historical candlestick data, display it in a readable format, and show summary statistics including highest price, lowest price, and average volume.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Choose Appropriate Timeframes** | Daily data provides years of history, while minute data is very limited |
| **Handle Missing Data** | Some symbols may not have data for certain time periods (holidays, delistings) |
| **Respect API Rate Limits** | Don't make excessive API calls; cache data when possible |
| **Validate Symbol Names** | Ensure stock symbols are correct (e.g., "AAPL" not "APPLE") |
| **Understand Data Formats** | OHLCV data comes as DataFrames; learn to manipulate them for analysis |

## Conclusion

You've successfully fetched historical market data from Alpaca! You now understand how to retrieve OHLCV candlestick data, which is the foundation for technical analysis and trading strategy development. Each row represents one candlestick with open, high, low, close, and volume information. In the next lesson, you'll learn how to place your first trade order using this data.
