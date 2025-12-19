# Lesson 23: **What If the Bot Restarts? – Managing Position State**

Welcome to Lesson 23 of the Alpaca Trading Course! This lesson teaches you how to make your trading bot resilient to crashes and restarts. You'll learn how to save the bot's position state to an external file, load and restore state when the bot restarts, and synchronize bot state with the broker's reality.

## The Problem: Bot Amnesia After Restart

Imagine this scenario: your bot buys 10 shares of SPY. The server reboots. Your bot script starts again. Since it has no memory, it checks the market, gets a buy signal, and buys 10 MORE shares of SPY. You've doubled your position and your risk! This happens because the bot's internal state (like `is_in_position = True`) is reset to default values on every restart.

| Problem/Challenge | Description |
|---|---|
| **State Loss on Restart** | Bot forgets it has a position when it restarts |
| **Double Positions** | Bot may buy again, creating unintended over-exposure |
| **Risk Management Failure** | Cannot properly manage risk without knowing current state |
| **Manual Intervention Required** | Must manually check and fix state after crashes |

## The Solution: Persistent State File

The solution is to save operational state to `state.json`, just as we separated configuration into `config.json`. This file acts as the bot's persistent memory. The bot lifecycle: (1) Bot starts, (2) Load state.json (restore memory), (3) Synchronize with broker (verify reality), (4) Run strategy, (5) Execute trade, (6) Save state.json (update memory), (7) Repeat.

### Step 23.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 23.2: Configure Your API Keys

1. Copy the example config:
   ```bash
   cp config.example.json config.json
   ```

2. Edit `config.json` with your Alpaca API credentials.

⚠️ **IMPORTANT:** Never commit `config.json` to Git!

### Step 23.3: Run the State-Managed Bot

Execute the bot:

```bash
python state_bot.py
```

The bot will:
- Load state from `state.json` on startup
- Synchronize with broker to verify actual positions
- Save state after every trade
- Restore state correctly after restarts

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Synchronize with Broker** | Always verify state.json matches broker reality on startup |
| **Save State After Trades** | Update state.json immediately after order execution |
| **Handle Missing State** | Create default state if state.json doesn't exist (first run) |
| **Atomic Writes** | Write state.json atomically to prevent corruption during crashes |
| **State Validation** | Verify state.json structure and values are valid before using |

## Conclusion

You've successfully learned how to implement persistent state management! Your bot now has a memory that survives restarts, preventing dangerous double-positions and ensuring proper risk management. This is essential for production-ready bots that run 24/7. In the next lesson, you'll learn how to send real-time notifications to Discord so you're always informed about your bot's activity.
