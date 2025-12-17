# Tutorial 13: Never Risk Too Much – Calculating Position Size

## 💰 Dynamic Position Sizing – The Foundation of Professional Trading

In this tutorial, you'll learn the **single most important rule of money management**: position sizing. You will learn how to dynamically calculate the number of shares to buy to ensure that you only risk a small, fixed percentage of your total capital on any single trade.

## 📚 What You'll Learn

- Why position sizing is the bedrock of risk management
- The mathematical formula that protects your capital
- How to calculate position size based on account equity
- How to implement dynamic position sizing in Python
- Why fixed quantity trading is dangerous
- How professional traders standardize risk across all trades

## 💡 Why Position Sizing is Essential

**The Problem**: Trading a fixed number of shares (e.g., always buying 10 shares) is fundamentally flawed. Risking 10 shares of a $20 stock is NOT the same as risking 10 shares of a $500 stock.

**The Solution**: Calculate position size dynamically so that you risk the same percentage of your capital on every trade, regardless of the stock price.

### Three Reasons Position Sizing Matters:

1. **Prevents Catastrophic Losses** - Makes it mathematically impossible for a single trade to destroy your account
2. **Ensures Consistency** - You risk 1% whether trading Apple or Tesla
3. **Enables Long-Term Survival** - Professional traders survive losing streaks through proper position sizing

## 🧮 The Position Sizing Formula

The calculation follows four simple steps:

### Step 1: Define Your Max Risk Per Trade
Decide on a small percentage of your total account equity you are willing to risk on one trade. Professionals typically use **1% or 2%**.

### Step 2: Calculate Your Risk Amount in Dollars
```
Risk Amount ($) = Total Equity × Risk Percentage
```

### Step 3: Determine Your Risk Per Share
This is the dollar amount you lose per share if your stop-loss is hit.
```
Risk Per Share ($) = Entry Price - Stop-Loss Price
```

### Step 4: Calculate the Number of Shares to Buy
```
Position Size = Risk Amount ($) ÷ Risk Per Share ($)
```

## 📊 Real Example

Let's see how this works in practice:

**Scenario:**
- Account Equity: $10,000
- Risk Percentage: 1%
- Entry Price: $50
- Stop-Loss: $48 (2% below entry)

**Calculation:**
1. Risk Amount = $10,000 × 0.01 = **$100**
2. Risk Per Share = $50 - $48 = **$2**
3. Position Size = $100 ÷ $2 = **50 shares**

**Result:**
If you buy 50 shares at $50 and the trade fails, you'll be stopped out at $48, losing exactly **$100** (50 shares × $2 loss/share), which is precisely 1% of your capital.

## 📋 Prerequisites

- Python 3.8 or higher
- Alpaca Paper Trading Account ([Sign up here](https://alpaca.markets/))
- Understanding of bracket orders (Tutorial 12 recommended)
- Basic knowledge of stop-loss orders

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
python dynamic_sizing_bot.py
```

## 📊 Trading Strategy

The bot implements professional-grade risk management:

- **Entry Signal**: Golden Cross (20-day SMA crosses above 50-day SMA)
- **Entry Type**: Market buy order
- **Position Sizing**: Dynamic calculation based on 1% risk
- **Take-Profit**: +3% above entry price (3:1 reward-to-risk ratio)
- **Stop-Loss**: -1% below entry price (risk control)

## 💰 Position Sizing Configuration

### The Core Calculation:

```python
RISK_PER_TRADE_PERCENTAGE = 1.0  # Risk only 1% of equity per trade
TAKE_PROFIT_PERCENTAGE = 3.0     # 3:1 reward-to-risk ratio
STOP_LOSS_PERCENTAGE = 1.0       # Stop-loss distance

# Calculate position size
risk_amount_dollars = total_equity * (RISK_PER_TRADE_PERCENTAGE / 100)
stop_loss_price = entry_price * (1 - STOP_LOSS_PERCENTAGE / 100)
risk_per_share = entry_price - stop_loss_price
qty_to_trade = int(risk_amount_dollars / risk_per_share)
```

### Example Output:

```
💼 Account Equity: $10,000.00
💰 Entry Price: $150.00
📏 Position Size Calculated: 67 shares
💵 Position Value: $10,050.00
🎯 Take-Profit: $154.50 (+3%)
🛡️  Stop-Loss: $148.50 (-1%)

--- Risk Analysis ---
💸 Risk Amount: $100.50 (1.01% of equity)
💰 Profit Potential: $301.50
📊 Risk/Reward: $100.50 to make $301.50
```

## ⚙️ Configuration

Edit these constants in `dynamic_sizing_bot.py`:

```python
SYMBOL_TO_TRADE = "AAPL"              # Stock symbol
RISK_PER_TRADE_PERCENTAGE = 1.0       # Risk per trade (1% recommended)
TAKE_PROFIT_PERCENTAGE = 3.0          # Profit target
STOP_LOSS_PERCENTAGE = 1.0            # Stop-loss distance
```

### Recommended Risk Levels:

- **Conservative**: 0.5% risk per trade
- **Balanced**: 1.0% risk per trade ← **Default (Recommended)**
- **Aggressive**: 2.0% risk per trade (maximum safe level)

⚠️ **Never risk more than 2% per trade!**

## 📖 Code Structure

The code follows educational best practices with clear, descriptive functions:

### Key Functions:

1. **`get_account_equity()`**
   - Fetches total account equity (cash + stocks)
   - Critical for position size calculation

2. **`calculate_position_size(total_equity, entry_price, risk_percentage, stop_loss_percentage)`**
   - **THIS IS THE CORE FUNCTION**
   - Implements the professional position sizing formula
   - Returns the exact number of shares to buy

3. **`calculate_take_profit_price(entry_price, profit_percentage)`**
   - Calculates your profit target
   - Ensures good risk/reward ratio

4. **`calculate_stop_loss_price(entry_price, loss_percentage)`**
   - Calculates your stop-loss price
   - Protects your capital

5. **`submit_bracket_order(symbol, quantity, tp_price, sl_price)`**
   - Submits the dynamically sized bracket order
   - Uses calculated position size (not fixed quantity)

6. **`run_dynamic_sizing_bot()`**
   - Main bot loop
   - Shows detailed position sizing calculations

### Educational Principles:
- **Full variable names**: `risk_amount_dollars`, not `r`
- **WHY comments**: Explains reasoning, not just actions
- **One action per line**: No complex nested logic
- **Extensive output**: Shows all calculations step-by-step

## 🔒 Risk Management Features

- ✅ **Dynamic Position Sizing** - Adapts to account size and stock price
- ✅ **Fixed Risk Percentage** - Always risk the same % of capital
- ✅ **Automatic Stop-Loss** - Limits losses to predetermined amount
- ✅ **Automatic Take-Profit** - Secures gains at target
- ✅ **Safety Checks** - Prevents trading if position size < 1 share
- ✅ **Account Protection** - Makes account blow-up mathematically impossible

## 💰 Comparison: Fixed vs Dynamic Position Sizing

### Fixed Quantity (Old Way - DANGEROUS):
```
Trade 1: Buy 10 shares of $50 stock = Risk $10 on 2% move
Trade 2: Buy 10 shares of $200 stock = Risk $40 on 2% move
```
**Problem**: Inconsistent risk! Second trade risks 4x more.

### Dynamic Sizing (Professional Way):
```
Trade 1: Buy 50 shares of $50 stock = Risk exactly $100 (1%)
Trade 2: Buy 12 shares of $200 stock = Risk exactly $100 (1%)
```
**Solution**: Consistent risk on every trade, regardless of price!

## 📈 Example Trade Walkthrough

**Account State:**
- Equity: $10,000
- Risk: 1% = $100

**Trade Setup:**
- Symbol: AAPL
- Entry: $180.00
- Stop-Loss: $178.20 (-1%)
- Take-Profit: $185.40 (+3%)

**Position Sizing:**
- Risk Per Share: $180.00 - $178.20 = $1.80
- Position Size: $100 ÷ $1.80 = **55 shares**

**Potential Outcomes:**
- ✅ **Win**: Price hits $185.40 → Profit = $297 (+2.97% of account)
- ❌ **Loss**: Price hits $178.20 → Loss = $99 (-0.99% of account)
- 📊 **Risk/Reward**: Risk $99 to make $297 (3:1 ratio)

## 🎓 Educational Philosophy

This project prioritizes **clarity over cleverness**:

- Every line is understandable for beginners
- No "magic" or hidden complexity
- Verbose, explicit code with detailed comments
- Step-by-step calculations shown in output
- Perfect for learning professional risk management

## ⚠️ Important Warnings

- **Paper Trading Only** - Uses fake money for learning
- **Not Financial Advice** - Educational purposes only
- **Test Thoroughly** - Understand the code before live trading
- **Markets Are Risky** - You can lose money in real trading
- **Never Risk More Than 2%** - Professional maximum per trade

## 🧪 Testing Position Sizing

Want to see how position sizing adapts? Try these experiments:

### Experiment 1: Different Stock Prices
```python
SYMBOL_TO_TRADE = "GOOGL"  # ~$140
# vs
SYMBOL_TO_TRADE = "AMZN"   # ~$180
```
Watch how the bot calculates different quantities but risks the same dollar amount!

### Experiment 2: Different Risk Levels
```python
RISK_PER_TRADE_PERCENTAGE = 0.5  # More conservative
# vs
RISK_PER_TRADE_PERCENTAGE = 2.0  # More aggressive
```
See how position size adjusts to maintain consistent risk.

### Experiment 3: Different Stop-Loss Distances
```python
STOP_LOSS_PERCENTAGE = 0.5  # Tighter stop = larger position
# vs
STOP_LOSS_PERCENTAGE = 2.0  # Wider stop = smaller position
```
Understand the inverse relationship between stop distance and position size.

## 📚 Related Tutorials

- **Tutorial 09**: Crossover Bot v1
- **Tutorial 10**: Crossover Bot Final
- **Tutorial 11**: Bracket Orders - Stop-Loss
- **Tutorial 12**: Take Your Profits - Take-Profit Orders
- **Tutorial 13**: Position Sizing ← **You are here**

## 📝 Files in This Tutorial

- `dynamic_sizing_bot.py` - Main bot with dynamic position sizing
- `config.example.py` - Configuration template
- `instructions.md` - Detailed tutorial instructions
- `requirements.txt` - Python dependencies
- `README.md` - This file
- `.gitignore` - Protects your API keys
- `HOW_TO_PUBLISH.md` - GitHub publishing guide

## 💡 Key Concepts Learned

1. **Position Sizing** - The foundation of risk management
2. **Fixed Risk Percentage** - Standardizing risk across trades
3. **Dynamic Calculation** - Adapting to stock price and account size
4. **Risk Per Share** - Understanding per-share loss potential
5. **Account Equity** - Using total portfolio value, not just cash
6. **Professional Trading** - How pros protect their capital

## 🔧 Troubleshooting

**Problem**: "Calculated position size is 0 shares"
- **Cause**: Account too small or stock too expensive
- **Solution**: The bot shows minimum equity needed. Either:
  - Increase paper trading account size
  - Trade a cheaper stock
  - Increase risk percentage (not recommended above 2%)

**Problem**: "Risk per share is zero or negative"
- **Cause**: Stop-loss percentage is 0 or negative
- **Solution**: Ensure `STOP_LOSS_PERCENTAGE > 0`

**Problem**: Bot can't connect to Alpaca API
- **Solution**: Check your API keys in `config.py`

**Problem**: Order gets rejected
- **Solution**: Ensure you're using paper trading and market is open

**Problem**: No Golden Cross signal
- **Solution**: Golden Cross is rare. Be patient or test with different symbols

## 📊 Understanding the Output

When a signal is detected, you'll see:

```
📈 Golden Cross Detected! Calculating dynamic position size...

============================================================
💼 Account Equity: $10,000.00
💰 Entry Price: $150.00
📏 Position Size Calculated: 67 shares
💵 Position Value: $10,050.00
🎯 Take-Profit: $154.50 (+3%)
🛡️  Stop-Loss: $148.50 (-1%)

--- Risk Analysis ---
💸 Risk Amount: $100.50 (1.01% of equity)
💰 Profit Potential: $301.50
📊 Risk/Reward: $100.50 to make $301.50
============================================================

✅ Dynamically sized bracket order submitted successfully!
ℹ️  This trade risks exactly 1.0% of your capital.
ℹ️  No matter what the stock price is, your risk is controlled.
```

**What this tells you:**
- Your total account value
- The price you're entering at
- The exact number of shares calculated
- How much capital you're deploying
- Your profit target and stop-loss
- **Your actual dollar risk (always ~1% of equity)**
- Your profit potential
- Your risk/reward ratio

## 🎯 Next Steps

After mastering position sizing:
1. Track your trades to verify risk is consistent
2. Experiment with different risk percentages (stay under 2%)
3. Test with different symbols and timeframes
4. Learn about portfolio heat (total risk across all positions)
5. Explore advanced techniques like volatility-based sizing

## 🏆 The Professional Difference

**Amateur Trader:**
- "I'll buy 10 shares"
- Inconsistent risk
- One bad trade can destroy account
- No mathematical foundation

**Professional Trader:**
- "I'll risk 1% of my capital"
- Consistent risk on every trade
- Account protected mathematically
- Can survive 100+ losing trades

**This tutorial teaches you to trade like a professional.**

## 📦 Publishing to GitHub

See `HOW_TO_PUBLISH.md` for detailed instructions on publishing this tutorial to GitHub.

Quick summary:
1. Create repository on GitHub
2. Run `git init` in this directory
3. Run `git add .` to stage files
4. Run `git commit -m "Tutorial 13: Dynamic Position Sizing"`
5. Push to GitHub with provided commands

## 📞 Support

Questions or issues? Open an issue in the repository!

---

**Remember**: Position sizing is what separates amateurs from professionals. Master this skill, and you'll have the foundation for long-term trading success. Never trade with money you can't afford to lose! 📈💰

**"It's not about how much you make. It's about how much you don't lose." - Warren Buffett**

