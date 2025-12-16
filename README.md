# Alpaca Trading Bot - Tutorial 9

## Simple Exit Logic – Selling on a Reversal Signal

This tutorial implements a complete moving average crossover trading bot with both entry and exit logic.

## Strategy Overview

- **Entry Signal (Golden Cross)**: Buy when the short-term SMA (20-day) crosses above the long-term SMA (50-day)
- **Exit Signal (Death Cross)**: Sell when the short-term SMA (20-day) crosses below the long-term SMA (50-day)

## Project Structure

```
Alpaca09/
├── config.py              # API credentials (NOT in git)
├── crossover_bot_v1.py   # Main bot script
├── requirements.txt       # Python dependencies
├── instructions.md        # Tutorial instructions
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys**
   - Copy `config.py` and add your Alpaca API credentials
   - Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
   - The bot uses paper trading by default (configured in `config.py`)

3. **Run the Bot**
   ```bash
   python crossover_bot_v1.py
   ```

## Features

- ✅ Position checking before trading
- ✅ Golden Cross entry detection
- ✅ Death Cross exit detection
- ✅ Error handling for API calls
- ✅ Paper trading environment by default
- ✅ Graceful shutdown with Ctrl+C

## Important Notes

- **This bot uses paper trading by default** - no real money is at risk
- **API keys are stored in `config.py`** - this file is excluded from version control
- The bot checks for signals every 5 minutes
- The bot uses daily bar data for SMA calculations

## Code Philosophy

This code follows educational principles:
- Clear, descriptive variable names
- Comments explain "WHY", not "WHAT"
- One action per line
- Explicit error handling
- Functions with single responsibility

## License

Educational project for learning algorithmic trading with Alpaca API.

