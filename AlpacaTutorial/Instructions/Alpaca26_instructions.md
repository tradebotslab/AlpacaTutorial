Lesson 26: Time Travel – The Basics of Backtesting Your Strategy
Welcome to Lesson 26. So far, you have a resilient, autonomous bot. But the most important question remains: Is your trading strategy actually profitable? Deploying an untested strategy, even with paper money, is like setting sail without a map. You might get lucky, but you're more likely to get lost.

This is where backtesting comes in. Backtesting is the process of simulating your trading strategy on historical market data to see how it would have performed in the past. In this lesson, you'll learn the basics of "time travel" by using the powerful backtesting.py library to test your ideas before risking a single dollar.

Why Backtest? The Power of Hindsight
Backtesting allows you to answer critical questions about your strategy:

Would it have made money over the last year? The last five years?

How much risk did it involve? What was the largest loss it would have suffered?

How does it perform compared to simply buying and holding the stock?

How sensitive is it to small changes in its parameters?

The key advantage of backtesting over live paper trading is speed. You can simulate years of trading in seconds, allowing for rapid iteration and refinement of your ideas.

Setting Up Your Backtesting Environment
We will use backtesting.py, a fantastic library that does most of the heavy lifting for us. We'll also need to fetch historical data.

1. Install Libraries:
Open your terminal and install the required libraries:

bash
pip install backtesting pandas
# You should already have the alpaca-trade-api installed
2. Get Historical Data:
backtesting.py requires historical data in a pandas DataFrame with specific column names: Open, High, Low, Close, and Volume (case-sensitive). We can easily get this data from Alpaca's Market Data API.

python
import pandas as pd
from alpaca.data.historical import StockHistClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime

# --- Your Alpaca API Credentials ---
# Best to load these from your config.json file
API_KEY = 'YOUR_API_KEY' 
API_SECRET = 'YOUR_SECRET_KEY'

def get_historical_data(symbol, start_date, end_date):
    """
    Fetches historical OHLCV data from Alpaca.
    """
    client = StockHistClient(API_KEY, API_SECRET)
    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date
    )
    bars = client.get_stock_bars(request_params)
    df = bars.df
    
    # The library requires column names in a specific format
    df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)
    
    return df
Creating Your First Strategy: The Moving Average Crossover
A Moving Average Crossover is a classic trend-following strategy. The logic is simple:

Buy Signal: When a faster (shorter-period) moving average crosses above a slower (longer-period) moving average, it suggests the start of an uptrend.

Sell Signal: When the short MA crosses below the long MA, it suggests the start of a downtrend.

Let's implement this using backtesting.py.

python
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# We need a way to calculate indicators. The library can help.
from backtesting.test import SMA

class SmaCross(Strategy):
    # Define the two MA lengths as class variables
    short_ma_period = 10
    long_ma_period = 30

    def init(self):
        # This method is called once at the start.
        # We pre-calculate the indicators here.
        self.short_ma = self.I(SMA, self.data.Close, self.short_ma_period)
        self.long_ma = self.I(SMA, self.data.Close, self.long_ma_period)

    def next(self):
        # This method is called for each data point (each day in our case).
        # `crossover()` is a helper function from the library.
        
        # If the short MA crosses above the long MA, and we're not in a position, buy.
        if crossover(self.short_ma, self.long_ma):
            if not self.position:
                self.buy()

        # If the short MA crosses below the long MA, and we are in a position, sell.
        elif crossover(self.long_ma, self.short_ma):
            if self.position:
                self.sell()
Running the Backtest and Interpreting the Results
Now, let's put it all together: fetch the data, define the backtest, and run it.

python
if __name__ == '__main__':
    # --- 1. Fetch Data ---
    start = datetime(2020, 1, 1)
    end = datetime(2022, 12, 31)
    data = get_historical_data("TSLA", start, end)

    # --- 2. Run Backtest ---
    # Instantiate the Backtest class
    bt = Backtest(
        data,             # The historical data
        SmaCross,         # Our strategy class
        cash=10000,       # Initial cash
        commission=.002   # Broker commission (e.g., 0.2%)
    )
    
    # Run the backtest
    stats = bt.run()
    
    # --- 3. Print and Visualize ---
    print(stats)
    bt.plot()
The Output
The stats variable contains a wealth of information. Here are some of the most important metrics:

Metric	Description
Return
The total percentage gain or loss for the strategy over the entire period.
Buy & Hold Return
The return you would have gotten if you just bought the asset at the start and sold at the end. This is your benchmark. Did your strategy beat it?
Max. Drawdown
The largest percentage drop from a portfolio peak to a subsequent trough. This is a key measure of risk. A high drawdown means your strategy suffered large losses at some point.
Sharpe Ratio	A measure of risk-adjusted return. Higher is generally better. It tells you how much return you got for the amount of risk you took.
# Trades	The total number of trades executed. Too few might mean the results aren't statistically significant. Too many might mean you're losing a lot to commissions.
The bt.plot() command will generate and open an interactive HTML file in your browser. This plot is incredibly useful, showing your equity curve, the points where trades were made, and the indicators you used.

Conclusion
Backtesting is an indispensable skill for any algorithmic trader. It allows you to fail fast and cheap, discarding bad ideas and refining promising ones without losing real money. While a positive backtest is no guarantee of future results, a negative backtest is a strong signal that you should go back to the drawing board.

In the next lessons, we'll explore more complex strategies and further refine our backtesting process. See you there!