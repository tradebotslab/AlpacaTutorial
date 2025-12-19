Lesson 3: Fetching Market Data – Your First Candlestick
Welcome to Lesson 3 of the Alpaca Trading Course! In the last lesson, you set up your Python environment and connected to Alpaca. Now it's time to get the "fuel" for any trading strategy: market data. Before your bot can make any decisions, it needs to know what has happened in the market.

In this lesson, you'll write your first functional piece of code to retrieve historical price data for any stock, giving your bot the context it needs to begin its analysis.

The Problem: A Single Price Is Not Enough
Knowing the current price of a stock is useful, but it tells you very little. Is the stock on an upward trend? Is it unusually volatile today? A single data point offers no context. To build any meaningful strategy, you need to analyze historical data patterns.

Problem/Challenge	Description
No Context	The current price doesn't tell you if the market is trending up, down, or sideways.
No Volatility Measure	You can't know the day's trading range (the high and low) just from one price point.
Analysis is Impossible	Virtually all technical indicators (like moving averages) require a series of historical prices to be calculated.
The Solution: The OHLC Candlestick
The standard way to represent historical price action is with OHLCV data, which stands for Open, High, Low, Close, and Volume. This data is often visualized as a "candlestick" and gives a complete picture of the trading activity within a specific period (e.g., a day, an hour).

We will use the Alpaca Market Data API to fetch this structured data programmatically.

Step 3.1: Write the Code to Fetch Data
First, we need to write a Python script to communicate with Alpaca's data endpoint. We'll use the official alpaca-trade-api library.

Create a new Python file (e.g., fetch_data.py) and add the following code. Make sure to replace the placeholder keys with the real API keys you generated in Lesson 1.

python
import os
from datetime import datetime
from alpaca.data.historical import StockHistClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# --- Your Alpaca API Credentials ---
# IMPORTANT: It's best practice to set these as environment variables
# or use a config file, not to hardcode them like this.
# We'll cover that in a later lesson.
API_KEY = "YOUR_API_KEY_ID"
SECRET_KEY = "YOUR_SECRET_KEY"

# 1. Instantiate a Stock Historical Data Client
client = StockHistClient(api_key=API_KEY, secret_key=SECRET_KEY)

# 2. Define the Request Parameters
request_params = StockBarsRequest(
    symbol_or_symbols=["AAPL"],
    timeframe=TimeFrame.Day,
    start=datetime(2023, 1, 1),
    end=datetime(2023, 1, 10)
)

# 3. Fetch the Data
# The get_stock_bars() method returns a dictionary, with the symbol as the key
# and a list of bar objects as the value. We can access the dataframe with .df
bars_df = client.get_stock_bars(request_params).df

# 4. Print the Data
print(bars_df)
Step 3.2: Run the Script and See the Output
Open your terminal, navigate to the folder containing your script, and run it:

bash
python fetch_data.py
You should see output that looks something like this (dates and prices will vary):

                      open     high      low    close   volume trade_count         vwap
symbol timestamp                                                                       
AAPL   2023-01-03 12:00:00+00:00  130.28  130.900  124.170  125.07  112117500      820835  126.449103
       2023-01-04 12:00:00+00:00  126.89  128.655  125.080  126.36   89113600      673444  126.920143
       2023-01-05 12:00:00+00:00  127.12  127.770  124.760  125.02   85925400      642646  126.255536
       2023-01-06 12:00:00+00:00  126.01  130.290  124.890  129.61   87693100      653303  128.144426
       2023-01-09 12:00:00+00:00  129.47  133.410  129.470  130.15   70790800      521997  131.624634
       2023-01-10 12:00:00+00:00  130.26  131.260  128.120  130.73   63896200      486632  129.939226
Step 3.3: Understanding Your First Candlestick
Congratulations! You've just fetched your first set of historical data. Each row in that output represents one "candlestick" for one day of trading for AAPL.

Column	Description
open	The price of the stock at the beginning of the period (e.g., at market open for TimeFrame.Day).
high	The highest price the stock reached during that period.
low	The lowest price the stock reached during that period.
close	The price of the stock at the end of the period (e.g., at market close).
volume	The total number of shares that were traded during that period.
vwap	Volume-Weighted Average Price. A measure of the average price weighted by volume.
This structured data is the fundamental building block for all technical analysis.

Important Considerations
Timeframes: Notice the timeframe=TimeFrame.Day parameter. You can change this to TimeFrame.Hour or TimeFrame.Minute to get more granular data, though the amount of history you can fetch may be more limited for smaller timeframes.

Data Format: The data is returned in a pandas DataFrame, a powerful data structure in Python that is the standard for any kind of data analysis. We will use it extensively in future lessons.

API Key Security: Hardcoding keys in your script is bad practice. We did it here for simplicity, but in future lessons, we'll learn how to manage them securely in a configuration file.

Conclusion
You have successfully fetched historical OHLCV data from the Alpaca API. You've moved from simply connecting to the service to actually retrieving the core information needed for trading analysis. You now have the power to programmatically access market history for thousands of stocks.

In the next lesson, we'll start using this data to calculate our first technical indicator: the Simple Moving Average.