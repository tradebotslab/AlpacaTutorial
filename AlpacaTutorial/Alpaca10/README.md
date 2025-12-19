# Lesson 10: **Moving Average Crossover Strategy - Complete Bot**

Welcome to Lesson 10 of the Alpaca Trading Course! This lesson combines all the components from previous lessons into a single, functioning trading system. You'll build a complete automated trading bot that implements a Golden Cross / Death Cross strategy using Simple Moving Averages (SMA).

## The Problem: Fragmented Trading Components

In previous lessons, you've learned individual components (API connection, data fetching, indicators, signals, orders), but they exist as separate scripts. Without integrating them into a cohesive system, you cannot build a fully automated trading bot that runs continuously and makes trading decisions autonomously.

| Problem/Challenge | Description |
|---|---|
| **Disconnected Components** | Individual scripts cannot work together as a unified trading system |
| **No Continuous Operation** | Cannot run a bot that continuously monitors markets and executes trades |
| **Manual Intervention Required** | Need to manually run different scripts for different tasks |
| **No Complete Strategy** | Missing the integration of all components into a single, working bot |

## The Solution: Build a Complete Integrated Trading Bot

The solution is to integrate all components into a single bot that combines: a main loop for continuous operation, position management to track holdings, technical analysis to calculate SMAs, signal detection to identify crossovers, and order execution to automatically place trades.

### Step 10.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 10.2: Configure API Credentials

1. Clone this repository or navigate to the Alpaca10 folder
2. Copy the example config file:
   ```bash
   cp config.py.example config.py
   ```
3. Edit `config.py` and add your API keys:
   ```python
   API_KEY = "your_key_here"
   SECRET_KEY = "your_secret_here"
   ```

### Step 10.3: Run the Complete Trading Bot

Execute the bot:

```bash
python crossover_bot_final.py
```

The bot will:
- Start and display configuration information
- Check for existing positions
- Fetch market data every 5 minutes
- Calculate moving averages
- Detect crossover signals
- Place orders automatically when signals are detected

**To stop the bot**: Press `Ctrl+C`

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Position Management** | Always check for existing positions before placing new orders |
| **Main Loop Structure** | Use appropriate sleep intervals (5 minutes is reasonable for daily data) |
| **Error Handling** | Implement robust error handling so the bot continues running even if one iteration fails |
| **Signal Confirmation** | Golden Cross and Death Cross are rare; the bot may wait days or weeks for signals |
| **Paper Trading** | Always test thoroughly in paper trading before considering live trading |

## Conclusion

Congratulations! You've built a complete, automated trading bot that combines all the components you've learned: API connection, data fetching, technical indicators, signal detection, and order execution. This bot runs continuously, monitors the market, and executes trades automatically based on moving average crossovers. This is a significant achievement - you now have a fully functional algorithmic trading system. In future lessons, you'll learn about risk management, stop-losses, and more advanced trading concepts.
