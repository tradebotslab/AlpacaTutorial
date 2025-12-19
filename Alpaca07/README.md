# Alpaca Trading Course - Tutorial 7: Simple Moving Average (SMA)

This tutorial demonstrates how to calculate Simple Moving Average (SMA) technical indicators using pandas and Alpaca API.

## What is a Simple Moving Average (SMA)?

A Simple Moving Average is the average price of a stock over a specific number of periods. For example, a 20-day SMA is the average of the closing prices over the last 20 days.

### Why is it useful?

- **Smoothing**: It smooths out short-term price fluctuations and market "noise"
- **Trend Identification**: It helps you identify the underlying trend. If the price is consistently above the SMA, it suggests an uptrend. If it's below, it suggests a downtrend
- **Trading Signals**: The relationship between a short-term SMA and a long-term SMA can be used to generate buy or sell signals (a concept known as a "crossover strategy")

## Project Structure

```
Alpaca07/
├── config.py              # API credentials (not included in repo - see setup below)
├── config.py.template     # Template for config.py
├── calculate_sma.py       # Main script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── instructions.md       # Detailed tutorial instructions
```

## Prerequisites

- Completed Tutorial 3 (fetching historical data)
- Python 3.7+
- Alpaca paper trading account
- pandas library (installed via requirements.txt)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

1. Copy `config.py.template` to `config.py`:
   ```bash
   cp config.py.template config.py
   ```
   On Windows:
   ```powershell
   Copy-Item config.py.template config.py
   ```

2. Edit `config.py` and add your Alpaca API credentials:
   - Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
   - Replace `YOUR_API_KEY_HERE` and `YOUR_SECRET_KEY_HERE` with your actual keys

**Important:** The `config.py` file is excluded from git to protect your API keys. Never commit this file!

### 3. Run the Script

```bash
python calculate_sma.py
```

The script will:
- Fetch 100 days of historical data for AAPL
- Calculate 20-day and 50-day Simple Moving Averages
- Display the results with price data and SMA values

## Understanding the Code

### Key Concepts

1. **`.rolling(window=N)`**: Creates a rolling window of N periods. For window=20, it includes the current row and the 19 previous rows.

2. **`.mean()`**: Calculates the average of all values in the rolling window.

3. **NaN Values**: The first N-1 rows will have NaN (Not a Number) values for an N-day SMA because there isn't enough historical data to calculate the average yet.

### Example Output

When you run the script, you'll see output like:

```
Fetching 100 days of historical data for AAPL...
Successfully fetched 100 days of data for AAPL.

--- Price data for AAPL with 20-day and 50-day SMA ---
                                 open    high     low   close  ...      vwap      sma_20      sma_50
timestamp                                                      ...                                
2023-12-04 05:00:00+00:00  189.98  190.05  187.45  189.43  ...  188.85  190.5235  182.0136
2023-12-05 05:00:00+00:00  190.21  194.40  190.18  193.42  ...  192.95  190.7290  182.5158
...
```

Notice how the SMA values are much "smoother" than the daily closing prices.

## Security Notes

- **Never commit `config.py`** - It contains your API keys and is excluded via `.gitignore`
- **Always use paper trading** - The default `BASE_URL` points to the paper trading environment for safety
- **Keep your keys secure** - Treat your API keys like passwords

## Next Steps

In future tutorials, you'll learn how to:
- Use SMA crossovers to generate trading signals
- Combine multiple technical indicators
- Build trading strategies based on technical analysis

## License

This is an educational project for learning automated trading with Alpaca.

