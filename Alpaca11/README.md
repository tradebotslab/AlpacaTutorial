# Tutorial 11: Bracket Orders - Stop-Loss & Take-Profit

## 📚 The Safety Net – How to Set a Simple Stop-Loss

In this tutorial, you will learn one of the most critical aspects of risk management: how to automatically protect your trades using **bracket orders**.

## 🎯 What You'll Learn

- How to set automatic **stop-loss** orders to limit potential losses
- How to set automatic **take-profit** orders to lock in gains
- How to use **bracket orders** to manage risk without manual intervention
- How to implement the "Golden Cross" strategy with automated exits

## 🛡️ What is a Bracket Order?

A bracket order combines three orders into one:
1. **Entry Order**: Your initial buy order
2. **Take-Profit**: Automatically sells at +5% profit
3. **Stop-Loss**: Automatically sells at -2% loss

When one exit order triggers, the other is automatically canceled (One-Cancels-Other).

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Basic understanding of moving averages
- Completion of Tutorials 1-10 (recommended)

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your API keys

Copy the example config file:

```bash
copy config.example.py config.py
```

Then edit `config.py` and add your Alpaca Paper Trading API keys:

```python
API_KEY = "YOUR_PAPER_TRADING_API_KEY"
SECRET_KEY = "YOUR_PAPER_TRADING_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"
```

⚠️ **Never commit your `config.py` file!** It's already in `.gitignore`.

### 3. Run the bot

```bash
python bracket_bot.py
```

## 📊 Trading Strategy

The bot uses a **Golden Cross** strategy:
- **Signal**: 20-day SMA crosses above 50-day SMA
- **Entry**: Market buy order
- **Take-Profit**: +5% above entry price
- **Stop-Loss**: -2% below entry price

## 🔒 Risk Management Features

- **Default Stop-Loss**: 2% (you risk only 2% per trade)
- **Default Take-Profit**: 5% (2.5:1 reward-to-risk ratio)
- **Position Size**: 1 share (adjustable in code)
- **Symbol**: AAPL (adjustable in code)

## ⚙️ Configuration

Edit these constants in `bracket_bot.py`:

```python
SYMBOL_TO_TRADE = "AAPL"           # Change to any stock
QTY_PER_TRADE = 1                   # Number of shares
TAKE_PROFIT_PERCENTAGE = 5.0        # Profit target
STOP_LOSS_PERCENTAGE = 2.0          # Maximum loss
```

## 📖 Code Structure

The code follows educational best practices:

### Main Functions:

1. **`check_position_exists(symbol)`** - Check if we have an open position
2. **`get_historical_bars(symbol, limit)`** - Fetch historical price data
3. **`calculate_moving_averages(dataframe)`** - Calculate SMAs
4. **`detect_golden_cross(dataframe)`** - Identify entry signal
5. **`get_current_price(symbol)`** - Get latest market price
6. **`calculate_exit_prices(...)`** - Calculate stop-loss and take-profit levels
7. **`submit_bracket_order(...)`** - Submit the complete bracket order
8. **`run_bracket_bot()`** - Main bot loop

### Key Principles:
- **Clear variable names**: `take_profit_price`, not `tp`
- **Single responsibility**: Each function does one thing
- **Extensive comments**: Explains WHY, not just WHAT
- **Error handling**: All API calls wrapped in try/except

## 🎓 Educational Philosophy

This project prioritizes **clarity over cleverness**:
- One line = one action
- No "magic" code
- Verbose, explicit logic
- Perfect for beginners

## ⚠️ Important Warnings

- **This is for PAPER TRADING only** - Uses fake money
- **Not financial advice** - Educational purposes only
- **Test thoroughly** before considering live trading
- **Markets are risky** - You can lose money

## 📚 Related Tutorials

- **Tutorial 02**: Hello Alpaca - First API Connection
- **Tutorial 04**: Placing Your First Order
- **Tutorial 05**: Checking Order Status
- **Tutorial 06**: Main Loop Bot
- **Tutorial 07**: Calculate SMA
- **Tutorial 08**: Crossover Detector
- **Tutorial 09**: Crossover Bot v1
- **Tutorial 10**: Crossover Bot Final
- **Tutorial 11**: Bracket Orders ← You are here

## 📝 Files in This Tutorial

- `bracket_bot.py` - Main bot with bracket order implementation
- `config.example.py` - Example configuration template
- `instructions.md` - Detailed tutorial instructions
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 💡 Key Concepts Learned

1. **Bracket Orders** - Combining entry, stop-loss, and take-profit in one order
2. **Risk Management** - Protecting capital with automatic stop-loss
3. **Profit Taking** - Automatically locking in gains
4. **OCO Orders** - One-Cancels-Other order types
5. **Set and Forget** - Letting the broker manage exits

## 🔧 Troubleshooting

**Problem**: Bot can't connect to Alpaca API
- **Solution**: Check your API keys in `config.py`

**Problem**: Order gets rejected
- **Solution**: Make sure you're using paper trading account and market is open

**Problem**: No Golden Cross signal
- **Solution**: This is normal! Golden Cross is rare. Be patient or test with different symbols

## 📞 Support

Questions or issues? Open an issue in the main repository!

---

**Remember**: Never trade with money you can't afford to lose. Always test in paper trading first! 📈

