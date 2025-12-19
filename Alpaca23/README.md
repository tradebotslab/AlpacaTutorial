# 📚 Alpaca Trading Tutorial 23: What If the Bot Restarts? – Managing Position State

## 🎯 What You'll Learn

In this tutorial, you'll discover how to make your trading bot resilient to crashes and restarts. You'll learn how to:

- ✅ Save the bot's position state to an external file
- ✅ Load and restore state when the bot restarts
- ✅ Synchronize bot state with the broker's reality
- ✅ Prevent dangerous double-positions or missed trades
- ✅ Build a production-ready bot that survives interruptions

**Learning Outcome**: After this lesson, your bot will have a memory that persists across restarts!

---

## 🚨 The Problem: Bot Amnesia

Imagine this scenario:

1. Your bot buys 10 shares of SPY. It is now "in a position".
2. The server running your bot reboots for a system update.
3. Your bot script starts again.
4. Since it has no memory, it checks the market, gets a buy signal, and buys 10 MORE shares of SPY.

**You've doubled your position and your risk!** This happens because the bot's internal state (like `is_in_position = True`) is reset to default values on every restart.

### The Danger of Stateless Bots

| Scenario | Without State Management | With State Management |
|----------|--------------------------|----------------------|
| **Bot Restart** | Forgets it has a position | Remembers position from file |
| **Buy Signal** | Buys again (double position!) | Skips buy (already in position) |
| **Risk** | Unintended over-exposure | Controlled risk |
| **Recovery** | Manual intervention needed | Automatic recovery |

---

## ✅ The Solution: Persistent State File

Just as we separated configuration into `config.json` (Lesson 22), we'll save operational state to `state.json`. This file acts as the bot's **persistent memory**.

### How It Works

```
Bot Lifecycle:
┌─────────────────┐
│  Bot Starts     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Load state.json │  ← Restore memory
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Synchronize     │  ← Verify with broker
│ with Broker     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Run Strategy    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute Trade   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Save state.json │  ← Update memory
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Repeat...       │
└─────────────────┘
```

---

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.8 or higher installed
- ✅ An Alpaca account (paper trading is fine)
- ✅ Completed Tutorial 22 (External Config Files)
- ✅ Understanding of JSON format

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

### Step 4: Create Your State File

```bash
# Copy the example state to create your own
copy state.example.json state.json  # Windows
# or
cp state.example.json state.json    # Mac/Linux
```

The initial `state.json` should contain:

```json
{
  "is_in_position": false
}
```

### Step 5: Add Your API Keys

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
python state_bot.py
```

### What You'll See

```
📂 Loading configuration from config.json...
✅ Configuration loaded successfully!

======================================================================
🚀 State-Managed Trading Bot Starting...
======================================================================
📊 Trading Symbol: SPY
📏 Quantity per Trade: 10 shares
📈 Strategy: Golden Cross (40/100 SMA)
⏱️  Check Interval: 300 seconds
🔧 Paper Trading: True
======================================================================

✅ State file found. Loaded bot state from disk.
📋 Loaded State: is_in_position = False

🔄 Synchronizing state with broker for SPY...
ℹ️  No existing position found on Alpaca for SPY
✅ State is synchronized with broker.

💡 State management ensures the bot remembers its position across restarts!
   Even if this script crashes, it will recover correctly.
```

---

## 🎮 How It Works

### 1. State Loading on Startup

```python
def load_state():
    """Loads the bot's state from the state file."""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, return a default state
        return {'is_in_position': False}
```

**What happens:**
- Bot reads `state.json` to check if it was in a position
- If file doesn't exist, assumes no position (safe default)
- Logs the loaded state for debugging

### 2. Synchronizing with Broker

```python
def synchronize_state_with_broker(symbol):
    """Verifies the bot's state against the broker."""
    try:
        position = trading_client.get_open_position(symbol)
        # If this succeeds, we have a position
        return True
    except Exception:
        # No position found
        return False
```

**Why this is critical:**
- The broker is the **ultimate source of truth**
- Protects against corrupted state files
- Ensures bot and reality are aligned

### 3. Saving State After Actions

```python
# After a successful BUY order
is_in_position = True
bot_state['is_in_position'] = True
save_state(bot_state)

# After a successful SELL order
is_in_position = False
bot_state['is_in_position'] = False
save_state(bot_state)
```

**Critical timing:**
- State is saved **immediately after** a successful trade
- If bot crashes mid-trade, broker sync will correct it on restart
- Every state change is logged

---

## 🧪 Testing State Persistence

### Test 1: Normal Operation

1. Start the bot: `python state_bot.py`
2. Wait for a buy signal (Golden Cross)
3. Check `state.json` - it should show `"is_in_position": true`
4. Stop the bot (Ctrl+C)
5. Restart the bot
6. **Result**: Bot remembers it has a position and won't buy again

### Test 2: Manual State Corruption

1. While bot is running and in a position, edit `state.json`
2. Change `"is_in_position": true` to `false`
3. Restart the bot
4. **Result**: Bot detects mismatch with broker and corrects state

### Test 3: Crash Recovery

1. Start the bot
2. Wait for a buy signal
3. Force-kill the bot (Task Manager or `kill` command)
4. Restart the bot
5. **Result**: Bot reads state file and continues correctly

---

## 📊 The Trading Strategy

The bot uses a **Golden Cross / Death Cross** strategy:

### Entry Signal: Golden Cross
- **When**: Short-term SMA (40-day) crosses **above** long-term SMA (100-day)
- **Action**: BUY (if not already in position)
- **State Update**: `is_in_position = True`

### Exit Signal: Death Cross
- **When**: Short-term SMA (40-day) crosses **below** long-term SMA (100-day)
- **Action**: SELL (if in position)
- **State Update**: `is_in_position = False`

### State-Aware Logic

```python
if not is_in_position:
    # Look for entry signal
    if detect_golden_cross():
        buy()
        save_state({'is_in_position': True})
else:
    # Look for exit signal
    if detect_death_cross():
        sell()
        save_state({'is_in_position': False})
```

---

## 📁 File Structure

```
Alpaca22/
├── state_bot.py              # Main bot script with state management
├── config.example.json       # Template configuration
├── config.json              # Your actual config (NEVER commit!)
├── state.example.json       # Template state file
├── state.json              # Bot's persistent memory (NEVER commit!)
├── trading_bot.log         # Execution logs
├── requirements.txt        # Python dependencies
├── .gitignore             # Protects sensitive files
├── instructions.md        # Detailed lesson content
└── README.md             # This file
```

---

## 🔒 Security Best Practices

### Files to NEVER Commit

Your `.gitignore` already protects:

```gitignore
# API Keys and Secrets
config.json

# Bot State (may contain sensitive trading info)
state.json

# Logs (may contain API keys or sensitive data)
*.log
```

### Safe to Share

- ✅ `state_bot.py` - The code
- ✅ `config.example.json` - Template with placeholders
- ✅ `state.example.json` - Template with default state
- ✅ `README.md` - Documentation
- ✅ `requirements.txt` - Dependencies

---

## 🐛 Troubleshooting

### Problem: "State file not found"

**Solution**: This is normal on first run. The bot will create the file automatically.

```bash
# Or create it manually:
copy state.example.json state.json  # Windows
cp state.example.json state.json    # Mac/Linux
```

### Problem: "State mismatch detected"

**Example output:**
```
⚠️  WARNING: State mismatch detected!
   Saved state: False
   Actual broker state: True
   Updating local state to match broker...
```

**What it means**: The state file says "not in position" but the broker shows you have a position.

**Solution**: This is actually **good**! The bot detected the mismatch and corrected it automatically. This protects you from:
- Corrupted state files
- Manual trades made outside the bot
- Missed state updates

### Problem: Bot buys twice

**If this happens**, it means state wasn't saved properly. Check:

1. **File permissions**: Can Python write to `state.json`?
   ```bash
   # Check if file exists and is writable
   ls -l state.json  # Mac/Linux
   dir state.json    # Windows
   ```

2. **Check logs**: Look in `trading_bot.log` for errors
   ```python
   # You should see lines like:
   # "State saved: {'is_in_position': True}"
   ```

3. **Verify state file**: After a trade, manually check `state.json`

### Problem: Bot doesn't trade after restart

**Possible causes:**

1. **State shows in position**: Check `state.json` - if `"is_in_position": true`, the bot won't buy again (this is correct behavior!)

2. **No new signals**: The bot only trades on crossovers. It may take time for a new signal.

3. **Market closed**: Bot can't trade outside market hours.

---

## 📈 Example Execution Flow

### Scenario: Bot Restart During Position

```
--- First Run ---
[14:00:00] Bot starting...
[14:00:01] Loaded state: is_in_position = False
[14:00:02] Synchronizing with broker: No position found
[14:00:03] State synchronized ✅
[14:05:00] GOLDEN CROSS DETECTED!
[14:05:01] Buying 10 shares of SPY
[14:05:02] Order filled ✅
[14:05:03] State saved: is_in_position = True

--- System Reboot ---

--- Second Run (After Restart) ---
[14:30:00] Bot starting...
[14:30:01] Loaded state: is_in_position = True  ← Remembered!
[14:30:02] Synchronizing with broker: Position found (10 shares)
[14:30:03] State synchronized ✅
[14:30:04] Holding position. Monitoring for exit signal...
[14:35:00] Holding position. No exit signal.
[14:40:00] Holding position. No exit signal.
[14:45:00] DEATH CROSS DETECTED!
[14:45:01] Closing position on SPY
[14:45:02] Position closed ✅
[14:45:03] State saved: is_in_position = False
```

**Key observation**: After restart at 14:30, the bot correctly remembered it had a position and didn't try to buy again!

---

## 🎓 Key Takeaways

### What You Learned

1. **State Persistence**: How to save and restore bot state across restarts
2. **Broker Synchronization**: Using the broker as the source of truth
3. **Error Recovery**: Automatic detection and correction of state mismatches
4. **Production Readiness**: Building bots that can run unsupervised
5. **Logging**: Using logs to track state changes and debug issues

### Before This Tutorial

```python
# Bot forgets its position on restart
is_in_position = False  # Always starts as False
# Risk: May buy twice if restarted during a position
```

### After This Tutorial

```python
# Bot remembers its position
bot_state = load_state()  # Loads from file
is_in_position = synchronize_with_broker()  # Verifies with broker
# Result: Bot always knows the correct state
```

**The Result**: A resilient bot that survives crashes, reboots, and interruptions!

---

## 🔧 Customization Ideas

### Add More State Information

Extend `state.json` to track additional information:

```json
{
  "is_in_position": true,
  "entry_price": 450.25,
  "entry_time": "2024-01-15T14:05:00Z",
  "shares": 10,
  "stop_loss": 445.00
}
```

### Multiple Symbols

Track state for multiple symbols:

```json
{
  "positions": {
    "SPY": {"is_in_position": true, "qty": 10},
    "AAPL": {"is_in_position": false, "qty": 0}
  }
}
```

### Trade History

Keep a history of trades:

```json
{
  "is_in_position": false,
  "trade_history": [
    {
      "symbol": "SPY",
      "action": "BUY",
      "qty": 10,
      "price": 450.25,
      "timestamp": "2024-01-15T14:05:00Z"
    },
    {
      "symbol": "SPY",
      "action": "SELL",
      "qty": 10,
      "price": 455.00,
      "timestamp": "2024-01-15T16:30:00Z",
      "profit": 47.50
    }
  ]
}
```

---

## 📚 Additional Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Python JSON Module](https://docs.python.org/3/library/json.html)
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Stateful vs Stateless Applications](https://www.redhat.com/en/topics/cloud-native-apps/stateful-vs-stateless)

---

## ⚠️ Important Disclaimers

- **Paper Trading**: This tutorial uses paper trading by default. No real money is at risk.
- **Educational Purpose**: This bot is for learning. Not financial advice.
- **No Guarantees**: Past performance doesn't guarantee future results.
- **Risk Warning**: Trading involves risk. Only trade with money you can afford to lose.
- **Test Thoroughly**: Always test state management thoroughly before live trading.

---

## 💡 Pro Tips

### Tip #1: Always Check Logs

The `trading_bot.log` file is your friend:

```bash
# View recent logs
tail -f trading_bot.log  # Mac/Linux
Get-Content trading_bot.log -Tail 20 -Wait  # Windows PowerShell
```

### Tip #2: Backup State File

Before major changes, backup your state:

```bash
copy state.json state_backup.json  # Windows
cp state.json state_backup.json    # Mac/Linux
```

### Tip #3: Monitor State File

Watch state changes in real-time:

```bash
# Mac/Linux
watch -n 5 cat state.json

# Windows PowerShell
while ($true) { Clear-Host; Get-Content state.json; Start-Sleep -Seconds 5 }
```

### Tip #4: Use Absolute Timestamps

For production bots, add timestamps to state:

```json
{
  "is_in_position": true,
  "last_updated": "2024-01-15T14:05:03Z"
}
```

This helps debug issues and understand state age.

---

## 🎉 Congratulations!

You've just built a **production-ready trading bot** with state management! Your bot can now:

- 🔄 **Survive restarts** without losing its memory
- ✅ **Synchronize with reality** using broker verification
- 🛡️ **Prevent double-positions** through state awareness
- 📊 **Log everything** for debugging and auditing
- 🚀 **Run unsupervised** with confidence

**"Risk comes from not knowing what you're doing." - Warren Buffett**

And now you know how to build resilient, state-aware trading bots! 🚀

---

## 🔄 Next Steps

1. **Run the bot** and observe state changes
2. **Test crash recovery** by force-killing and restarting
3. **Add more state** like entry prices and timestamps
4. **Implement stop-loss** using saved entry prices
5. **Track performance** by logging all trades to state
6. **Build a dashboard** that reads and displays state

---

## 📞 Questions or Issues?

If you encounter any problems or have questions:

1. Check the Troubleshooting section above
2. Review `trading_bot.log` for detailed error messages
3. Verify your `state.json` file is properly formatted
4. Consult the [Alpaca Community Forum](https://forum.alpaca.markets/)
5. Review the code comments - they explain the "why" behind each decision

---

**Happy Trading! 📈**

*Remember: Always test with paper trading first. This is educational content, not financial advice.*
