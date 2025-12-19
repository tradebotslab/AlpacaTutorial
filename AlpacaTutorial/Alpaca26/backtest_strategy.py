"""
Alpaca Trading Course - Lesson 26
Time Travel – The Basics of Backtesting Your Strategy

This script demonstrates how to backtest a trading strategy using historical data
from Alpaca and the backtesting.py library.

Strategy: Moving Average Crossover (Golden Cross / Death Cross)
- Buy when short MA crosses above long MA
- Sell when short MA crosses below long MA
"""

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import json
import os


# Configuration
CONFIG_FILE = 'config.py'


def load_config():
    """
    Load API credentials from config.py file.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Error: {CONFIG_FILE} not found!")
        print(f"   Please copy config.example.py to {CONFIG_FILE} and add your API keys.")
        exit(1)
    
    try:
        # Import config as module
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", CONFIG_FILE)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return config.API_KEY, config.SECRET_KEY
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        exit(1)


def get_historical_data(symbol, start_date, end_date, api_key, secret_key):
    """
    Fetches historical OHLCV data from Alpaca.
    
    Args:
        symbol: Stock symbol (e.g., "TSLA", "SPY")
        start_date: Start date (datetime object)
        end_date: End date (datetime object)
        api_key: Alpaca API key
        secret_key: Alpaca secret key
    
    Returns:
        pandas DataFrame with columns: Open, High, Low, Close, Volume
    """
    try:
        print(f"📊 Fetching historical data for {symbol}...")
        print(f"   From: {start_date.strftime('%Y-%m-%d')}")
        print(f"   To: {end_date.strftime('%Y-%m-%d')}")
        
        client = StockHistoricalDataClient(api_key, secret_key)
        request_params = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Day,
            start=start_date,
            end=end_date
        )
        bars = client.get_stock_bars(request_params)
        df = bars.df
        
        # Handle multi-index if multiple symbols (we only use one)
        if isinstance(df.index, pd.MultiIndex):
            df = df.droplevel(0)
        
        # The library requires column names in a specific format (case-sensitive)
        df.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }, inplace=True)
        
        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # Sort by date
        df.sort_index(inplace=True)
        
        print(f"✅ Fetched {len(df)} days of data")
        return df
    
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        raise


class SmaCross(Strategy):
    """
    Moving Average Crossover Strategy
    
    This is a classic trend-following strategy:
    - Buy Signal (Golden Cross): When short MA crosses above long MA
    - Sell Signal (Death Cross): When short MA crosses below long MA
    """
    # Define the two MA lengths as class variables
    # These can be optimized later
    short_ma_period = 10
    long_ma_period = 30

    def init(self):
        """
        This method is called once at the start.
        We pre-calculate the indicators here for efficiency.
        """
        # Calculate moving averages
        # self.I() is a helper method that creates an indicator
        self.short_ma = self.I(SMA, self.data.Close, self.short_ma_period)
        self.long_ma = self.I(SMA, self.data.Close, self.long_ma_period)

    def next(self):
        """
        This method is called for each data point (each day in our case).
        Here we implement the trading logic.
        """
        # crossover() is a helper function from the library
        # It returns True when the first series crosses above the second
        
        # If the short MA crosses above the long MA, and we're not in a position, buy.
        if crossover(self.short_ma, self.long_ma):
            if not self.position:
                self.buy()
                print(f"📈 BUY signal at {self.data.index[-1].strftime('%Y-%m-%d')} - Price: ${self.data.Close[-1]:.2f}")

        # If the short MA crosses below the long MA, and we are in a position, sell.
        elif crossover(self.long_ma, self.short_ma):
            if self.position:
                self.sell()
                print(f"📉 SELL signal at {self.data.index[-1].strftime('%Y-%m-%d')} - Price: ${self.data.Close[-1]:.2f}")


def print_backtest_results(stats):
    """
    Print backtest results in a readable format.
    """
    print("\n" + "="*70)
    print("📊 BACKTEST RESULTS")
    print("="*70)
    
    # Key metrics
    print(f"\n💰 Return: {stats['Return [%]']:.2f}%")
    print(f"📈 Buy & Hold Return: {stats['Buy & Hold Return [%]']:.2f}%")
    print(f"📉 Max. Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"📊 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    print(f"🔢 # Trades: {stats['# Trades']}")
    
    if stats['# Trades'] > 0:
        print(f"✅ Win Rate: {stats['Win Rate [%]']:.2f}%")
        print(f"📊 Avg. Trade: {stats['Avg. Trade [%]']:.2f}%")
        print(f"📈 Best Trade: {stats['Best Trade [%]']:.2f}%")
        print(f"📉 Worst Trade: {stats['Worst Trade [%]']:.2f}%")
    
    print("\n" + "="*70)
    
    # Performance comparison
    strategy_return = stats['Return [%]']
    buy_hold_return = stats['Buy & Hold Return [%]']
    
    if strategy_return > buy_hold_return:
        print(f"✅ Strategy outperformed Buy & Hold by {strategy_return - buy_hold_return:.2f}%")
    elif strategy_return < buy_hold_return:
        print(f"⚠️  Strategy underperformed Buy & Hold by {buy_hold_return - strategy_return:.2f}%")
    else:
        print("➡️  Strategy performed equal to Buy & Hold")
    
    print("="*70 + "\n")


def main():
    """
    Main function to run the backtest.
    """
    print("="*70)
    print("📚 Alpaca Trading Course - Lesson 26")
    print("📖 Time Travel – The Basics of Backtesting Your Strategy")
    print("="*70)
    print()
    
    # Load configuration
    print("🔑 Loading API credentials...")
    api_key, secret_key = load_config()
    print("✅ Configuration loaded!")
    print()
    
    # Backtest parameters
    SYMBOL = "TSLA"
    START_DATE = datetime(2020, 1, 1)
    END_DATE = datetime(2022, 12, 31)
    INITIAL_CASH = 10000
    COMMISSION = 0.002  # 0.2% commission
    
    print(f"📊 Backtest Configuration:")
    print(f"   Symbol: {SYMBOL}")
    print(f"   Period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
    print(f"   Initial Cash: ${INITIAL_CASH:,.2f}")
    print(f"   Commission: {COMMISSION*100:.2f}%")
    print(f"   Strategy: Moving Average Crossover (10/30)")
    print()
    
    # Fetch historical data
    try:
        data = get_historical_data(SYMBOL, START_DATE, END_DATE, api_key, secret_key)
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return
    
    print()
    
    # Create and run backtest
    print("🚀 Running backtest...")
    print()
    
    bt = Backtest(
        data,              # The historical data
        SmaCross,          # Our strategy class
        cash=INITIAL_CASH, # Initial cash
        commission=COMMISSION  # Broker commission (e.g., 0.2%)
    )
    
    # Run the backtest
    stats = bt.run()
    
    # Print results
    print_backtest_results(stats)
    
    # Generate and open interactive plot
    print("📈 Generating interactive plot...")
    print("   (This will open in your default web browser)")
    print()
    bt.plot()
    
    print("\n✅ Backtest complete!")
    print("\n💡 Tip: The interactive plot shows:")
    print("   - Equity curve (portfolio value over time)")
    print("   - Buy and sell signals")
    print("   - Moving averages")
    print("   - Trade markers")


if __name__ == '__main__':
    main()


