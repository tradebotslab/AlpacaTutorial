# Alpaca Trading Tutorial 11: Bracket Orders

## 📚 Tutorial: The Safety Net – How to Set a Simple Stop-Loss

This is Tutorial 11 from the Alpaca Trading Course series. In this tutorial, you will learn one of the most critical aspects of risk management: how to automatically protect your trades using **bracket orders**.

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

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/TomaszCieslar/AlpacaTutorial.git
cd AlpacaTutorial
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API keys

Create a `config.py` file in the project directory:

```python
API_KEY = "YOUR_PAPER_TRADING_API_KEY"
SECRET_KEY = "YOUR_PAPER_TRADING_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"
```

⚠️ **Never commit your `config.py` file!** It's already in `.gitignore`.

### 4. Run the bot

```bash
python bracket_bot.py
```

## 📊 Trading Strategy

The bot uses a **Golden Cross** strategy:
- **Signal**: 20-day SMA crosses above 50-day SMA
- **Entry**: Market buy order
- **Take-Profit**: +5% above entry price
- **Stop-Loss**: -2% below entry price

## 🔒 Risk Management

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

This is part of a series. Check out other tutorials:
- Tutorial 1-10: [Previous concepts]
- Tutorial 12: [Coming next]

## 🤝 Contributing

This is an educational project. Feel free to:
- Report issues
- Suggest improvements
- Share your learning experience

## 📄 License

MIT License - Free to use for educational purposes

## 📞 Support

Questions? Open an issue on GitHub!

---

**Remember**: Never trade with money you can't afford to lose. Always test in paper trading first! 📈

