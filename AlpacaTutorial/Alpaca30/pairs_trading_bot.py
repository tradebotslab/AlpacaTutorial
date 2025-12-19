"""
Alpaca Trading Course - Lesson 30
A Step Towards PRO – Statistical Arbitrage (Pairs Trading)

This script implements a market-neutral pairs trading strategy that profits from
temporary distortions in the price relationship between two highly correlated assets.

Strategy Overview:
- Find two cointegrated assets (e.g., KO and PEP)
- Calculate the spread between their prices
- Trade when the spread deviates significantly from its historical mean
- Profit from mean reversion of the spread

Key Concepts:
- Cointegration: Statistical relationship between two time series
- Spread: Price difference or ratio between two assets
- Z-Score: Number of standard deviations from the mean
- Market Neutrality: Profit from relative performance, not market direction
"""

import pandas as pd
import numpy as np
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest, OrderSide
from alpaca.trading.enums import OrderSide as OrderSideEnum, TimeInForce
from datetime import datetime, timedelta
import os
import json
import logging
from typing import Tuple, Optional
from statsmodels.tsa.stattools import coint
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pairs_trading.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG_FILE = 'config.py'
STATE_FILE = 'pairs_trading_state.json'


def load_config():
    """
    Load API credentials from config.py file.
    """
    if not os.path.exists(CONFIG_FILE):
        logger.error(f"{CONFIG_FILE} not found!")
        logger.error(f"Please copy config.example.py to {CONFIG_FILE} and add your API keys.")
        exit(1)
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", CONFIG_FILE)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        return config.API_KEY, config.SECRET_KEY, config.BASE_URL
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        exit(1)


def load_state():
    """Load bot state from JSON file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading state: {e}")
    return {
        'position': None,  # 'long_spread', 'short_spread', or None
        'entry_z_score': None,
        'entry_time': None,
        'symbol_a': None,
        'symbol_b': None
    }


def save_state(state):
    """Save bot state to JSON file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving state: {e}")


def get_historical_data(symbol: str, days: int, api_key: str, secret_key: str) -> pd.DataFrame:
    """
    Fetch historical price data for a symbol.
    
    Args:
        symbol: Stock symbol (e.g., 'KO')
        days: Number of days of historical data
        api_key: Alpaca API key
        secret_key: Alpaca secret key
    
    Returns:
        DataFrame with 'close' prices
    """
    try:
        client = StockHistoricalDataClient(api_key, secret_key)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        request = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame.Day,
            start=start_date,
            end=end_date
        )
        
        bars = client.get_stock_bars(request)
        
        if not bars.data:
            logger.error(f"No data returned for {symbol}")
            return pd.DataFrame()
        
        df = pd.DataFrame([{
            'timestamp': bar.timestamp,
            'close': float(bar.close)
        } for bar in bars.data[symbol]])
        
        df.set_index('timestamp', inplace=True)
        return df
    
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()


def test_cointegration(series_a: pd.Series, series_b: pd.Series) -> Tuple[bool, float]:
    """
    Test if two time series are cointegrated using Augmented Dickey-Fuller test.
    
    Args:
        series_a: First time series
        series_b: Second time series
    
    Returns:
        Tuple of (is_cointegrated, p_value)
    """
    try:
        # Calculate spread (price difference)
        spread = series_a - series_b
        
        # Perform cointegration test
        score, p_value, _ = coint(series_a.values, series_b.values)
        
        # Typically, p-value < 0.05 indicates cointegration
        is_cointegrated = p_value < 0.05
        
        return is_cointegrated, p_value
    except Exception as e:
        logger.error(f"Error testing cointegration: {e}")
        return False, 1.0


def calculate_spread_stats(series_a: pd.Series, series_b: pd.Series, lookback: int = 60) -> dict:
    """
    Calculate spread statistics (mean, std, z-score).
    
    Args:
        series_a: First time series
        series_b: Second time series
        lookback: Number of periods for rolling statistics
    
    Returns:
        Dictionary with spread statistics
    """
    # Calculate spread
    spread = series_a - series_b
    
    # Use rolling window for dynamic statistics
    rolling_mean = spread.rolling(window=lookback).mean()
    rolling_std = spread.rolling(window=lookback).std()
    
    # Current spread
    current_spread = spread.iloc[-1]
    current_mean = rolling_mean.iloc[-1]
    current_std = rolling_std.iloc[-1]
    
    # Calculate z-score
    if current_std > 0:
        z_score = (current_spread - current_mean) / current_std
    else:
        z_score = 0.0
    
    return {
        'spread': current_spread,
        'mean': current_mean,
        'std': current_std,
        'z_score': z_score,
        'spread_series': spread
    }


def get_current_price(symbol: str, trading_client: TradingClient) -> Optional[float]:
    """Get current market price for a symbol."""
    try:
        position = trading_client.get_open_position(symbol)
        return float(position.current_price)
    except:
        try:
            # If no position, get latest bar
            from alpaca.data.historical import StockHistoricalDataClient
            from alpaca.data.requests import StockLatestBarRequest
            
            api_key, secret_key, _ = load_config()
            data_client = StockHistoricalDataClient(api_key, secret_key)
            request = StockLatestBarRequest(symbol_or_symbols=[symbol])
            bar = data_client.get_stock_latest_bar(request)
            
            if bar and symbol in bar:
                return float(bar[symbol].close)
        except Exception as e:
            logger.error(f"Error getting price for {symbol}: {e}")
    
    return None


def calculate_position_size(account_value: float, risk_per_trade: float = 0.02) -> float:
    """
    Calculate position size based on account value and risk per trade.
    
    Args:
        account_value: Total account value
        risk_per_trade: Percentage of account to risk per trade (default 2%)
    
    Returns:
        Position size in dollars
    """
    return account_value * risk_per_trade


def execute_pairs_trade(
    trading_client: TradingClient,
    symbol_a: str,
    symbol_b: str,
    side: str,  # 'long_spread' or 'short_spread'
    position_size: float
):
    """
    Execute a pairs trade: simultaneously trade both assets.
    
    Args:
        trading_client: Alpaca trading client
        symbol_a: First symbol
        symbol_b: Second symbol
        side: 'long_spread' (buy A, sell B) or 'short_spread' (sell A, buy B)
        position_size: Dollar amount for each leg
    """
    try:
        # Get current prices
        price_a = get_current_price(symbol_a, trading_client)
        price_b = get_current_price(symbol_b, trading_client)
        
        if not price_a or not price_b:
            logger.error("Could not get current prices")
            return False
        
        # Calculate shares
        shares_a = int(position_size / price_a)
        shares_b = int(position_size / price_b)
        
        if shares_a < 1 or shares_b < 1:
            logger.warning("Position size too small for minimum shares")
            return False
        
        # Execute trades based on spread direction
        if side == 'long_spread':
            # Long spread: Buy A, Sell B
            logger.info(f"Executing LONG SPREAD: BUY {shares_a} {symbol_a}, SELL {shares_b} {symbol_b}")
            
            order_a = MarketOrderRequest(
                symbol=symbol_a,
                qty=shares_a,
                side=OrderSideEnum.BUY,
                time_in_force=TimeInForce.DAY
            )
            
            order_b = MarketOrderRequest(
                symbol=symbol_b,
                qty=shares_b,
                side=OrderSideEnum.SELL,
                time_in_force=TimeInForce.DAY
            )
        
        else:  # short_spread
            # Short spread: Sell A, Buy B
            logger.info(f"Executing SHORT SPREAD: SELL {shares_a} {symbol_a}, BUY {shares_b} {symbol_b}")
            
            order_a = MarketOrderRequest(
                symbol=symbol_a,
                qty=shares_a,
                side=OrderSideEnum.SELL,
                time_in_force=TimeInForce.DAY
            )
            
            order_b = MarketOrderRequest(
                symbol=symbol_b,
                qty=shares_b,
                side=OrderSideEnum.BUY,
                time_in_force=TimeInForce.DAY
            )
        
        # Submit both orders
        trading_client.submit_order(order_a)
        trading_client.submit_order(order_b)
        
        logger.info("✅ Pairs trade executed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error executing pairs trade: {e}")
        return False


def close_pairs_position(trading_client: TradingClient, symbol_a: str, symbol_b: str):
    """
    Close existing pairs position by closing both legs.
    """
    try:
        # Close position A
        try:
            position_a = trading_client.get_open_position(symbol_a)
            close_order_a = MarketOrderRequest(
                symbol=symbol_a,
                qty=abs(int(position_a.qty)),
                side=OrderSideEnum.SELL if position_a.qty > 0 else OrderSideEnum.BUY,
                time_in_force=TimeInForce.DAY
            )
            trading_client.submit_order(close_order_a)
            logger.info(f"Closed position in {symbol_a}")
        except:
            pass
        
        # Close position B
        try:
            position_b = trading_client.get_open_position(symbol_b)
            close_order_b = MarketOrderRequest(
                symbol=symbol_b,
                qty=abs(int(position_b.qty)),
                side=OrderSideEnum.SELL if position_b.qty > 0 else OrderSideEnum.BUY,
                time_in_force=TimeInForce.DAY
            )
            trading_client.submit_order(close_order_b)
            logger.info(f"Closed position in {symbol_b}")
        except:
            pass
        
        logger.info("✅ Pairs position closed")
        return True
    
    except Exception as e:
        logger.error(f"Error closing pairs position: {e}")
        return False


def main():
    """
    Main pairs trading bot logic.
    """
    logger.info("=" * 60)
    logger.info("Pairs Trading Bot - Lesson 30")
    logger.info("=" * 60)
    
    # Load configuration
    api_key, secret_key, base_url = load_config()
    
    # Initialize clients
    trading_client = TradingClient(api_key, secret_key, paper=True)
    
    # Configuration
    SYMBOL_A = "KO"  # Coca-Cola
    SYMBOL_B = "PEP"  # Pepsi
    LOOKBACK_DAYS = 252  # ~1 year of trading days
    Z_SCORE_ENTRY = 2.0  # Enter when z-score > 2 or < -2
    Z_SCORE_EXIT = 0.5  # Exit when z-score returns to < 0.5
    RISK_PER_TRADE = 0.02  # 2% of account per trade
    
    logger.info(f"Pair: {SYMBOL_A} / {SYMBOL_B}")
    logger.info(f"Entry threshold: Z-score > {Z_SCORE_ENTRY} or < -{Z_SCORE_ENTRY}")
    logger.info(f"Exit threshold: Z-score < {Z_SCORE_EXIT}")
    
    # Load state
    state = load_state()
    
    # Fetch historical data
    logger.info(f"Fetching historical data for {SYMBOL_A} and {SYMBOL_B}...")
    data_a = get_historical_data(SYMBOL_A, LOOKBACK_DAYS, api_key, secret_key)
    data_b = get_historical_data(SYMBOL_B, LOOKBACK_DAYS, api_key, secret_key)
    
    if data_a.empty or data_b.empty:
        logger.error("Failed to fetch historical data")
        return
    
    # Align dataframes
    combined = pd.concat([data_a['close'], data_b['close']], axis=1, keys=[SYMBOL_A, SYMBOL_B])
    combined = combined.dropna()
    
    if len(combined) < 60:
        logger.error("Insufficient data for analysis")
        return
    
    series_a = combined[SYMBOL_A]
    series_b = combined[SYMBOL_B]
    
    # Test cointegration
    logger.info("Testing cointegration...")
    is_cointegrated, p_value = test_cointegration(series_a, series_b)
    
    if not is_cointegrated:
        logger.warning(f"⚠️  Assets are NOT cointegrated (p-value: {p_value:.4f})")
        logger.warning("This pair may not be suitable for pairs trading.")
        logger.warning("Consider using a different pair or proceed with caution.")
    else:
        logger.info(f"✅ Assets are cointegrated (p-value: {p_value:.4f})")
    
    # Calculate spread statistics
    stats = calculate_spread_stats(series_a, series_b, lookback=60)
    current_z = stats['z_score']
    
    logger.info(f"Current spread: ${stats['spread']:.2f}")
    logger.info(f"Spread mean: ${stats['mean']:.2f}")
    logger.info(f"Spread std: ${stats['std']:.2f}")
    logger.info(f"Current Z-score: {current_z:.2f}")
    
    # Get account info
    account = trading_client.get_account()
    account_value = float(account.portfolio_value)
    logger.info(f"Account value: ${account_value:,.2f}")
    
    # Check for existing position
    has_position_a = False
    has_position_b = False
    
    try:
        trading_client.get_open_position(SYMBOL_A)
        has_position_a = True
    except:
        pass
    
    try:
        trading_client.get_open_position(SYMBOL_B)
        has_position_b = True
    except:
        pass
    
    # Trading logic
    if has_position_a or has_position_b:
        # We have an open position
        logger.info("Open position detected")
        
        if state['position']:
            entry_z = state.get('entry_z_score', 0)
            
            # Exit conditions
            if state['position'] == 'long_spread' and current_z <= Z_SCORE_EXIT:
                logger.info(f"Exit signal: Z-score ({current_z:.2f}) <= {Z_SCORE_EXIT}")
                close_pairs_position(trading_client, SYMBOL_A, SYMBOL_B)
                state['position'] = None
                state['entry_z_score'] = None
                state['entry_time'] = None
                save_state(state)
            
            elif state['position'] == 'short_spread' and current_z >= -Z_SCORE_EXIT:
                logger.info(f"Exit signal: Z-score ({current_z:.2f}) >= {-Z_SCORE_EXIT}")
                close_pairs_position(trading_client, SYMBOL_A, SYMBOL_B)
                state['position'] = None
                state['entry_z_score'] = None
                state['entry_time'] = None
                save_state(state)
            
            else:
                logger.info(f"Position held. Entry Z: {entry_z:.2f}, Current Z: {current_z:.2f}")
        else:
            # Position exists but not in state - close it
            logger.warning("Position exists but not in state. Closing...")
            close_pairs_position(trading_client, SYMBOL_A, SYMBOL_B)
    
    else:
        # No position - look for entry signals
        logger.info("No open position. Looking for entry signals...")
        
        if current_z >= Z_SCORE_ENTRY:
            # Spread is too wide - short the spread (sell A, buy B)
            logger.info(f"Entry signal: Z-score ({current_z:.2f}) >= {Z_SCORE_ENTRY}")
            
            position_size = calculate_position_size(account_value, RISK_PER_TRADE)
            
            if execute_pairs_trade(trading_client, SYMBOL_A, SYMBOL_B, 'short_spread', position_size):
                state['position'] = 'short_spread'
                state['entry_z_score'] = current_z
                state['entry_time'] = datetime.now().isoformat()
                state['symbol_a'] = SYMBOL_A
                state['symbol_b'] = SYMBOL_B
                save_state(state)
        
        elif current_z <= -Z_SCORE_ENTRY:
            # Spread is too narrow - long the spread (buy A, sell B)
            logger.info(f"Entry signal: Z-score ({current_z:.2f}) <= -{Z_SCORE_ENTRY}")
            
            position_size = calculate_position_size(account_value, RISK_PER_TRADE)
            
            if execute_pairs_trade(trading_client, SYMBOL_A, SYMBOL_B, 'long_spread', position_size):
                state['position'] = 'long_spread'
                state['entry_z_score'] = current_z
                state['entry_time'] = datetime.now().isoformat()
                state['symbol_a'] = SYMBOL_A
                state['symbol_b'] = SYMBOL_B
                save_state(state)
        
        else:
            logger.info(f"No entry signal. Z-score ({current_z:.2f}) within bounds.")
    
    logger.info("=" * 60)
    logger.info("Bot execution complete")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()


