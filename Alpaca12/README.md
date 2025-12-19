# Tutorial 12: Take Your Profits! – Setting a Take-Profit Order

## 🎯 Take Your Profits – The Offensive Exit Strategy

In this tutorial, you'll learn how to **secure your gains** by setting automatic take-profit orders. While stop-losses protect you from losses, take-profit orders ensure you don't let winning trades turn into losers.

## 📚 What You'll Learn

- Why setting a profit target is crucial for disciplined trading
- How to calculate take-profit prices based on percentage goals
- How to implement take-profit orders in bracket orders
- The importance of risk/reward ratios
- How to automate the complete trade lifecycle

## 💡 Why Take-Profit Matters

**The Problem**: Markets are volatile. A stock that hits your profit goal can quickly reverse, turning a winning trade into a losing one.

**The Solution**: Set a take-profit order that automatically sells when your target is reached.

### Three Parts of a Complete Strategy:
1. **Entry Signal** - When to buy (Golden Cross)
2. **Defensive Exit** - Protect from losses (Stop-Loss)
3. **Offensive Exit** - Lock in gains (Take-Profit) ← **You are here**

## 🛡️ What is a Take-Profit Order?

A take-profit is a **limit order** that automatically sells your shares when the price reaches your target:

- **Entry Price**: $100
- **Take-Profit**: 5% gain = $105
- **Result**: Automatically sells at $105 or better

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Basic understanding of bracket orders
- Completion of Tutorial 11 (recommended)

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

The bot implements a complete risk-managed strategy:

- **Entry Signal**: Golden Cross (20-day SMA crosses above 50-day SMA)
- **Entry Type**: Market buy order
- **Take-Profit**: +5% above entry price (your profit goal)
- **Stop-Loss**: -2% below entry price (your safety net)
- **Risk/Reward Ratio**: 2.5:1 (risk $2 to make $5)

## 🎯 Take-Profit Configuration

### The Core Calculation:

```python
TAKE_PROFIT_PERCENTAGE = 5.0  # Your profit goal

# Calculate target price
take_profit_price = entry_price * (1 + TAKE_PROFIT_PERCENTAGE / 100)

# For example: $100 * 1.05 = $105
```

### Submitting the Order:

```python
api.submit_order(
    symbol="AAPL",
    qty=1,
    side='buy',
    type='market',
    time_in_force='day',
    order_class='bracket',
    take_profit={'limit_price': take_profit_price},  # ← Profit target
    stop_loss={'stop_price': stop_loss_price}
)
```

## ⚙️ Configuration

Edit these constants in `bracket_bot.py`:

```python
SYMBOL_TO_TRADE = "AAPL"           # Stock symbol
QTY_PER_TRADE = 1                   # Number of shares
TAKE_PROFIT_PERCENTAGE = 5.0        # Profit target (adjustable)
STOP_LOSS_PERCENTAGE = 2.0          # Maximum loss (adjustable)
```

### Recommended Risk/Reward Ratios:
- **Conservative**: 2:1 (risk 2% to make 4%)
- **Balanced**: 2.5:1 (risk 2% to make 5%) ← **Default**
- **Aggressive**: 3:1 (risk 2% to make 6%)

## 📖 Code Structure

The code follows educational best practices with clear, descriptive functions:

### Key Functions:

1. **`calculate_take_profit_price(entry_price, profit_percentage)`**
   - Converts your percentage goal into a dollar amount
   - Returns the precise target price

2. **`calculate_stop_loss_price(entry_price, loss_percentage)`**
   - Calculates your maximum acceptable loss
   - Returns the stop price

3. **`submit_bracket_order(symbol, quantity, tp_price, sl_price)`**
   - Submits the complete bracket order
   - Broker automatically manages both exits

4. **`run_bracket_bot()`**
   - Main bot loop
   - Shows detailed profit/loss calculations

### Educational Principles:
- **Full variable names**: `take_profit_price`, not `tp`
- **WHY comments**: Explains reasoning, not just actions
- **One action per line**: No complex nested logic
- **Extensive output**: Shows all calculations

## 🔒 Risk Management Features

- **Automatic Profit Taking**: Never miss your target
- **No Greed**: Removes temptation to "hold for more"
- **Disciplined Exits**: Emotion-free trading
- **Risk/Reward Display**: Shows potential profit vs. loss
- **Position Monitoring**: Tracks active trades

## 💰 Example Trade Walkthrough

```
Entry: $100.00 (Golden Cross signal)
Take-Profit: $105.00 (+5%)
Stop-Loss: $98.00 (-2%)

Potential Profit: $5.00
Potential Loss: $2.00
Risk/Reward: 1:2.5
```

**Outcome 1**: Price rises to $105 → Sell automatically → **+$5 profit** ✅
**Outcome 2**: Price falls to $98 → Sell automatically → **-$2 loss** 🛡️

## 🎓 Educational Philosophy

This project prioritizes **clarity over cleverness**:

- Every line is understandable for beginners
- No "magic" or hidden complexity
- Verbose, explicit code
- Perfect for learning algorithmic trading

## ⚠️ Important Warnings

- **Paper Trading Only** - Uses fake money for learning
- **Not Financial Advice** - Educational purposes only
- **Test Thoroughly** - Understand the code before live trading
- **Markets Are Risky** - You can lose money in real trading

## 📚 Related Tutorials

- **Tutorial 09**: Crossover Bot v1
- **Tutorial 10**: Crossover Bot Final
- **Tutorial 11**: Bracket Orders - Stop-Loss
- **Tutorial 12**: Take Your Profits! ← **You are here**

## 📝 Files in This Tutorial

- `bracket_bot.py` - Main bot with take-profit implementation
- `config.example.py` - Configuration template
- `instructions.md` - Detailed tutorial instructions
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `.gitignore` - Protects your API keys

## 💡 Key Concepts Learned

1. **Take-Profit Orders** - Automatic profit-taking
2. **Limit Orders** - Sell at your price or better
3. **Risk/Reward Ratios** - Balancing profit potential vs. risk
4. **Complete Strategy** - Entry + defensive exit + offensive exit
5. **Discipline Over Greed** - Automated decision-making

## 🔧 Troubleshooting

**Problem**: Bot can't connect to Alpaca API
- **Solution**: Check your API keys in `config.py`

**Problem**: Order gets rejected
- **Solution**: Ensure you're using paper trading and market is open

**Problem**: No Golden Cross signal
- **Solution**: Golden Cross is rare. Be patient or test with different symbols

**Problem**: Take-profit never triggers
- **Solution**: Your target might be too ambitious. Consider lowering the percentage

## 📊 Understanding the Output

```
🎯 Take-Profit Target: $105.00 (+5%)
🛡️  Stop-Loss Target: $98.00 (-2%)
💵 Potential Profit: $5.00
💵 Potential Loss: $2.00
```

This tells you:
- Where your order will sell for profit
- Where your order will sell for protection
- How much you could gain
- How much you could lose

## 🎯 Next Steps

After mastering take-profit orders:
1. Experiment with different risk/reward ratios
2. Test with different symbols and timeframes
3. Combine with other technical indicators
4. Learn about trailing stops (Tutorial 13+)

## 📦 Publishing to GitHub

To publish this tutorial to your own GitHub:

1. **Create a new repository** on GitHub:
   - Go to https://github.com/new
   - Repository name: `AlpacaTutorial-12-TakeProfit` (or your preferred name)
   - Choose Public/Private
   - **DO NOT** initialize with README
   - Click "Create repository"

2. **Push your code**:
   ```bash
   cd Alpaca12
   git init
   git add .
   git commit -m "Tutorial 12: Take Your Profits - Setting a Take-Profit Order"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

3. **What will be published**:
   - ✅ bracket_bot.py
   - ✅ README.md
   - ✅ requirements.txt
   - ✅ instructions.md
   - ✅ config.example.py
   - ✅ .gitignore

4. **What will NOT be published** (protected by .gitignore):
   - ❌ config.py (contains your API keys)
   - ❌ .cursorrules (IDE configuration)
   - ❌ __pycache__/ (Python cache)

## 📞 Support

Questions or issues? Open an issue in the repository!

---

**Remember**: The best traders protect their capital AND secure their profits. Never trade with money you can't afford to lose! 📈💰

