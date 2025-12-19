# Lesson 25: **Making Your Bot Resilient – Handling API and Connection Errors**

Welcome to Lesson 25 of the Alpaca Trading Course! This lesson teaches you how to transform your trading bot from a fragile script that crashes at the first sign of trouble into a resilient, production-ready system that can gracefully handle temporary API failures, network connection issues, invalid data, file operation errors, and rate limiting.

## The Problem: A Brittle Bot

Without error handling, your bot is like a house of cards. One error and the bot crashes. If the network drops for just 1 second, the bot crashes. You're now offline and have no idea if you're in a position or not. Every interaction with the outside world can fail: API calls to Alpaca, network requests to Discord, file operations for config/state files.

| Problem/Challenge | Description |
|---|---|
| **Single Point of Failure** | One API error crashes the entire bot |
| **No Recovery Mechanism** | Bot cannot recover from temporary network issues |
| **Lost State** | Crashes can leave you uncertain about positions |
| **Unreliable Operation** | Bot cannot run 24/7 if it crashes on every error |

## The Solution: Comprehensive Error Handling

The solution is to implement comprehensive error handling with three recovery strategies: (1) Log and Continue - for non-critical failures that don't affect trading logic, (2) Retry with Backoff - for temporary failures like network timeouts, and (3) Graceful Degradation - for optional features like Discord notifications.

### Step 25.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 25.2: Configure Your API Credentials

Copy the example config and add your Alpaca API credentials:

```bash
cp config.example.json config.json
```

⚠️ **IMPORTANT:** Never commit `config.json` to Git!

### Step 25.3: Run the Resilient Bot

Execute the bot:

```bash
python resilient_bot.py
```

The bot will:
- Handle API errors gracefully without crashing
- Retry failed operations with exponential backoff
- Continue running even when optional features fail
- Log all errors for debugging
- Send error notifications to Discord (if configured)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Wrap All API Calls** | Every external call should be in a try-except block |
| **Retry Logic** | Implement retry with exponential backoff for transient failures |
| **Error Logging** | Log all errors with context for debugging |
| **Graceful Degradation** | Optional features (like notifications) shouldn't crash the bot if they fail |
| **State Protection** | Ensure state is saved even if errors occur during trading logic |

## Conclusion

You've successfully learned how to make your trading bot resilient! Your bot is now virtually uncrashable - it will log errors, send notifications, and continue running even when things go wrong. This is essential for production bots that must run 24/7. In the next lesson, you'll learn about backtesting - testing your strategies on historical data before risking real money.
