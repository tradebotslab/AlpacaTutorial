# Lesson 24: **Stay Updated – Sending Real-Time Notifications to Discord**

Welcome to Lesson 24 of the Alpaca Trading Course! This lesson teaches you how to add real-time Discord notifications to your trading bot. You'll learn how to set up a private Discord server and webhook, send push notifications when trades execute, and get immediate alerts for errors and important events.

## The Problem: Running a Black Box

Your bot is running on a cloud server. You're at work. The market opens, and your bot executes a $5,000 buy order. You have no idea this happened until you manually check hours later. Or worse: An error occurs, the bot crashes, and you miss important trades. Relying solely on log files is impractical - you have to actively check them.

| Problem/Challenge | Description |
|---|---|
| **No Real-Time Awareness** | Cannot know immediately when trades execute or errors occur |
| **Manual Monitoring Required** | Must actively check logs or SSH into server to see bot status |
| **Missed Opportunities** | Discover issues hours later, missing time-sensitive actions |
| **No Peace of Mind** | Constant worry about bot status when away from computer |

## The Solution: Discord Webhooks for Real-Time Notifications

The solution is to use Discord webhooks - simple, free, and powerful URLs that your bot can send messages to. When it does, the message instantly appears in your Discord channel. Discord provides: mobile app (notifications on phone), desktop app (monitor from computer), web browser (check from anywhere), free (no cost, no limits for reasonable use), push notifications (instant alerts), rich formatting (markdown, code blocks, emojis), and privacy (your own server, complete control).

### Step 24.1: Install Required Packages

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `alpaca-py` - Alpaca API client
- `requests` - For sending HTTP requests to Discord webhook

### Step 24.2: Set Up Discord Webhook

1. Create a Discord server (or use an existing one)
2. Go to Server Settings → Integrations → Webhooks
3. Create a new webhook and copy the webhook URL
4. Add the webhook URL to your `config.json`:
   ```json
   {
     "discord_webhook_url": "https://discord.com/api/webhooks/..."
   }
   ```

### Step 24.3: Run the Notification Bot

Execute the bot:

```bash
python discord_bot.py
```

The bot will send Discord notifications for:
- Bot startup and shutdown
- Trade executions (buy/sell orders)
- Errors and warnings
- Important state changes

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Webhook Security** | Keep webhook URL private - anyone with it can send messages to your channel |
| **Rate Limiting** | Discord has rate limits; don't spam notifications |
| **Error Handling** | Wrap webhook calls in try-except so notification failures don't crash the bot |
| **Rich Formatting** | Use Discord markdown, code blocks, and emojis for readable messages |
| **Notification Levels** | Only send notifications for important events to avoid notification fatigue |

## Conclusion

You've successfully learned how to add Discord notifications to your trading bot! You'll never miss a trade or error again. Your bot will keep you informed in real-time, giving you peace of mind and allowing you to monitor your bot from anywhere. In the next lesson, you'll learn how to make your bot resilient by handling API and connection errors gracefully.
