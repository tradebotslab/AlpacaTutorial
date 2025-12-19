# Lesson 21: **The Bot's "Black Box" – Logging Every Decision to a File**

Welcome to Lesson 21 of the Alpaca Trading Course! This lesson teaches you the art of comprehensive logging in algorithmic trading. You'll learn how to set up Python's `logging` library for production-grade logging, use different log levels, implement rotating log files, and create a complete audit trail of every trading decision.

## The Problem: No Record of Trading Decisions

Without proper logging, you're flying blind. If your bot makes an unexpected trade, crashes at 3 AM, or shows poor performance, you have no way to understand what happened. There's no record of decisions, errors, or bot state when issues occur.

| Problem/Challenge | Description |
|---|---|
| **No Audit Trail** | Cannot review what the bot did or why it made certain decisions |
| **Difficult Debugging** | No way to see what happened before a crash or error |
| **Performance Analysis** | Cannot analyze bot behavior to identify losing strategies |
| **Compliance Issues** | Many trading regulations require complete records of all trading activity |

## The Solution: Comprehensive Logging System

The solution is to implement a comprehensive logging system using Python's `logging` library. This creates a complete "black box" record of every decision, error, and state change. Logs are written to both file and console, with different severity levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) and rotating log files to prevent disk space issues.

### Step 21.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 21.2: Configure API Credentials

1. Copy the example config:
```bash
cp config.example.py config.py
```

2. Edit `config.py` with your Alpaca API credentials.

⚠️ **IMPORTANT**: Never commit `config.py` to git!

### Step 21.3: Run the Logging Bot

Execute the bot:

```bash
python logging_bot.py
```

The bot will:
- Create a `trading_bot.log` file
- Display logs in the console
- Check market status every 60 seconds
- Log every action and error with appropriate severity levels

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Log Levels** | Use DEBUG for detailed info, INFO for general messages, WARNING for unexpected but non-critical issues, ERROR for problems, CRITICAL for serious failures |
| **Rotating Logs** | Use rotating file handlers to prevent log files from growing too large |
| **Dual Output** | Log to both file (for history) and console (for real-time monitoring) |
| **Complete Audit Trail** | Log every trading decision, order placement, and state change |
| **Error Context** | Include enough context in error messages to diagnose issues later |

## Conclusion

You've successfully implemented comprehensive logging for your trading bot! This creates a complete audit trail and "black box" record of all bot activity. Proper logging is essential for debugging, performance analysis, and compliance. In algorithmic trading, if it's not logged, it didn't happen. In the next lesson, you'll learn how to use external configuration files to separate settings from code.
