# Tutorial 3: Fetching Market Data – Your First Candlestick

This tutorial demonstrates how to fetch historical OHLCV (Open, High, Low, Close, Volume) candlestick data from the Alpaca API. You'll learn how to retrieve market data programmatically, which is the foundation for any trading strategy.

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8 or higher** (Python 3.10+ recommended)
  - Check your Python version: `python --version`
- **An Alpaca Paper Trading Account**
  - Sign up at [https://alpaca.markets](https://alpaca.markets) if you don't have one
- **Alpaca API Keys**
  - Generate your API keys from the Alpaca dashboard
  - You'll need both `API_KEY` and `SECRET_KEY`
- **Completed Tutorial 2**
  - You should have a working `config.py` file with your API keys

## 🚀 Installation Steps

### Step 1: Install Python Dependencies

Open your terminal or command prompt and navigate to the project directory:

```bash
cd path/to/Alpaca03
```

Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install:
- `alpaca-py` - Official Alpaca Python SDK (new version with market data support)
- `pandas` - Data manipulation library (used for handling DataFrames)

**Alternative installation method:**

If you prefer to install packages individually:

```bash
pip install alpaca-py pandas
```

### Step 2: Verify Installation

To verify that the packages were installed correctly, you can test the import:

```bash
python -c "from alpaca.data.historical import StockHistoricalDataClient; print('Installation successful!')"
```

If you see "Installation successful!" without any errors, you're ready to proceed.

## ⚙️ Configuration

### Step 3: Configure Your API Keys

1. Copy the example configuration file:
   ```bash
   cp config.example.py config.py
   ```

2. Open the `config.py` file in your code editor.

3. Replace the placeholder values with your actual Alpaca API keys:

   ```python
   API_KEY = "YOUR_PAPER_API_KEY_HERE"  # Replace with your actual API key
   SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"  # Replace with your actual secret key
   ```

4. **Important Security Notes:**
   - Never share your API keys publicly
   - Never commit `config.py` to version control (it should be in `.gitignore`)
   - The `BASE_URL` should remain as `https://paper-api.alpaca.markets` for paper trading

### Where to Find Your API Keys

1. Log in to your Alpaca account at [https://app.alpaca.markets](https://app.alpaca.markets)
2. Navigate to **"Your API Keys"** section (usually found in the dashboard or account settings)
3. Make sure you're viewing **Paper Trading** keys (not Live Trading)
4. Copy the **API Key ID** and **Secret Key**
5. Paste them into your `config.py` file

## ▶️ Running the Program

### Step 4: Execute the Script

Once your API keys are configured, run the script:

```bash
python fetch_data.py
```

### Expected Output

If everything is configured correctly, you should see output similar to this:

```
Fetching historical market data from Alpaca API...

======================================================================
HISTORICAL CANDLESTICK DATA FOR AAPL
======================================================================
                      open     high      low    close   volume trade_count         vwap
symbol timestamp                                                                       
AAPL   2023-01-03 12:00:00+00:00  130.28  130.900  124.170  125.07  112117500      820835  126.449103
       2023-01-04 12:00:00+00:00  126.89  128.655  125.080  126.36   89113600      673444  126.920143
       2023-01-05 12:00:00+00:00  127.12  127.770  124.760  125.02   85925400      642646  126.255536
       2023-01-06 12:00:00+00:00  126.01  130.290  124.890  129.61   87693100      653303  128.144426
       2023-01-09 12:00:00+00:00  129.47  133.410  129.470  130.15   70790800      521997  131.624634
       2023-01-10 12:00:00+00:00  130.26  131.260  128.120  130.73   63896200      486632  129.939226

======================================================================
Total bars retrieved: 6
======================================================================

======================================================================
SUMMARY STATISTICS FOR AAPL
======================================================================
Date Range: 2023-01-03 12:00:00+00:00 to 2023-01-10 12:00:00+00:00
Highest Price: $133.41
Lowest Price: $124.17
First Close: $125.07
Last Close: $130.73
Average Volume: 84,094,283 shares
======================================================================

Successfully fetched historical data! Each row represents one candlestick.
```

## 📊 Understanding the Output

### What is OHLCV Data?

Each row in the output represents one **candlestick** for a specific time period (in this case, one day). The data includes:

- **open**: The price of the stock at the beginning of the period (e.g., at market open for `TimeFrame.Day`)
- **high**: The highest price the stock reached during that period
- **low**: The lowest price the stock reached during that period
- **close**: The price of the stock at the end of the period (e.g., at market close)
- **volume**: The total number of shares that were traded during that period
- **vwap**: Volume-Weighted Average Price - A measure of the average price weighted by volume
- **trade_count**: The number of individual trades that occurred during the period

### Why This Data Matters

A single price point tells you very little about market behavior. OHLCV data provides:

- **Context**: You can see if the stock is trending up, down, or moving sideways
- **Volatility**: The high-low range shows how much the price moved during the period
- **Market Activity**: Volume indicates how actively the stock was traded
- **Foundation for Analysis**: This data is required for calculating technical indicators (moving averages, RSI, etc.)

## 🔧 Customizing the Script

### Changing the Stock Symbol

To fetch data for a different stock, modify the `symbol` variable in the `main()` function:

```python
symbol = "MSFT"  # Microsoft
# or
symbol = "GOOGL"  # Google
# or
symbol = "TSLA"  # Tesla
```

### Changing the Date Range

Modify the `start_date` and `end_date` in the `main()` function:

```python
start_date = datetime(2023, 6, 1)  # June 1, 2023
end_date = datetime(2023, 6, 30)    # June 30, 2023
```

### Changing the Timeframe

You can fetch data at different timeframes:

```python
timeframe = TimeFrame.Hour    # Hourly candlesticks
# or
timeframe = TimeFrame.Minute  # Minute candlesticks (limited history)
# or
timeframe = TimeFrame.Day     # Daily candlesticks (default)
```

**Note:** The amount of historical data available depends on the timeframe:
- Daily data: Several years of history
- Hourly data: Limited to recent months
- Minute data: Very limited history (usually days or weeks)

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'alpaca'`

**Solution:** Install the required packages:
```bash
pip install -r requirements.txt
```

**Note:** Make sure you're using `alpaca-py` (the new SDK), not `alpaca-trade-api` (the old SDK).

### Error: `Error fetching stock data: 401 Client Error: Unauthorized`

**Possible causes:**
- Invalid API keys in `config.py`
- API keys are for Live Trading instead of Paper Trading
- API keys have been revoked or expired

**Solution:**
1. Double-check your API keys in `config.py`
2. Verify you're using Paper Trading keys (not Live Trading)
3. Generate new API keys from your Alpaca dashboard if necessary

### Error: `Error fetching stock data: Connection timeout` or network errors

**Possible causes:**
- No internet connection
- Firewall blocking the connection
- Alpaca API is temporarily unavailable

**Solution:**
1. Check your internet connection
2. Verify you can access [https://paper-api.alpaca.markets](https://paper-api.alpaca.markets) in your browser
3. Check if your firewall or antivirus is blocking Python's network access
4. Try again after a few minutes if the API is temporarily down

### Error: `No data available for [SYMBOL]`

**Possible causes:**
- The stock symbol is invalid
- The date range is outside market hours or holidays
- The date range is too far in the past (for minute/hourly data)

**Solution:**
1. Verify the stock symbol is correct (e.g., "AAPL" not "APPLE")
2. Check that your date range includes trading days (not weekends or holidays)
3. For minute/hourly data, use more recent dates

### Error: `AttributeError: 'module' object has no attribute 'StockHistoricalDataClient'`

**Solution:** You might be using the old `alpaca-trade-api` library. Uninstall it and install the new one:

```bash
pip uninstall alpaca-trade-api
pip install alpaca-py
```

## 📁 Project Structure

```
Alpaca03/
│
├── config.py              # API keys configuration (DO NOT SHARE THIS FILE)
├── config.example.py       # Template for config.py
├── fetch_data.py          # Main script
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
├── Instructions.md       # Tutorial instructions
└── .gitignore            # Git ignore file (protects config.py)
```

## 🔒 Security Reminders

- ⚠️ **Never commit `config.py` to Git** - Add it to `.gitignore`
- ⚠️ **Never share your API keys** publicly or in screenshots
- ⚠️ **Use Paper Trading keys** for tutorials (not Live Trading)
- ⚠️ **Rotate your keys** if you suspect they've been compromised

## 📚 Next Steps

Once you've successfully fetched historical data, you can:

- Learn how to calculate technical indicators (Simple Moving Average, RSI, etc.)
- Build trading strategies based on historical patterns
- Analyze multiple stocks simultaneously
- Create visualizations of price data

## 📖 Additional Resources

- [Alpaca Market Data API Documentation](https://alpaca.markets/docs/api-documentation/market-data-api/)
- [Pandas DataFrame Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
- [OHLCV Data Explained](https://www.investopedia.com/terms/o/ohlcchart.asp)

## 📞 Support

If you encounter issues:

1. Check the [Alpaca API Documentation](https://alpaca.markets/docs/)
2. Review the error messages for specific details
3. Ensure all prerequisites are met
4. Verify your API keys are correct

## 📝 License

This tutorial is part of an educational course on algorithmic trading with Alpaca.

