# Lesson 6: **Anatomy of a Bot - The Main Loop**

Welcome to Lesson 6 of the Alpaca Trading Course! This lesson demonstrates the core component of any automated trading bot: the main loop. You will learn how to build a simple, infinite loop that serves as the bot's "heartbeat," allowing it to perform actions at regular, controlled intervals.

## The Problem: No Continuous Operation Mechanism

A trading bot needs to run continuously and perform actions at regular intervals. Without a main loop structure, your bot would execute once and stop, requiring manual intervention to check the market, analyze data, or place trades repeatedly.

| Problem/Challenge | Description |
|---|---|
| **One-Time Execution** | Scripts that run once cannot continuously monitor markets or respond to changing conditions |
| **No Automation** | Cannot build truly automated systems that operate 24/7 without human intervention |
| **Manual Restart Required** | Would need to manually restart the script every time you want to check the market |
| **No Scheduled Actions** | Cannot perform actions at regular intervals (e.g., check market every 5 minutes) |

## The Solution: Implement a Main Loop with Controlled Intervals

The solution is to create a main loop - an infinite `while True:` loop that performs tasks at regular intervals and then sleeps before repeating. This structure allows your bot to operate autonomously 24/7, checking the market, analyzing data, and executing trades continuously.

### Step 6.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 6.2: Configure API Credentials

1. Copy `config.py.template` to `config.py`
2. Edit `config.py` and add your Alpaca API credentials
3. Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

**Important:** The `config.py` file is excluded from git to protect your API keys. Never commit this file!

### Step 6.3: Run the Main Loop Bot

Execute the bot:

```bash
python main_loop_bot.py
```

The bot will:
- Start and display "Bot is starting..."
- Every 60 seconds, check your account status and buying power
- Continue running until you stop it with `Ctrl+C`

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Use Appropriate Sleep Intervals** | Don't sleep too short (overwhelms API) or too long (misses opportunities) |
| **Handle Errors Gracefully** | Wrap loop logic in try-except blocks so one error doesn't crash the entire bot |
| **Implement Graceful Shutdown** | Handle `KeyboardInterrupt` (Ctrl+C) to clean up resources before exiting |
| **Rate Limiting** | The `time.sleep()` command is critical to avoid overwhelming the API and getting rate-limited |
| **Logging** | Add logging to track bot activity and debug issues when the bot runs for extended periods |

## Conclusion

You've successfully built the foundation of an automated trading bot with a main loop! This infinite loop structure is the "heartbeat" of any trading bot, allowing it to run continuously and perform actions at regular intervals. The main loop enables your bot to operate autonomously without manual intervention. In future lessons, you'll learn how to add trading logic, technical indicators, and order execution inside this main loop.
