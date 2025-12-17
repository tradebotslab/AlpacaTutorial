# 📈 Tutorial 14: Trailing Stop-Loss Bot

## 🎯 Objective
Learn how to protect your profits using a **trailing stop-loss** - one of the most powerful tools in algorithmic trading. This bot automatically locks in gains as your trade moves in your favor while giving winners room to run.

## 🧠 What You'll Learn
- The limitation of fixed stop-losses
- How trailing stops work and why they're superior
- Implementing trailing stops with Alpaca API
- Monitoring positions with dynamic risk management
- Real-time position tracking

## 📚 Concept: What is a Trailing Stop-Loss?

### The Problem with Fixed Stop-Losses
A fixed stop-loss protects you from losses but has a critical flaw:

**Example:**
- You buy at $100, set stop-loss at $98
- Stock rises to $150 (you have $50 paper profit!)
- Stock drops back to $99
- Your stop triggers at $98 → You lose $2 despite the stock reaching $150

**You watched your entire $50 profit disappear!**

### The Solution: Trailing Stop-Loss
A **trailing stop** automatically moves up as the price increases, but never moves down.

**Example with 10% trailing stop:**
1. **Entry:** Buy at $100 → Stop at $90
2. **Price rises to $110:** Stop moves to $99 (10% below $110)
3. **Price rises to $140:** Stop moves to $126 (10% below $140)
4. **Price dips to $135:** Stop STAYS at $126 (doesn't move down)
5. **Price falls to $126:** Position closes with $26 profit

### Benefits
✅ **Protects Unrealized Profits** - Converts paper gains into locked-in profits  
✅ **Lets Winners Run** - Stays in trades during uptrends  
✅ **Emotion-Free** - Automated, systematic exit strategy  
✅ **Adapts to Volatility** - Adjusts to market movement

## 🛠️ How This Bot Works

### Trading Logic
1. **Check Account Status** - Verify available capital
2. **Check Existing Positions** - Avoid duplicate orders
3. **Place Order** - Buy with automatic trailing stop
4. **Monitor Position** - Track price, P/L, and stop level
5. **Auto Exit** - Alpaca automatically closes when stop triggers

### Key Features
- **Automatic Stop Adjustment** - Alpaca manages the trailing stop
- **Real-Time Monitoring** - Display current price, P/L, and stop level
- **Position Sizing** - Uses 90% of available cash safely
- **GTC Orders** - "Good 'Til Canceled" keeps stop active
- **OTO Order Class** - "One-Triggers-Other" activates stop after buy fills

## 📋 Prerequisites
- Alpaca paper trading account ([sign up free](https://alpaca.markets))
- Python 3.7 or higher
- API keys from Alpaca

## 🚀 Installation

### Step 1: Clone or Download
```bash
cd AlpacaTutorial/Alpaca14
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys
1. Copy the example config:
```bash
cp config.example.py config.py
```

2. Edit `config.py` and add your Alpaca API keys:
```python
API_KEY = "your_api_key_here"
SECRET_KEY = "your_secret_key_here"
BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading
```

⚠️ **NEVER commit `config.py` to Git!** (It's in `.gitignore`)

## ▶️ Usage

### Run the Bot
```bash
python trailing_stop_bot.py
```

### What Happens
1. Bot connects to Alpaca
2. Displays account information
3. Checks for existing position in SPY
4. If no position:
   - Calculates affordable shares
   - Places buy order with 5% trailing stop
   - Enters monitoring mode
5. If position exists:
   - Displays current status
   - Monitors P/L and stop level
   - Updates every 60 seconds

### Example Output
```
==================================================
🚀 Trailing Stop-Loss Bot Starting...
==================================================

=== Account Information ===
Account Status: ACTIVE
Buying Power: $100000.00
Cash: $100000.00
Portfolio Value: $100000.00

📊 No existing position in SPY
Current Price: $450.25

💡 Planning to buy 200 shares at ~$450.25
With 5.0% trailing stop-loss
Initial Stop Price: $427.74
(This will automatically move up as price increases)

📤 Placing order...

✅ Order placed successfully!
Order ID: abc123...
Symbol: SPY
Quantity: 200
Side: buy
Type: market
Trailing Stop: 5.0%

=== Position Status for SPY ===
Quantity: 200 shares
Entry Price: $450.30
Current Price: $452.10
Current Value: $90420.00
Unrealized P/L: $360.00 (0.40%)
Approximate Trailing Stop: $429.50
(Actual stop is managed automatically by Alpaca)

⏳ Waiting 60 seconds before next check...
```

## 🎛️ Configuration

### Adjustable Parameters (in `trailing_stop_bot.py`)
```python
SYMBOL = "SPY"                      # Stock to trade
TRAIL_PERCENT = 5.0                 # Trailing stop percentage
CHECK_INTERVAL_SECONDS = 60         # Monitoring frequency
```

### Recommended Trail Percentages
- **Volatile stocks (TSLA, NVDA):** 8-10%
- **Blue chips (SPY, AAPL):** 5-7%
- **Conservative trades:** 3-5%

## 📊 Understanding the Output

### Account Information
- **Buying Power:** Maximum you can spend (includes margin if enabled)
- **Cash:** Actual cash available
- **Portfolio Value:** Total account value

### Position Status
- **Entry Price:** Average price you bought at
- **Current Price:** Real-time market price
- **Unrealized P/L:** Profit/Loss (only realized when you sell)
- **Trailing Stop:** Approximate level (actual is managed by Alpaca)

## 🔒 Risk Management

### Built-in Safety Features
1. **Position Size Limit** - Uses only 90% of cash
2. **Automatic Stop-Loss** - Can't forget to set it
3. **Paper Trading Default** - Practice without risk
4. **Error Handling** - Try/except blocks on all API calls

### Best Practices
✅ **Start with paper trading** - Test thoroughly before real money  
✅ **Monitor regularly** - Check bot performance daily  
✅ **Adjust trail %** - Tighter for volatile stocks, wider for trends  
✅ **Review exits** - Learn from stopped-out trades  
❌ **Don't over-trade** - One position at a time for learning

## 🧪 Testing the Bot

### Paper Trading Test Plan
1. **Day 1:** Run bot, verify order placement
2. **Day 2-7:** Monitor position daily
3. **Check scenarios:**
   - Price rises → Stop should move up
   - Price dips slightly → Stop should stay fixed
   - Stop triggers → Position closes automatically

### Verification Checklist
- [ ] Order places successfully
- [ ] Trailing stop shows in Alpaca dashboard
- [ ] Stop level moves up as price increases
- [ ] Stop doesn't move down when price dips
- [ ] Position closes when stop triggers

## 📖 Code Structure

### Main Components
```python
# 1. Imports - External libraries
# 2. Constants - Configuration values
# 3. API Connection - Connect to Alpaca
# 4. Helper Functions:
    - get_account_info()           # Fetch account details
    - get_current_price()          # Get latest price
    - check_existing_position()    # Check for open positions
    - place_order_with_trailing_stop()  # Submit order
    - monitor_position()           # Track open position
# 5. Main Logic - Orchestrates everything
# 6. Run - Entry point
```

### Key Function: `place_order_with_trailing_stop()`
```python
order = api.submit_order(
    symbol=symbol,
    qty=qty,
    side='buy',
    type='market',
    time_in_force='gtc',      # Order stays active
    order_class='oto',        # Stop activates after buy
    stop_loss=dict(
        trail_percent=trail_percent  # Magic happens here!
    )
)
```

## 🐛 Troubleshooting

### "Insufficient buying power"
**Solution:** Reduce `TRAIL_PERCENT` or choose cheaper stock

### "Order rejected"
**Possible causes:**
- Market is closed (check trading hours)
- Invalid API keys
- Stock is not tradable on Alpaca

### Position not appearing
**Solution:** Wait 5-10 seconds after order submission for fill

### Stop triggered immediately
**Solution:** Price may be too volatile - increase `TRAIL_PERCENT`

## 📈 Next Steps

### Extend This Bot
1. **Add take-profit level** - Exit at target price
2. **Multiple positions** - Trade several stocks
3. **Email notifications** - Alert when stop triggers
4. **Backtesting** - Test on historical data
5. **Dynamic trail %** - Adjust based on volatility

### Continue Learning
- **Tutorial 15:** Multiple timeframe analysis
- **Tutorial 16:** Portfolio rebalancing
- **Tutorial 17:** Options trading basics

## 📚 Educational Resources

### Understanding Trailing Stops
- [Alpaca API Docs: Orders](https://alpaca.markets/docs/trading/orders/)
- [Trailing Stop Strategy Guide](https://www.investopedia.com/terms/t/trailingstop.asp)

### Risk Management
- Position sizing calculators
- Volatility-based stop placement
- Win rate vs. reward/risk ratio

## ⚠️ Important Disclaimers

**This is Educational Software**
- For learning purposes only
- Not financial advice
- Past performance ≠ future results

**Paper Trading First**
- Always test thoroughly with paper trading
- Understand every line of code before live trading
- Start small when going live

**Risk Warning**
- Trading involves risk of loss
- Only trade with money you can afford to lose
- Trailing stops don't guarantee profits

## 🤝 Contributing
Found a bug? Have an improvement? Open an issue or pull request!

## 📄 License
MIT License - Free to use and modify

## 🙏 Acknowledgments
Built with [Alpaca Markets API](https://alpaca.markets)  
Part of the Alpaca Trading Course series

---

**"Risk comes from not knowing what you're doing." - Warren Buffett**

Start with paper trading, understand the code, and trade responsibly! 🚀

