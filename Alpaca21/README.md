# 📝 Lesson 21: The Bot's "Black Box" – Logging Every Decision to a File

## 🎯 What You'll Learn

In this lesson, you'll master the art of **comprehensive logging** in algorithmic trading. You'll learn how to:

- ✅ Set up Python's `logging` library for production-grade logging
- ✅ Use different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- ✅ Implement rotating log files to prevent disk space issues
- ✅ Log both to file and console simultaneously
- ✅ Create a complete audit trail of every trading decision
- ✅ Debug errors using detailed log files
- ✅ Monitor bot performance through log analysis

## 🚨 Why Logging Is Non-Negotiable

Think of a log file as your bot's **diary**. Without proper logging, you're flying blind:

| Problem | Solution with Logging |
|---------|----------------------|
| Bot makes unexpected trade | Review log to see exact decision logic |
| Crash at 3 AM | Log shows what happened before crash |
| Poor performance | Analyze logs to identify losing strategies |
| Audit requirements | Complete record of all trading activity |
| Debugging | See exact state when error occurred |

**Remember**: In algorithmic trading, if it's not logged, it didn't happen.

## 📁 Project Structure

```
Alpaca21/
├── logging_bot.py          # Main bot with comprehensive logging
├── config.example.py       # Template for API credentials
├── requirements.txt        # Python dependencies
├── .gitignore             # Protects your API keys
├── instructions.md        # Detailed lesson content
└── README.md              # This file
```

## 🔧 Installation

### Step 1: Clone or Download

```bash
cd Alpaca21
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Credentials

1. Copy the example config:
```bash
cp config.example.py config.py
```

2. Edit `config.py` with your Alpaca API credentials:
```python
API_KEY = 'your_actual_api_key'
SECRET_KEY = 'your_actual_secret_key'
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading
```

⚠️ **IMPORTANT**: Never commit `config.py` to git! It's protected by `.gitignore`.

## 🚀 Running the Bot

### Basic Run

```bash
python logging_bot.py
```

The bot will:
- ✅ Create a `trading_bot.log` file
- ✅ Display logs in the console
- ✅ Check market status every 60 seconds
- ✅ Make trading decisions during market hours
- ✅ Log every action and error

### Stop the Bot

Press `Ctrl+C` to stop gracefully. The bot will log a final shutdown message.

## 📊 Understanding Log Levels

The bot uses five severity levels:

| Level | When to Use | Example |
|-------|-------------|---------|
| `DEBUG` | Detailed information for diagnosis | "Current position: 10 shares" |
| `INFO` | General informational messages | "Bot started", "Order submitted" |
| `WARNING` | Something unexpected but not critical | "Price unavailable, skipping" |
| `ERROR` | Error occurred but bot can continue | "Failed to submit order" |
| `CRITICAL` | Serious error, bot may need to stop | "Cannot connect to API" |

## 📄 Log File Format

Each log entry includes:

```
2025-12-18 10:30:45 - root - INFO - ✓ BUY ORDER SUBMITTED - Order ID: abc123
```

- **Timestamp**: When the event occurred
- **Logger name**: Which part of the code logged it
- **Level**: Severity of the message
- **Message**: What happened

## 🔄 Log Rotation

The bot uses **RotatingFileHandler** to prevent log files from growing too large:

- Max file size: **5 MB**
- Backup files: **3** (keeps last 3 rotated logs)
- When `trading_bot.log` reaches 5 MB, it becomes `trading_bot.log.1`
- Previous `trading_bot.log.1` becomes `trading_bot.log.2`
- And so on...

This prevents disk space issues in long-running bots.

## 💡 Key Features

### 1. Dual Output (File + Console)

```python
# File handler - saves everything (DEBUG and above)
file_handler = RotatingFileHandler('trading_bot.log', maxBytes=5*1024*1024)
file_handler.setLevel(logging.DEBUG)

# Console handler - shows important stuff (INFO and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
```

### 2. Comprehensive Order Logging

Every order includes:
- ✅ Symbol and quantity
- ✅ Order type and price
- ✅ Order ID for tracking
- ✅ Submission status
- ✅ Fill price and status

### 3. Exception Handling

All API calls are wrapped in try-except blocks:

```python
try:
    order = api.submit_order(...)
    logging.info(f"✓ Order submitted: {order.id}")
except Exception as error:
    logging.error(f"✗ Failed to submit order: {error}")
```

### 4. Account Status on Startup

The bot logs your account details when starting:

```
Account Status: ACTIVE
Buying Power: $100,000.00
Portfolio Value: $102,350.00
```

## 🎓 Educational Features

This bot demonstrates:

1. **RotatingFileHandler**: Automatic log rotation
2. **Multiple handlers**: File + console output
3. **Custom formatting**: Timestamps and severity levels
4. **Different log levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
5. **Exception logging**: Full traceback for errors
6. **Audit trail**: Complete record of all decisions

## 📈 Analyzing Your Logs

### Find All Orders

```bash
# Windows PowerShell
Select-String "ORDER SUBMITTED" trading_bot.log

# Linux/Mac
grep "ORDER SUBMITTED" trading_bot.log
```

### Find All Errors

```bash
# Windows PowerShell
Select-String "ERROR" trading_bot.log

# Linux/Mac
grep "ERROR" trading_bot.log
```

### Count Decisions

```bash
# Windows PowerShell
(Select-String "DECISION" trading_bot.log).Count

# Linux/Mac
grep -c "DECISION" trading_bot.log
```

## 🛠️ Customization

### Change Symbol

```python
SYMBOL = "TSLA"  # Trade Tesla instead of Apple
```

### Change Check Interval

```python
CHECK_INTERVAL_SECONDS = 300  # Check every 5 minutes
```

### Change Log File Size

```python
MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10 MB instead of 5 MB
```

### Change Trading Logic

Replace the simple time-based logic in `make_trade_decision()` with your strategy.

## 🔒 Security Best Practices

1. ✅ **Never commit `config.py`** - It's in `.gitignore`
2. ✅ **Use paper trading** - Start with `paper-api.alpaca.markets`
3. ✅ **Review logs regularly** - Check for unexpected behavior
4. ✅ **Rotate logs** - Prevents disk space issues
5. ✅ **Monitor errors** - Set up alerts for ERROR/CRITICAL logs

## 🧪 Testing Checklist

Before running with real money:

- [ ] Bot starts without errors
- [ ] Log file is created
- [ ] Account information is logged correctly
- [ ] Market status is checked
- [ ] Trading decisions are logged
- [ ] Orders are logged with all details
- [ ] Errors are caught and logged
- [ ] Bot shuts down gracefully with Ctrl+C
- [ ] Log rotation works (let it run to create 5 MB of logs)

## 📚 Next Steps

After mastering logging, consider:

1. **Log Analysis Tools**: Use ELK stack (Elasticsearch, Logstash, Kibana)
2. **Alerting**: Send email/SMS for ERROR or CRITICAL logs
3. **Performance Metrics**: Log execution time for each operation
4. **Trade Analysis**: Calculate win rate from logs
5. **Backtesting**: Use logs to replay and improve strategy

## 🐛 Troubleshooting

### Issue: No log file created

**Solution**: Check file permissions in the directory.

### Issue: Logs show "Market is CLOSED"

**Solution**: Run during market hours (Mon-Fri, 9:30 AM - 4:00 PM ET) or wait for next open.

### Issue: "API connection failed"

**Solution**: 
1. Check `config.py` has correct credentials
2. Verify internet connection
3. Check Alpaca API status: https://status.alpaca.markets

### Issue: Log file too large

**Solution**: Decrease `MAX_LOG_FILE_SIZE` or increase `BACKUP_LOG_COUNT`.

## 📖 Additional Resources

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [Alpaca Paper Trading](https://alpaca.markets/docs/trading/paper-trading/)

## 🎓 Key Takeaways

1. **Logging is mandatory** for production trading bots
2. **Use appropriate log levels** for different situations
3. **Rotate logs** to prevent disk space issues
4. **Log both to file and console** for flexibility
5. **Log exceptions** with full details
6. **Create an audit trail** of every decision

## ⚠️ Disclaimer

This bot is for **educational purposes only**. 

- Start with **paper trading** (fake money)
- Test thoroughly before using real money
- Understand the risks of algorithmic trading
- Past performance doesn't guarantee future results

## 📞 Support

Questions? Issues?

1. Check `instructions.md` for detailed explanations
2. Review the code comments (they explain WHY, not just WHAT)
3. Check your logs - they usually tell you what went wrong!

---

**"In trading, what gets measured gets managed. What gets logged gets improved."**

Happy Trading! 📈🤖

