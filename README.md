# Alpaca Trading Bot - Moving Average Crossover Strategy

This is a complete automated trading bot that implements a **Golden Cross / Death Cross** strategy using Simple Moving Averages (SMA). The bot trades automatically based on technical indicators without human intervention.

## 📋 Overview

This bot is part of **Tutorial 10** in the Alpaca Trading Course. It combines all the components from previous tutorials into a single, functioning trading system:

- **Main Loop**: Continuous monitoring of the market
- **Position Management**: Tracks whether we hold a position
- **Technical Analysis**: Calculates 20-day and 50-day SMAs
- **Signal Detection**: Identifies Golden Cross (buy) and Death Cross (sell) signals
- **Order Execution**: Automatically places buy/sell orders

## 🎯 Strategy Description

### Golden Cross (Buy Signal)
- Occurs when the 20-day SMA crosses **above** the 50-day SMA
- Indicates potential upward momentum
- Bot places a **BUY** order (if no position exists)

### Death Cross (Sell Signal)
- Occurs when the 20-day SMA crosses **below** the 50-day SMA
- Indicates potential downward momentum
- Bot places a **SELL** order (if a position exists)

## 🚀 Getting Started

### Prerequisites

1. **Alpaca Account**: Sign up at [alpaca.markets](https://alpaca.markets)
2. **Paper Trading API Keys**: Get your keys from the [Alpaca Dashboard](https://app.alpaca.markets/paper/dashboard/overview)
3. **Python 3.7+**: Make sure Python is installed

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/TomaszCieslar/AlpacaTutorial.git
   cd AlpacaTutorial
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API credentials**:
   ```bash
   # Copy the example config file
   cp config.py.example config.py
   
   # Edit config.py and add your API keys
   # API_KEY = "your_key_here"
   # SECRET_KEY = "your_secret_here"
   ```

### Running the Bot

```bash
python crossover_bot_final.py
```

The bot will:
- Start and display configuration information
- Check for existing positions
- Fetch market data every 5 minutes
- Calculate moving averages
- Detect crossover signals
- Place orders automatically when signals are detected

**To stop the bot**: Press `Ctrl+C`

## ⚙️ Configuration

You can modify these constants in `crossover_bot_final.py`:

```python
SYMBOL_TO_TRADE = "AAPL"        # Stock symbol to trade
QTY_PER_TRADE = 1               # Number of shares per trade
SMA_SHORT_WINDOW = 20           # Short-term SMA period (days)
SMA_LONG_WINDOW = 50            # Long-term SMA period (days)
LOOP_SLEEP_MINUTES = 5          # How often to check the market (minutes)
```

## 📁 Project Structure

```
AlpacaTutorial/
├── crossover_bot_final.py    # Main trading bot script
├── config.py.example          # Template for API credentials
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── instructions.md            # Detailed tutorial instructions
└── .gitignore                 # Git ignore rules
```

## 🔒 Security

- **Never commit `config.py`** - It contains your API keys
- The `.gitignore` file protects sensitive files
- Always use **Paper Trading** for testing
- Only switch to live trading after thorough testing

## 📚 How It Works

1. **Position Check**: At the start of each loop, the bot checks if it holds a position
2. **Data Fetching**: Retrieves historical price data (enough for the longest SMA)
3. **Indicator Calculation**: Computes 20-day and 50-day Simple Moving Averages
4. **Signal Detection**: Compares current and previous day's SMAs to detect crossovers
5. **Order Placement**: Places buy/sell orders based on detected signals
6. **Wait**: Sleeps for the configured interval before the next iteration

## 🛠️ Next Steps & Improvements

This bot is a solid foundation, but here are ideas for enhancement:

- ✅ **Add More Indicators**: Combine SMA with RSI, MACD, or other indicators
- ✅ **Implement Stop-Loss**: Automatically sell if price drops by X%
- ✅ **Trade Multiple Symbols**: Monitor and trade a portfolio of stocks
- ✅ **Better Logging**: Save bot actions to a file for analysis
- ✅ **Error Handling**: More robust handling of API errors and edge cases
- ✅ **Backtesting**: Test strategies on historical data before live trading

## ⚠️ Disclaimer

This bot is for **educational purposes only**. Trading involves risk, and past performance does not guarantee future results. Always:

- Test thoroughly in paper trading mode
- Understand the strategy before using real money
- Start with small position sizes
- Monitor the bot regularly
- Never risk more than you can afford to lose

## 📖 Tutorial Series

This is Tutorial 10 in a series covering:
- Tutorial 1-9: Individual components (API connection, data fetching, indicators, etc.)
- Tutorial 10: Complete bot assembly (this project)

## 📝 License

This project is for educational purposes as part of the Alpaca Trading Course.

## 🤝 Contributing

This is a tutorial project. Feel free to fork and experiment with your own improvements!

---

**Happy Trading! 📈**
