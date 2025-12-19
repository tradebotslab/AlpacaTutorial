# 📚 Alpaca Trading Tutorial 22: Stop Digging in the Code – Using an External Config File

## 🎯 What You'll Learn

In this tutorial, you'll discover one of the most important professional practices in software development: **separating configuration from code**. You'll learn how to:

- ✅ Move API keys and strategy parameters to an external JSON file
- ✅ Load and use configuration in your Python trading bot
- ✅ Make your bot more secure and flexible
- ✅ Change trading parameters without touching code
- ✅ Protect your API keys from accidental exposure

**Learning Outcome**: After this lesson, you'll never hardcode settings again!

---

## 🚨 The Problem with "Hardcoding" Settings

Until now, you've likely kept API keys and parameters directly in your Python code:

```python
# ❌ BAD: Hardcoded values scattered throughout the code
trading_client = TradingClient('PKxxxxx', 'yyyyyyy', paper=True)
symbol = "SPY"
quantity = 10
short_window = 40
long_window = 100
```

### Why This Is Problematic:

| Problem | Description |
|---------|-------------|
| **Lack of Flexibility** | Want to change the symbol? You dig through code. Adjust strategy parameters? More digging. |
| **Security Risk** | Accidentally share your code on GitHub? You've shared your API keys too! 💸 |
| **Management Difficulty** | As your bot grows, settings get scattered across multiple files. |
| **No Separation of Concerns** | Configuration mixed with logic makes code harder to maintain. |

---

## ✅ The Solution: External Configuration File

The professional approach is to separate configuration from application logic using a `config.json` file:

```json
{
  "api_key": "YOUR_API_KEY",
  "api_secret": "YOUR_API_SECRET",
  "paper_trading": true,
  "trade_symbol": "SPY",
  "trade_quantity": 10,
  "strategy_parameters": {
    "short_window": 40,
    "long_window": 100
  }
}
```

### Benefits:

- 🔒 **More Secure**: API keys separated from code
- 🔧 **More Flexible**: Change parameters without modifying logic
- 📁 **Better Organized**: All settings in one dedicated place
- 👥 **Team-Friendly**: Different team members can use different configs
- 🧪 **Easier Testing**: Switch between test/production configs easily

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.8 or higher installed
- ✅ An Alpaca account (paper trading is fine)
- ✅ Basic understanding of JSON format
- ✅ Completed earlier tutorials (or understanding of Alpaca API)

---

## 🚀 Installation

### Step 1: Clone or Download This Tutorial

```bash
cd Alpaca22
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `alpaca-py` - Alpaca's official Python SDK
- `pandas` - Data manipulation for historical analysis
- `requests` - HTTP library (dependency)

### Step 3: Create Your Configuration File

```bash
# Copy the example config to create your own
copy config.example.json config.json  # Windows
# or
cp config.example.json config.json    # Mac/Linux
```

### Step 4: Add Your API Keys

Open `config.json` in a text editor and fill in your details:

```json
{
  "api_key": "YOUR_ACTUAL_API_KEY",
  "api_secret": "YOUR_ACTUAL_SECRET_KEY",
  "paper_trading": true,
  "trade_symbol": "SPY",
  "trade_quantity": 10,
  "strategy_parameters": {
    "short_window": 40,
    "long_window": 100
  },
  "check_interval_seconds": 300
}
```

**Where to get API keys:**
1. Log in to [Alpaca](https://alpaca.markets/)
2. Go to "Paper Trading" section
3. Click "Generate API Keys"
4. Copy both the API Key and Secret Key

---

## 🏃‍♂️ Running the Bot

### Basic Execution

```bash
python config_bot.py
```

### What You'll See

```
📂 Loading configuration from config.json...
✅ Configuration loaded successfully!

======================================================================
🚀 Configuration-Based Trading Bot Starting...
======================================================================
📊 Trading Symbol: SPY
📏 Quantity per Trade: 10 shares
📈 Strategy: Golden Cross (40/100 SMA)
⏱️  Check Interval: 300 seconds
🔧 Paper Trading: True
======================================================================

💡 To change these settings, simply edit config.json!
   No need to dig through the code!
```

---

## 🎮 How It Works

### The Configuration Loading Process

```python
# 1. Import JSON library (built into Python)
import json

# 2. Load configuration file
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    print("✅ Configuration loaded successfully!")
except FileNotFoundError:
    print("❌ Error: config.json not found.")
    exit()

# 3. Extract values into variables
API_KEY = config['api_key']
SYMBOL = config['trade_symbol']
QUANTITY = config['trade_quantity']
SHORT_WINDOW = config['strategy_parameters']['short_window']
```

### The Trading Strategy

The bot implements a **Golden Cross strategy**:

1. **Calculate Moving Averages**: Short-term (40-day) and Long-term (100-day) SMAs
2. **Detect Crossover**: When short SMA crosses above long SMA
3. **Execute Trade**: Buy the configured quantity of shares
4. **Monitor Position**: Track profit/loss in real-time

**The Key Insight**: All parameters (symbol, quantity, windows) come from `config.json`!

---

## 🔧 Customization Guide

### Change the Trading Symbol

Edit `config.json`:

```json
{
  "trade_symbol": "AAPL",  // Changed from SPY to AAPL
  ...
}
```

No code changes needed! Just restart the bot.

### Adjust Strategy Parameters

Make the strategy more sensitive (faster signals):

```json
{
  "strategy_parameters": {
    "short_window": 20,   // More responsive
    "long_window": 50     // Faster crossovers
  }
}
```

Or more conservative (slower signals):

```json
{
  "strategy_parameters": {
    "short_window": 50,
    "long_window": 200
  }
}
```

### Change Check Interval

Check more frequently (every minute):

```json
{
  "check_interval_seconds": 60
}
```

Or less frequently (every 30 minutes):

```json
{
  "check_interval_seconds": 1800
}
```

### Switch to Live Trading

**⚠️ WARNING**: Only do this when you're ready!

```json
{
  "paper_trading": false,  // ⚠️ This uses REAL MONEY!
  ...
}
```

---

## 📊 Code Structure

```
Alpaca22/
├── config_bot.py              # Main bot script
├── config.example.json        # Template configuration (safe to share)
├── config.json               # Your actual config (NEVER commit!)
├── requirements.txt          # Python dependencies
├── .gitignore               # Protects config.json
├── instructions.md          # Detailed lesson content
└── README.md               # This file
```

---

## 🔒 Security Best Practices

### Rule #1: NEVER Commit config.json

Your `.gitignore` file already protects you:

```gitignore
# API Keys and Secrets - NEVER commit these files!
config.json
```

### Rule #2: Use config.example.json for Sharing

When sharing your code:
- ✅ Include `config.example.json` with placeholder values
- ❌ Never include `config.json` with real keys

### Rule #3: Use Paper Trading by Default

Always set `"paper_trading": true` in your example configs.

### Rule #4: Rotate Keys if Exposed

If you accidentally commit your keys:
1. Go to Alpaca dashboard immediately
2. Delete the exposed keys
3. Generate new ones
4. Update your `config.json`

---

## 🐛 Troubleshooting

### Problem: "config.json not found"

**Solution**: Create the file from the template:

```bash
copy config.example.json config.json  # Windows
cp config.example.json config.json    # Mac/Linux
```

Then edit `config.json` with your API keys.

### Problem: "Invalid JSON format"

**Solution**: Validate your JSON using:
- [JSONLint.com](https://jsonlint.com/)
- VS Code's built-in JSON validator

Common issues:
- Missing comma between fields
- Trailing comma after last field
- Unquoted strings
- Using single quotes instead of double quotes

### Problem: "API authentication error"

**Solution**: Check your keys in `config.json`:
1. Make sure there are no extra spaces
2. Verify you're using paper trading keys (if `paper_trading: true`)
3. Check that keys haven't expired in Alpaca dashboard

### Problem: "Not enough historical data"

**Solution**: Choose a more liquid symbol like `SPY`, `AAPL`, or `MSFT` that has plenty of trading history.

---

## 📈 Example Output

```
--- Loop running at 2024-01-15 14:30:00 ---
ℹ️  No position held. Analyzing for entry signal...
📊 Current Price: $450.25
📈 SMA 40: $448.75
📉 SMA 100: $445.20

======================================================================
🎯 GOLDEN CROSS DETECTED!
======================================================================
📊 Short SMA (40) crossed above Long SMA (100)
💰 Buying 10 shares of SPY
✅ Order submitted successfully!
   Order ID: 61e5e6e5-5e5c-4f5e-9e5e-5e5e5e5e5e5e
   Symbol: SPY
   Quantity: 10
   Side: BUY
✅ Position opened successfully!

💡 Want to change the strategy parameters?
   Just edit config.json - no code changes needed!
```

---

## 🎓 Key Takeaways

### What You Learned

1. **Separation of Concerns**: Configuration should be separate from code
2. **JSON Format**: How to structure and use JSON configuration files
3. **Security**: How to protect API keys from accidental exposure
4. **Flexibility**: How easy it is to modify behavior without code changes
5. **Professional Practice**: Industry-standard approach to configuration management

### Before This Tutorial

```python
# Scattered hardcoded values
api_key = "PKxxx..."
symbol = "SPY"
quantity = 10
```

### After This Tutorial

```python
# Clean, configurable code
API_KEY = config['api_key']
SYMBOL = config['trade_symbol']
QUANTITY = config['trade_quantity']
```

**The Result**: More secure, flexible, and maintainable code!

---

## 🔄 Next Steps

Now that you've mastered external configuration:

1. **Try Different Symbols**: Edit `config.json` to trade different stocks
2. **Experiment with Parameters**: Adjust moving average windows
3. **Add More Settings**: Extend the config with your own parameters
4. **Multiple Configs**: Create `config.production.json`, `config.test.json`
5. **Environment Variables**: Learn about using OS environment variables for even better security

### Advanced Configuration Ideas

- Add risk management parameters (max loss per trade)
- Include multiple symbols for portfolio trading
- Add email/notification settings
- Include backtesting parameters
- Add logging configuration

---

## 📚 Additional Resources

- [JSON Format Documentation](https://www.json.org/)
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Python JSON Module](https://docs.python.org/3/library/json.html)
- [12-Factor App Methodology](https://12factor.net/config) - Industry best practices

---

## ⚠️ Important Disclaimers

- **Paper Trading**: This tutorial uses paper trading by default. No real money is at risk.
- **Educational Purpose**: This bot is for learning. Not financial advice.
- **No Guarantees**: Past performance doesn't guarantee future results.
- **Risk Warning**: Trading involves risk. Only trade with money you can afford to lose.

---

## 💡 Pro Tips

### Tip #1: Use Multiple Config Files

Create different configs for different scenarios:

```
config.development.json  # Your testing config
config.production.json   # Live trading config (if ever needed)
config.aggressive.json   # More frequent trades
config.conservative.json # Less frequent trades
```

Then load the appropriate one:

```python
import sys
config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
with open(config_file, 'r') as f:
    config = json.load(f)
```

Run with: `python config_bot.py config.aggressive.json`

### Tip #2: Add Configuration Validation

```python
required_fields = ['api_key', 'api_secret', 'trade_symbol']
for field in required_fields:
    if field not in config:
        print(f"❌ Missing required field: {field}")
        exit()
```

### Tip #3: Use Environment Variables for Production

For production systems, consider using environment variables:

```python
import os
API_KEY = os.getenv('ALPACA_API_KEY') or config.get('api_key')
```

This provides an extra layer of security.

---

## 🎉 Congratulations!

You've just implemented one of the most important professional practices in software development. Your trading bot is now:

- 🔒 **More Secure**: Keys separated from code
- 🔧 **More Flexible**: Easy to modify without code changes
- 📁 **Better Organized**: Clear separation of concerns
- 👨‍💼 **More Professional**: Following industry best practices

**"Risk comes from not knowing what you're doing." - Warren Buffett**

And now you know how to manage configuration like a professional developer! 🚀

---

## 📞 Questions or Issues?

If you encounter any problems or have questions:

1. Check the Troubleshooting section above
2. Review the `instructions.md` file for detailed explanations
3. Consult the [Alpaca Community Forum](https://forum.alpaca.markets/)
4. Review the code comments - they explain the "why" behind each decision

---

**Happy Trading! 📈**

*Remember: Always test with paper trading first. This is educational content, not financial advice.*

