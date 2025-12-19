# Lesson 9: **Simple Exit Logic – Selling on a Reversal Signal**

Welcome to Lesson 9 of the Alpaca Trading Course! This lesson implements a complete moving average crossover trading bot with both entry and exit logic. You'll learn how to build a bot that not only enters trades but also exits them based on reversal signals.

## The Problem: Entering Trades Without Exit Strategy

Entering trades based on signals is only half of a complete trading strategy. Without exit logic, you might hold positions too long, miss reversal signals, or fail to lock in profits when trends change. A bot that only enters trades but never exits them is incomplete.

| Problem/Challenge | Description |
|---|---|
| **No Exit Mechanism** | Cannot automatically close positions when reversal signals occur |
| **Holding Too Long** | Positions may be held indefinitely, missing opportunities to take profits |
| **No Reversal Detection** | Cannot detect when a trend has reversed and it's time to exit |
| **Incomplete Strategy** | Trading strategies need both entry and exit logic to be effective |

## The Solution: Implement Exit Logic Based on Reversal Signals

The solution is to implement exit logic that monitors for reversal signals (like a Death Cross) and automatically closes positions when these signals occur. This creates a complete trading cycle: enter on Golden Cross, exit on Death Cross.

### Step 9.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 9.2: Configure API Keys

1. Copy `config.py` and add your Alpaca API credentials
2. Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
3. The bot uses paper trading by default (configured in `config.py`)

### Step 9.3: Run the Complete Crossover Bot

Execute the bot:

```bash
python crossover_bot_v1.py
```

The bot will:
- Check for existing positions before trading
- Detect Golden Cross entry signals and place buy orders
- Detect Death Cross exit signals and place sell orders
- Run continuously, checking for signals every 5 minutes

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Check Position Before Entry** | Always verify you don't already have a position before placing a buy order |
| **Complete Trading Cycle** | Entry (Golden Cross) and Exit (Death Cross) create a complete strategy |
| **Error Handling** | Wrap all API calls in try-except blocks to handle errors gracefully |
| **Paper Trading First** | Always test in paper trading before using real money |
| **Signal Frequency** | Golden Cross and Death Cross are rare events; be patient |

## Conclusion

You've successfully built a complete trading bot with both entry and exit logic! This bot implements a full trading cycle: it enters positions on Golden Cross signals and exits on Death Cross signals. This is a significant milestone - you now have a functional, automated trading bot. In the next lesson, you'll refine this bot further and add additional features to make it more robust and professional.
