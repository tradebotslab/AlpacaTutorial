# Alpaca Trading Course - Tutorial 6: Anatomy of a Bot - The Main Loop

This tutorial demonstrates the core component of any automated trading bot: the main loop. You will learn how to build a simple, infinite loop that serves as the bot's "heartbeat," allowing it to perform actions at regular, controlled intervals.

## What is a Main Loop?

Every automated bot needs a core engine that runs continuously. This is the main loop - an infinite loop that:

- Wakes up at a set interval
- Performs a series of tasks (e.g., checks the market, analyzes data, looks for a trade signal)
- Goes back to sleep for a set period
- Repeats this cycle indefinitely until you stop it

This structure allows your bot to operate autonomously 24/7 without any manual intervention.

## Project Structure

```
Alpaca06/
├── config.py              # API credentials (not included in repo - see setup below)
├── config.py.template     # Template for config.py
├── main_loop_bot.py       # Main bot script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── instructions.md       # Detailed tutorial instructions
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

1. Copy `config.py.template` to `config.py`:
   ```bash
   cp config.py.template config.py
   ```
   On Windows:
   ```powershell
   Copy-Item config.py.template config.py
   ```

2. Edit `config.py` and add your Alpaca API credentials:
   - Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
   - Replace `YOUR_API_KEY_HERE` and `YOUR_SECRET_KEY_HERE` with your actual keys

**Important:** The `config.py` file is excluded from git to protect your API keys. Never commit this file!

### 3. Run the Bot

```bash
python main_loop_bot.py
```

The bot will:
- Start and display "Bot is starting..."
- Every 60 seconds, check your account status and buying power
- Continue running until you stop it

### 4. Stop the Bot

Press `Ctrl+C` in your terminal to gracefully stop the bot. You will see the message "Bot is shutting down. Goodbye!"

## How It Works

### The Main Loop

The core of the bot is an infinite `while True:` loop that:
1. Gets the current timestamp
2. Fetches account information from Alpaca API
3. Displays account status and buying power
4. Sleeps for 60 seconds before the next iteration

### Error Handling

All API calls are wrapped in `try...except` blocks to ensure the bot continues running even if one iteration fails. If an error occurs, the bot logs it and waits 30 seconds before retrying.

### Rate Limiting

The `time.sleep(60)` command is critical - without it, the loop would run thousands of times per second, overwhelming your computer and spamming the Alpaca API, which would result in rate limiting.

## Security Notes

- **Never commit `config.py`** - It contains your API keys and is excluded via `.gitignore`
- **Always use paper trading** - The default `BASE_URL` points to the paper trading environment for safety
- **Keep your keys secure** - Treat your API keys like passwords

## Next Steps

In future tutorials, you'll learn how to:
- Fetch market data inside the main loop
- Calculate technical indicators
- Implement trading strategies
- Place orders based on signals

## License

This is an educational project for learning automated trading with Alpaca.

