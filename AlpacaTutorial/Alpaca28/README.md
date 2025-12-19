# Lesson 28: **Faster Than HTTP – Streaming Real-Time Data with WebSockets**

Welcome to Lesson 28 of the Alpaca Trading Course! This lesson teaches you how to upgrade your bot from polling to professional, event-driven architecture using WebSockets. You'll learn why polling is inefficient and how WebSockets enable real-time data streaming.

## The Problem: Polling (HTTP Request/Response) is Slow and Inefficient

When your bot makes standard API calls, it follows this pattern: open connection, ask for latest price, receive answer, close connection, wait 60 seconds, repeat. This has major drawbacks: latency (you only get new information when you ask - if price spikes and crashes within your wait period, your bot is oblivious), inefficiency (each request has overhead, most of the time price hasn't changed), and API rate limits (aggressive polling can get you temporarily blocked).

| Problem/Challenge | Description |
|---|---|
| **Latency** | Only get new information when you ask for it - miss rapid price movements |
| **Inefficiency** | Most requests are wasteful - price hasn't changed |
| **Rate Limiting** | Many services limit requests per minute - polling aggressively can get blocked |
| **No Real-Time Reaction** | Cannot react instantly to market changes |

## The Solution: WebSockets for Real-Time Streaming

The solution is to use WebSockets - a persistent, two-way communication channel between your bot and the Alpaca server. Instead of your bot repeatedly asking for data, the server pushes the data to your bot the instant it becomes available. This is how modern, real-time applications work and is essential for trading strategies that need to react quickly to market changes.

### Step 28.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client with WebSocket support

### Step 28.2: Configure Your API Credentials

Copy the example configuration and edit `config.py` with your Alpaca API credentials:

```bash
copy config.example.py config.py
```

⚠️ **IMPORTANT:** Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

### Step 28.3: Run the WebSocket Stream

Execute the stream script:

```bash
python websocket_stream.py
```

The script will:
1. Connect to Alpaca's WebSocket stream
2. Subscribe to real-time trade data for SPY and TSLA
3. Print trade information as it arrives in real-time
4. Run until you press Ctrl+C

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Event-Driven Architecture** | WebSockets enable event-driven bots that react instantly to market data |
| **Persistent Connection** | Connection stays open, allowing server to push data immediately |
| **Subscribe to Symbols** | Subscribe only to symbols you need to reduce bandwidth |
| **Handle Reconnections** | Implement reconnection logic for when connection drops |
| **Async Handlers** | Use async handlers to process incoming data efficiently |

## Conclusion

You've successfully learned how to use WebSockets for real-time data streaming! This upgrades your bot from slow polling to professional, event-driven architecture. Your bot can now react instantly to market changes instead of waiting for the next polling cycle. This is essential for high-frequency strategies and professional trading systems. In the next lesson, you'll learn about deploying your bot to a VPS server for 24/7 operation.
