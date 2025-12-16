Tutorial 7: Calculating Your First Indicator – Simple Moving Average (SMA)
Objective: In this tutorial, you will learn how to calculate one of the most fundamental technical indicators, the Simple Moving Average (SMA), using the pandas library on the market data you've learned to fetch.

1. What is a Simple Moving Average (SMA)?
A Simple Moving Average is the average price of a stock over a specific number of periods. For example, a 20-day SMA is the average of the closing prices over the last 20 days.

Why is it useful?

Smoothing: It smooths out short-term price fluctuations and market "noise."

Trend Identification: It helps you identify the underlying trend. If the price is consistently above the SMA, it suggests an uptrend. If it's below, it suggests a downtrend.

Trading Signals: The relationship between a short-term SMA and a long-term SMA can be used to generate buy or sell signals (a concept known as a "crossover strategy").

2. Prerequisites
Completed Tutorial 3: You should be familiar with fetching historical data.

pandas library: Must be installed (pip install pandas).

3. Project Setup
In your alpaca_bot_project folder, create a new file named calculate_sma.py.

Your project structure should now look like this:

alpaca_bot_project/
├── config.py
├── ... (previous files)
└── calculate_sma.py     # New file
4. Creating the Script (calculate_sma.py)
Open calculate_sma.py and add the following code. This script will fetch the last 100 days of price data for AAPL and then calculate the 20-day and 50-day SMAs.

python
# calculate_sma.py

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import TimeFrame
import pandas as pd
import config

# --- 1. Authentication and API Connection ---
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL, api_version='v2')

try:
    # --- 2. Fetch Historical Data ---
    # We need more data to calculate a 50-day SMA, so let's get 100 days.
    symbol = "AAPL"
    end_date = pd.Timestamp.now(tz='America/New_York').isoformat()
    start_date = (pd.Timestamp.now(tz='America/New_York') - pd.Timedelta(days=100)).isoformat()

    barset = api.get_bars(
        symbol,
        TimeFrame.Day,
        start=start_date,
        end=end_date,
        adjustment='raw'
    )
    
    # Convert the barset to a pandas DataFrame
    df = barset.df
    print(f"Fetched {len(df)} days of data for {symbol}.")

    # --- 3. Calculate Simple Moving Averages (SMA) ---
    # We will calculate a short-term SMA (20 days) and a long-term SMA (50 days)
    # The SMA is calculated on the 'close' price.
    
    # Calculate the 20-day SMA
    df['sma_20'] = df['close'].rolling(window=20).mean()

    # Calculate the 50-day SMA
    df['sma_50'] = df['close'].rolling(window=50).mean()

    # --- 4. Display the Results ---
    print(f"\n--- Data for {symbol} with 20-day and 50-day SMA ---")
    # .tail() shows the last few rows of the DataFrame
    print(df.tail(10))

except Exception as e:
    print(f"An error occurred: {e}")
5. Understanding the Code
Authentication: Standard API connection.

Fetch Historical Data: We fetch 100 days of data to ensure we have enough history to calculate a 50-day SMA.

Calculate SMAs (.rolling().mean()): This is the core of the tutorial.

df['close']: We select the column of closing prices from our DataFrame.

.rolling(window=20): This is the magic function from pandas. It creates a "rolling window" of a specified size. For window=20, it takes the current row's closing price and the 19 previous closing prices to form a group of 20. It does this for every row in the DataFrame.

.mean(): This function is then chained to the rolling window to calculate the average (the mean) of the 20 values inside that window.

df['sma_20'] = ...: We take the result of this calculation and store it in a brand new column in our DataFrame called sma_20. We repeat the process for the 50-day SMA.

Display the Results:

When you run the script, look at the output. You'll see two new columns, sma_20 and sma_50, alongside the original price data.

Notice how the SMA values are much "smoother" than the daily closing prices.

Example Output:

                                 open    high     low   close  ...      vwap      sma_20      sma_50
timestamp                                                      ...                                
2023-12-04 05:00:00+00:00  189.98  190.05  187.45  189.43  ...  188.85  190.5235  182.0136
2023-12-05 05:00:00+00:00  190.21  194.40  190.18  193.42  ...  192.95  190.7290  182.5158
2023-12-06 05:00:00+00:00  194.45  194.76  192.11  192.32  ...  193.10  190.8140  182.9780
2023-12-07 05:00:00+00:00  193.63  195.00  193.59  194.27  ...  194.34  190.9995  183.4512
2023-12-08 05:00:00+00:00  194.20  195.99  193.67  195.71  ...  195.03  191.2925  183.9482
Note: If you were to look at the first 49 rows of the DataFrame (print(df.head(50))), you would see NaN (Not a Number) in the sma_50 column because there isn't enough preceding data to calculate the average.


