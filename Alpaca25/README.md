# 📚 Alpaca Trading Course - Lesson 25

## 🛡️ Making Your Bot Resilient – Handling API and Connection Errors

### 🎯 What You Will Learn

In this lesson, you will transform your trading bot from a fragile script that crashes at the first sign of trouble into a **resilient, production-ready system** that can gracefully handle:

- ✅ Temporary API failures
- ✅ Network connection issues
- ✅ Invalid or corrupted data
- ✅ File operation errors
- ✅ Market closed errors
- ✅ Rate limiting and timeouts

By the end of this lesson, your bot will be **virtually uncrashable** – it will log errors, send notifications, and continue running even when things go wrong.

---

## 📖 Why Error Handling is Critical

### The Problem: A Brittle Bot

Without error handling, your bot is like a house of cards:

```python
# ❌ BRITTLE CODE - One error and the bot crashes
latest_trade = trading_client.get_latest_trade("SPY")
price = latest_trade.p

# If the network drops for just 1 second, the bot crashes.
# You're now offline and have no idea if you're in a position or not.
```

### The Solution: Resilience Through Error Handling

With proper error handling, your bot survives temporary failures:

```python
# ✅ RESILIENT CODE - Bot continues running even if API fails
try:
    latest_trade = trading_client.get_latest_trade("SPY")
    price = latest_trade.p
    print(f"Current price: ${price}")
except Exception as error:
    print(f"Could not fetch price: {error}")
    logging.error(f"API error: {error}")
    send_discord_notification(f"⚠️ API error: {error}")
    # Bot continues running and will try again on next cycle
```

---

## 🛡️ Key Failure Points in a Trading Bot

Every interaction with the outside world can fail. You must protect:

### 1. API Calls to Alpaca
```python
# These can fail due to network issues, API downtime, or rate limiting
- get_account()
- submit_order()
- get_open_position()
- get_latest_trade()
- get_stock_bars()
- close_position()
```

### 2. Network Requests
```python
# Discord webhook calls can timeout or fail
requests.post(DISCORD_WEBHOOK_URL, ...)
```

### 3. File Operations
```python
# Files can be corrupted, locked, or missing
with open('config.json', 'r') as f:
    config = json.load(f)
```

---

## 🎓 Error Handling Strategies

This bot implements **three recovery strategies**:

### Strategy 1: Log and Continue ✅
**When:** For non-critical failures that don't affect trading logic.

**Example:** Discord notification fails to send.

```python
def send_discord_notification(message):
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, ...)
        response.raise_for_status()
    except Exception as error:
        # Log the error but don't stop the bot
        logging.error(f"Discord notification failed: {error}")
        print(f"⚠️ Discord error: {error}")
        # The trade was still placed, so bot continues
```

### Strategy 2: Log and Skip Cycle ⏭️
**When:** For critical failures where the bot cannot make informed decisions.

**Example:** Cannot fetch market data.

```python
bars = get_historical_bars(SYMBOL, days_limit=100)

if bars is None:
    # CRITICAL: Cannot get market data
    print("⚠️ Could not fetch market data. Skipping this cycle.")
    logging.warning("Skipping cycle due to data fetch failure")
    send_discord_notification("⚠️ Data fetch failed - skipping cycle")
    time.sleep(CHECK_INTERVAL_SECONDS)
    continue  # Skip to next iteration
```

### Strategy 3: Circuit Breaker 🚨
**When:** Too many consecutive errors suggest a systemic problem.

**Example:** 5 consecutive API failures.

```python
consecutive_errors = 0
MAX_CONSECUTIVE_ERRORS = 5

# In main loop:
if bars is None:
    consecutive_errors += 1
else:
    consecutive_errors = 0  # Reset on success

if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
    print("🚨 CRITICAL: Too many consecutive errors!")
    logging.critical("Circuit breaker triggered")
    send_discord_notification("🚨 Bot paused - too many errors")
    time.sleep(300)  # Pause for 5 minutes
    consecutive_errors = 0
```

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client
- `pandas` - Data manipulation
- `requests` - HTTP requests for Discord

### Step 2: Configure Your Bot

Copy the example configuration:

```bash
# Windows
copy config.example.json config.json

# macOS/Linux
cp config.example.json config.json
```

Edit `config.json` with your details:

```json
{
  "api_key": "YOUR_API_KEY_HERE",
  "api_secret": "YOUR_API_SECRET_HERE",
  "paper_trading": true,
  "trade_symbol": "SPY",
  "trade_quantity": 10,
  "strategy_parameters": {
    "short_window": 40,
    "long_window": 100
  },
  "check_interval_seconds": 300,
  "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
}
```

⚠️ **IMPORTANT:** Keep `paper_trading: true` while learning!

### Step 3: Run Your Resilient Bot

```bash
python resilient_bot.py
```

---

## 📊 What the Bot Does

### On Startup

1. ✅ **Loads configuration** with error handling
2. ✅ **Initializes Alpaca clients** with error handling
3. ✅ **Loads saved state** (or creates default if file is missing/corrupted)
4. ✅ **Synchronizes state with broker** (with fallback if API fails)
5. ✅ **Sends startup notification** to Discord
6. ✅ **Displays account info** (if available)

### In Main Loop (Every 5 Minutes)

1. ✅ **Fetches market data** with timeout and connection error handling
2. ✅ **Calculates moving averages** with data validation
3. ✅ **Detects trading signals** with error handling
4. ✅ **Executes trades** with comprehensive error handling
5. ✅ **Updates and saves state** with file operation error handling
6. ✅ **Sends notifications** for all actions and errors

### Error Scenarios Handled

| Scenario | Bot Response |
|----------|-------------|
| API timeout | Logs error, sends notification, skips cycle |
| Network connection lost | Logs error, sends notification, skips cycle |
| Market closed | Logs specific error, skips cycle |
| Insufficient buying power | Logs specific error, does not update state |
| Discord webhook fails | Logs warning, continues (notification not critical) |
| Config file corrupted | Logs error and exits (critical - cannot continue) |
| State file corrupted | Logs warning, starts with default state |
| Too many consecutive errors | Triggers circuit breaker, pauses for 5 minutes |

---

## 📁 Project Structure

```
Alpaca25/
├── resilient_bot.py         # Main bot script with comprehensive error handling
├── config.json               # Your configuration (not tracked by git)
├── config.example.json       # Template configuration file
├── state.json                # Bot's state (created automatically)
├── state.example.json        # Example state file
├── trading_bot.log           # Log file (created automatically)
├── requirements.txt          # Python dependencies
├── .gitignore                # Protects your API keys
├── instructions.md           # Lesson instructions
└── README.md                 # This file
```

---

## 🔍 Code Walkthrough

### 1. Configuration Loading with Error Handling

```python
def load_configuration():
    """
    Load configuration from JSON file with comprehensive error handling.
    WHY: File operations can fail, so we need to handle those errors gracefully.
    """
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
        print("✅ Configuration loaded successfully!")
        return config
    
    except FileNotFoundError:
        print("❌ Error: config.json not found")
        exit(1)  # Critical error - cannot continue
    
    except json.JSONDecodeError as error:
        print(f"❌ Error: Invalid JSON format: {error}")
        exit(1)  # Critical error - cannot continue
    
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        exit(1)
```

**Key Points:**
- ✅ Specific exception types for different errors
- ✅ Helpful error messages for users
- ✅ Exits on critical errors (cannot run without config)

### 2. API Call Error Handling

```python
def get_historical_bars(symbol, days_limit):
    """
    Fetch historical data with comprehensive error handling.
    """
    try:
        request_params = StockBarsRequest(...)
        bars = data_client.get_stock_bars(request_params)
        return bars.df
    
    except requests.exceptions.Timeout:
        logging.error("API request timed out")
        return None  # Caller will handle the None
    
    except requests.exceptions.ConnectionError:
        logging.error("Network connection error")
        return None
    
    except Exception as error:
        logging.error(f"Error fetching data: {error}")
        return None
```

**Key Points:**
- ✅ Catches specific exception types
- ✅ Returns `None` on failure (not critical - can retry)
- ✅ Logs detailed error information

### 3. Order Submission with Specific Error Messages

```python
def submit_market_order(symbol, quantity, side):
    """
    Submit order with detailed error handling.
    """
    try:
        order = trading_client.submit_order(order_data=market_order_data)
        logging.info(f"Order submitted: {order.id}")
        return order
    
    except Exception as error:
        error_str = str(error).lower()
        
        # Provide specific error messages
        if 'insufficient' in error_str and 'buying power' in error_str:
            error_message = "Insufficient buying power"
        elif 'market is closed' in error_str:
            error_message = "Market is closed"
        else:
            error_message = f"Order failed: {error}"
        
        logging.error(error_message)
        return None
```

**Key Points:**
- ✅ Parses error messages for specific issues
- ✅ Provides user-friendly error explanations
- ✅ Returns `None` so caller knows order failed

### 4. Circuit Breaker Pattern

```python
consecutive_errors = 0
MAX_CONSECUTIVE_ERRORS = 5

while True:
    try:
        bars = get_historical_bars(SYMBOL, days_limit=100)
        
        if bars is None:
            consecutive_errors += 1
            time.sleep(CHECK_INTERVAL_SECONDS)
            continue
        else:
            consecutive_errors = 0  # Reset on success
        
        # ... rest of logic ...
        
        # Check circuit breaker
        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
            logging.critical("Circuit breaker triggered")
            send_discord_notification("🚨 Too many errors - pausing")
            time.sleep(300)  # 5 minute pause
            consecutive_errors = 0
```

**Key Points:**
- ✅ Tracks consecutive failures
- ✅ Pauses when too many errors occur
- ✅ Prevents infinite error loop
- ✅ Resets counter after long pause

---

## 🎯 Trading Strategy

### Golden Cross / Death Cross

- **BUY Signal (Golden Cross):** Short-term SMA (40 days) crosses **above** long-term SMA (100 days)
- **SELL Signal (Death Cross):** Short-term SMA (40 days) crosses **below** long-term SMA (100 days)

### Position Management

- **State Persistence:** Bot remembers if it's in a position (survives restarts)
- **Broker Synchronization:** On startup, verifies state against actual Alpaca position
- **Error-Safe Updates:** State only updated after successful order execution

---

## 📢 Discord Notifications

The bot sends real-time notifications for:

### Success Events ✅
- Bot startup
- Buy orders executed
- Sell orders executed
- Position opened/closed

### Warning Events ⚠️
- State mismatch detected
- Data fetch failures
- Notification send failures
- Skipped cycles

### Error Events ❌
- Order submission failures
- Position close failures
- API errors
- Circuit breaker triggers

### Shutdown Events 🛑
- Manual bot shutdown
- Final state saved

**Notification Format:**

```
🚀 **BUY Order Executed**
```
Symbol: SPY
Quantity: 10 shares
Price: $475.32
Signal: Golden Cross
SMA 40: $476.15
SMA 100: $474.28
Order ID: abc-123-xyz
```
```

---

## 🔐 Security Best Practices

### ✅ What This Bot Does Right

1. **No Hardcoded API Keys**
   - Keys stored in `config.json`
   - `config.json` is in `.gitignore`

2. **Paper Trading by Default**
   - Safe environment for testing
   - No real money at risk

3. **Comprehensive Logging**
   - All actions logged
   - All errors logged with context
   - Audit trail for debugging

4. **State Verification**
   - Checks actual positions on startup
   - Detects and corrects state mismatches

### ⚠️ Additional Recommendations

1. **Rotate API Keys Regularly**
   - Generate new keys every 90 days

2. **Monitor Log Files**
   - Check `trading_bot.log` daily
   - Look for patterns in errors

3. **Set Up Alerts**
   - Discord notifications are just the start
   - Consider email or SMS for critical errors

4. **Test in Paper Trading First**
   - Run for at least 2 weeks in paper mode
   - Verify error handling works as expected

5. **Have a Manual Override Plan**
   - Know how to manually close positions on Alpaca website
   - Have phone app installed for emergency access

---

## 🐛 Troubleshooting

### Problem: Bot immediately crashes on startup

**Possible Causes:**
1. `config.json` doesn't exist or has invalid JSON
2. API keys are incorrect

**Solutions:**
```bash
# Check if config.json exists
ls config.json  # macOS/Linux
dir config.json  # Windows

# Validate JSON format
python -m json.tool config.json

# Test API keys manually
python
>>> from alpaca.trading.client import TradingClient
>>> client = TradingClient("your_key", "your_secret", paper=True)
>>> account = client.get_account()
>>> print(account.status)
```

### Problem: Bot keeps skipping cycles with "Could not fetch market data"

**Possible Causes:**
1. Internet connection is unstable
2. Alpaca API is experiencing issues
3. Symbol is invalid

**Solutions:**
```bash
# Check Alpaca API status
# Visit: https://status.alpaca.markets/

# Test your internet connection
ping api.alpaca.markets

# Verify symbol is valid (must be supported by Alpaca)
```

### Problem: Discord notifications not working

**Possible Causes:**
1. Webhook URL is incorrect
2. Discord server deleted webhook
3. Network blocking Discord API

**Solutions:**
1. Test webhook manually:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"content":"Test message"}' \
  YOUR_WEBHOOK_URL
```

2. Generate new webhook in Discord:
   - Server Settings → Integrations → Webhooks → New Webhook

3. Check if `discord_webhook_url` is in `config.json`

### Problem: State file corrupted

**Symptoms:** Bot always thinks it's in/out of position incorrectly

**Solution:**
```bash
# Delete corrupted state file
rm state.json  # macOS/Linux
del state.json  # Windows

# Bot will synchronize state with broker on next startup
```

### Problem: Too many consecutive errors / Circuit breaker triggering

**Possible Causes:**
1. Alpaca API is down for extended period
2. API keys revoked or expired
3. Network connectivity issues

**Solutions:**
1. Check Alpaca API status: https://status.alpaca.markets/
2. Verify API keys in Alpaca dashboard
3. Check network connectivity
4. Wait for circuit breaker to reset (5 minutes)
5. Consider increasing `CHECK_INTERVAL_SECONDS` to reduce API call frequency

---

## 📊 Sample Output

### Successful Startup

```
======================================================================
📚 Alpaca Trading Course - Lesson 25
📖 Making Your Bot Resilient – Handling API and Connection Errors
======================================================================

======================================================================
🛡️  Resilient Trading Bot Starting...
======================================================================
📊 Trading Symbol: SPY
📏 Quantity per Trade: 10 shares
📈 Strategy: Golden Cross (40/100 SMA)
⏱️  Check Interval: 300 seconds
🔧 Paper Trading: True
📢 Discord Notifications: ✅ ENABLED
======================================================================
🛡️  This bot includes comprehensive error handling!
   It will survive temporary API failures and network issues.
======================================================================

📂 Loading configuration from config.json...
✅ Configuration loaded successfully!
✅ Alpaca API clients initialized successfully!
✅ State file found. Loaded bot state from disk.

📋 Loaded State: is_in_position = False
🔄 Synchronizing state with broker for SPY...
ℹ️  No existing position found on Alpaca for SPY
✅ State is synchronized with broker.

💰 Account Info:
   Portfolio Value: $100,000.00
   Buying Power: $100,000.00
   Cash: $100,000.00

🔄 Starting main loop...

--- Loop running at 2024-03-15 14:30:00 ---
📊 Current Price: $475.32
📈 SMA 40: $476.15
📉 SMA 100: $474.28
📋 Current State: is_in_position = False
⏸️  No entry signal detected. Waiting...

💤 Sleeping for 300 seconds...
```

### Handling an API Error

```
--- Loop running at 2024-03-15 14:35:00 ---
❌ Error: API request timed out while fetching historical data
⚠️  CRITICAL: Could not fetch market data.
   STRATEGY: Skip this cycle and try again later.
💤 Sleeping for 300 seconds...

--- Loop running at 2024-03-15 14:40:00 ---
📊 Current Price: $475.89
📈 SMA 40: $476.22
📉 SMA 100: $474.35
📋 Current State: is_in_position = False
⏸️  No entry signal detected. Waiting...
```

### Successful Trade Execution

```
--- Loop running at 2024-03-15 09:35:00 ---
📊 Current Price: $478.50
📈 SMA 40: $475.80
📉 SMA 100: $475.20
📋 Current State: is_in_position = False

======================================================================
🎯 GOLDEN CROSS DETECTED!
======================================================================
📊 Short SMA (40) crossed above Long SMA (100)
💰 Attempting to buy 10 shares of SPY
✅ Order submitted successfully!
   Order ID: f3a8c7e2-4d5f-4a8b-9c3d-2e1f7b8a9c4d
   Symbol: SPY
   Quantity: 10
   Side: buy
✅ Position opened and state saved!
💾 State saved to disk: {'is_in_position': True}
```

---

## 📈 Next Steps

### Lesson 26: Advanced Risk Management
- Position sizing based on volatility
- Maximum drawdown protection
- Portfolio heat management

### Lesson 27: Multi-Symbol Trading
- Trading multiple assets simultaneously
- Correlation analysis
- Portfolio diversification

### Lesson 28: Backtesting Framework
- Historical strategy testing
- Performance metrics calculation
- Strategy optimization

---

## 🎓 Key Takeaways

1. **Error Handling is Not Optional** – It's a fundamental requirement for any production system

2. **Three Recovery Strategies:**
   - **Log and Continue** for non-critical errors
   - **Log and Skip Cycle** for critical decision-making errors
   - **Circuit Breaker** for systemic failures

3. **Specific Exception Handling** – Catch specific exception types for better error messages

4. **Comprehensive Logging** – Log everything: successes, warnings, errors

5. **Real-Time Notifications** – Combine logging with Discord notifications for immediate awareness

6. **State Safety** – Only update state after successful operations

7. **Graceful Degradation** – Bot should continue running even when non-critical components fail

---

## 📚 Additional Resources

### Python Exception Handling
- [Python Official Docs - Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Real Python - Exception Handling](https://realpython.com/python-exceptions/)

### Alpaca API
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca API Status Page](https://status.alpaca.markets/)
- [Alpaca Python SDK](https://github.com/alpacahq/alpaca-py)

### Resilience Patterns
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Retry Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/retry)

---

## 📝 License

This is educational material for learning algorithmic trading with Alpaca API.

---

## ⚠️ Disclaimer

This bot is for educational purposes only. Trading involves substantial risk of loss. Always:

- ✅ Test in paper trading mode first
- ✅ Never risk more than you can afford to lose
- ✅ Understand the strategy before running with real money
- ✅ Monitor your bot regularly
- ✅ Have a manual override plan

**Past performance does not guarantee future results.**

---

## 💬 Support

Found an issue? Have questions?

- Check the troubleshooting section above
- Review the log file: `trading_bot.log`
- Check Alpaca API status: https://status.alpaca.markets/

---

**"Risk comes from not knowing what you're doing." - Warren Buffett**

Your bot is now resilient and ready for the real world! 🛡️

---

*Alpaca Trading Course - Lesson 25*
*Making Your Bot Resilient – Handling API and Connection Errors*

