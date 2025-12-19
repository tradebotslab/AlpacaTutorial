"""
Alpaca Trading Course - Lesson 27
Understanding Your Results – Analyzing a Backtest Report

This script demonstrates how to analyze backtest results in depth, focusing on
critical metrics: Annual Return, Max Drawdown, Sharpe Ratio, and Win Rate.

It extends the backtest from Lesson 26 with detailed analysis and interpretation
of the results to help you understand if your strategy is genuinely robust.
"""

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import os
import importlib.util


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

        # If the short MA crosses below the long MA, and we are in a position, sell.
        elif crossover(self.long_ma, self.short_ma):
            if self.position:
                self.sell()


def calculate_annual_return(total_return, start_date, end_date):
    """
    Calculate annualized return from total return and time period.
    
    Args:
        total_return: Total return as a percentage (e.g., 50 for 50%)
        start_date: Start date of backtest
        end_date: End date of backtest
    
    Returns:
        Annual return as a percentage
    """
    # Calculate number of years
    days = (end_date - start_date).days
    years = days / 365.25
    
    if years <= 0:
        return 0.0
    
    # Convert percentage to decimal
    total_return_decimal = total_return / 100.0
    
    # Calculate annualized return using compound annual growth rate (CAGR)
    # CAGR = (End Value / Start Value)^(1/years) - 1
    annual_return_decimal = (1 + total_return_decimal) ** (1 / years) - 1
    
    return annual_return_decimal * 100


def interpret_sharpe_ratio(sharpe_ratio):
    """
    Provide interpretation of Sharpe Ratio.
    
    Args:
        sharpe_ratio: Sharpe Ratio value
    
    Returns:
        Interpretation string
    """
    if sharpe_ratio < 1.0:
        return "❌ Not great - Returns do not justify the risk taken"
    elif sharpe_ratio < 2.0:
        return "✅ Good - Decent risk-adjusted returns"
    elif sharpe_ratio < 3.0:
        return "✅✅ Very good - Excellent risk-adjusted returns"
    else:
        return "⚠️ Excellent (but may be 'too good to be true' - check for overfitting)"


def interpret_drawdown(drawdown_percent):
    """
    Provide interpretation of Max Drawdown.
    
    Args:
        drawdown_percent: Max drawdown as a percentage (negative value)
    
    Returns:
        Interpretation string
    """
    drawdown_abs = abs(drawdown_percent)
    
    if drawdown_abs < 10:
        return "✅ Low risk - Manageable drawdown"
    elif drawdown_abs < 20:
        return "⚠️ Moderate risk - Requires discipline to hold through"
    elif drawdown_abs < 40:
        return "⚠️⚠️ High risk - Very difficult to stick with psychologically"
    else:
        return "❌ Extreme risk - Would wipe out most retail traders"


def analyze_win_rate(win_rate, profit_factor, avg_win, avg_loss):
    """
    Analyze win rate in context of profit factor and average win/loss.
    
    Args:
        win_rate: Win rate as percentage
        profit_factor: Profit factor (total wins / total losses)
        avg_win: Average winning trade percentage
        avg_loss: Average losing trade percentage
    
    Returns:
        Analysis string
    """
    analysis = []
    
    # Win rate interpretation
    if win_rate >= 60:
        analysis.append(f"✅ High win rate ({win_rate:.1f}%) - Psychologically comforting")
    elif win_rate >= 40:
        analysis.append(f"✅ Moderate win rate ({win_rate:.1f}%) - Acceptable")
    else:
        analysis.append(f"⚠️ Low win rate ({win_rate:.1f}%) - Requires discipline")
    
    # Profit factor interpretation
    if profit_factor > 2.0:
        analysis.append(f"✅✅ Excellent profit factor ({profit_factor:.2f}) - Wins significantly outweigh losses")
    elif profit_factor > 1.5:
        analysis.append(f"✅ Good profit factor ({profit_factor:.2f}) - Wins outweigh losses")
    elif profit_factor > 1.0:
        analysis.append(f"⚠️ Marginal profit factor ({profit_factor:.2f}) - Barely profitable")
    else:
        analysis.append(f"❌ Poor profit factor ({profit_factor:.2f}) - Losing strategy")
    
    # Average win vs loss
    if avg_win > abs(avg_loss) * 2:
        analysis.append(f"✅ Large wins vs small losses - Good risk/reward ratio")
    elif avg_win > abs(avg_loss):
        analysis.append(f"✅ Wins larger than losses - Positive expectancy")
    else:
        analysis.append(f"⚠️ Losses larger than wins - High win rate may be misleading")
    
    return "\n   ".join(analysis)


def print_detailed_analysis(stats, start_date, end_date):
    """
    Print comprehensive analysis of backtest results.
    
    Args:
        stats: Backtest statistics from backtesting.py
        start_date: Start date of backtest
        end_date: End date of backtest
    """
    print("\n" + "="*70)
    print("📊 DETAILED BACKTEST ANALYSIS")
    print("="*70)
    
    # 1. ANNUAL RETURN
    print("\n" + "─"*70)
    print("1️⃣  ANNUAL RETURN")
    print("─"*70)
    
    total_return = stats['Return [%]']
    annual_return = calculate_annual_return(total_return, start_date, end_date)
    buy_hold_return = stats['Buy & Hold Return [%]']
    buy_hold_annual = calculate_annual_return(buy_hold_return, start_date, end_date)
    
    print(f"   Total Return: {total_return:.2f}%")
    print(f"   Annual Return: {annual_return:.2f}%")
    print(f"   Buy & Hold Annual Return: {buy_hold_annual:.2f}%")
    
    if annual_return > buy_hold_annual:
        outperformance = annual_return - buy_hold_annual
        print(f"   ✅ Strategy outperforms Buy & Hold by {outperformance:.2f}% annually")
    elif annual_return < buy_hold_annual:
        underperformance = buy_hold_annual - annual_return
        print(f"   ⚠️  Strategy underperforms Buy & Hold by {underperformance:.2f}% annually")
        print(f"   💡 Consider: Is the added complexity worth it?")
    else:
        print(f"   ➡️  Strategy matches Buy & Hold")
    
    print(f"\n   📝 Why it matters:")
    print(f"      Annual Return standardizes performance for comparison.")
    print(f"      A 50% return over 5 years (≈8.4% annually) is very different")
    print(f"      from a 50% return in 1 year (50% annually).")
    
    # 2. MAX DRAWDOWN
    print("\n" + "─"*70)
    print("2️⃣  MAX DRAWDOWN")
    print("─"*70)
    
    max_drawdown = stats['Max. Drawdown [%]']
    print(f"   Max Drawdown: {max_drawdown:.2f}%")
    print(f"   {interpret_drawdown(max_drawdown)}")
    
    # Calculate what the portfolio would have dropped to
    initial_value = stats['Start'] if 'Start' in stats else 10000
    peak_value = initial_value * (1 + (total_return / 100))
    trough_value = peak_value * (1 + (max_drawdown / 100))
    
    print(f"\n   📊 Example:")
    print(f"      If your portfolio peaked at ${peak_value:,.2f},")
    print(f"      it would have dropped to ${trough_value:,.2f} at the worst point.")
    print(f"      That's a loss of ${peak_value - trough_value:,.2f}.")
    
    print(f"\n   📝 Why it matters:")
    print(f"      This is the metric of psychological pain.")
    print(f"      Could you stomach this loss without panicking and selling?")
    print(f"      A low drawdown = more stable, less stressful strategy.")
    
    # 3. SHARPE RATIO
    print("\n" + "─"*70)
    print("3️⃣  SHARPE RATIO")
    print("─"*70)
    
    sharpe_ratio = stats['Sharpe Ratio']
    print(f"   Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"   {interpret_sharpe_ratio(sharpe_ratio)}")
    
    print(f"\n   📝 Why it matters:")
    print(f"      Measures risk-adjusted return.")
    print(f"      A 20% return with wild swings might be worse than")
    print(f"      a 15% return with smooth, steady growth.")
    print(f"      Higher Sharpe Ratio = better return per unit of risk.")
    
    # 4. WIN RATE AND PROFIT FACTOR
    print("\n" + "─"*70)
    print("4️⃣  WIN RATE & PROFIT FACTOR")
    print("─"*70)
    
    if stats['# Trades'] > 0:
        win_rate = stats['Win Rate [%]']
        profit_factor = stats.get('Profit Factor', 0)
        avg_win = stats.get('Avg. Win [%]', 0)
        avg_loss = stats.get('Avg. Loss [%]', 0)
        
        print(f"   Win Rate: {win_rate:.2f}%")
        print(f"   Profit Factor: {profit_factor:.2f}")
        print(f"   Average Win: {avg_win:.2f}%")
        print(f"   Average Loss: {avg_loss:.2f}%")
        
        print(f"\n   📊 Analysis:")
        print(f"   {analyze_win_rate(win_rate, profit_factor, avg_win, avg_loss)}")
        
        print(f"\n   📝 Why it matters:")
        print(f"      Win rate alone can be misleading!")
        print(f"      Scenario A: 90% win rate, but avg loss ($100) > avg win ($10)")
        print(f"      → Net loss despite high win rate")
        print(f"      Scenario B: 40% win rate, but avg win ($100) > avg loss ($20)")
        print(f"      → Net profit despite low win rate")
        print(f"      Always look at win rate WITH profit factor!")
    else:
        print(f"   ⚠️  No trades executed - cannot analyze win rate")
    
    # 5. OVERALL ASSESSMENT
    print("\n" + "─"*70)
    print("5️⃣  OVERALL ASSESSMENT")
    print("─"*70)
    
    # Count positive indicators
    positive_indicators = 0
    total_indicators = 0
    
    # Annual return vs buy & hold
    total_indicators += 1
    if annual_return > buy_hold_annual:
        positive_indicators += 1
    
    # Drawdown
    total_indicators += 1
    if abs(max_drawdown) < 20:
        positive_indicators += 1
    
    # Sharpe ratio
    total_indicators += 1
    if sharpe_ratio >= 1.0:
        positive_indicators += 1
    
    # Profit factor (if available)
    if stats['# Trades'] > 0:
        total_indicators += 1
        profit_factor = stats.get('Profit Factor', 0)
        if profit_factor > 1.5:
            positive_indicators += 1
    
    score = (positive_indicators / total_indicators) * 100
    
    print(f"   Strategy Score: {score:.0f}% ({positive_indicators}/{total_indicators} key metrics positive)")
    
    if score >= 75:
        print(f"   ✅✅ STRONG STRATEGY - Multiple positive indicators")
        print(f"      This strategy shows promise. Consider paper trading next.")
    elif score >= 50:
        print(f"   ✅ MODERATE STRATEGY - Some positive indicators")
        print(f"      Strategy has potential but needs refinement.")
        print(f"      Consider optimizing parameters or adding filters.")
    else:
        print(f"   ⚠️  WEAK STRATEGY - Few positive indicators")
        print(f"      Strategy needs significant improvement.")
        print(f"      Consider going back to the drawing board.")
    
    print("\n" + "="*70)
    print("💡 KEY TAKEAWAY")
    print("="*70)
    print("Never judge a strategy by a single number!")
    print("Analyze all metrics together to understand the full story.")
    print("A strategy with lower returns but better risk metrics")
    print("may be superior to a high-return, high-risk strategy.")
    print("="*70 + "\n")


def print_basic_results(stats):
    """
    Print basic backtest results in a readable format.
    """
    print("\n" + "="*70)
    print("📊 BASIC BACKTEST RESULTS")
    print("="*70)
    
    # Key metrics
    print(f"\n💰 Return: {stats['Return [%]']:.2f}%")
    print(f"📈 Buy & Hold Return: {stats['Buy & Hold Return [%]']:.2f}%")
    print(f"📉 Max. Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
    print(f"📊 Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
    print(f"🔢 # Trades: {stats['# Trades']}")
    
    if stats['# Trades'] > 0:
        print(f"✅ Win Rate: {stats['Win Rate [%]']:.2f}%")
        if 'Profit Factor' in stats:
            print(f"📊 Profit Factor: {stats['Profit Factor']:.2f}")
        print(f"📊 Avg. Trade: {stats['Avg. Trade [%]']:.2f}%")
        print(f"📈 Best Trade: {stats['Best Trade [%]']:.2f}%")
        print(f"📉 Worst Trade: {stats['Worst Trade [%]']:.2f}%")
    
    print("="*70 + "\n")


def main():
    """
    Main function to run the backtest and detailed analysis.
    """
    print("="*70)
    print("📚 Alpaca Trading Course - Lesson 27")
    print("📖 Understanding Your Results – Analyzing a Backtest Report")
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
    
    # Print basic results
    print_basic_results(stats)
    
    # Print detailed analysis
    print_detailed_analysis(stats, START_DATE, END_DATE)
    
    # Generate and open interactive plot
    print("📈 Generating interactive plot...")
    print("   (This will open in your default web browser)")
    print()
    bt.plot()
    
    print("\n✅ Backtest analysis complete!")
    print("\n💡 Tip: The interactive plot shows:")
    print("   - Equity curve (portfolio value over time)")
    print("   - Buy and sell signals")
    print("   - Moving averages")
    print("   - Trade markers")
    print("\n📚 Remember: Past performance does not guarantee future results!")


if __name__ == '__main__':
    main()

