# Tutorial 8: Moving Average Crossover Detector

This project implements a simple trading signal detector that identifies moving average crossovers using the Alpaca API.

## Overview

A moving average crossover occurs when a shorter-term Simple Moving Average (SMA) crosses over a longer-term SMA. This event is often interpreted by traders as a signal that the trend may be changing.

### Signal Types

- **Golden Cross (Bullish Signal)**: The short-term SMA (20-day) crosses above the long-term SMA (50-day). This can indicate that price momentum is shifting upwards, and is often seen as a signal to buy.

- **Death Cross (Bearish Signal)**: The short-term SMA (20-day) crosses below the long-term SMA (50-day). This can indicate that price momentum is shifting downwards, and is often seen as a signal to sell.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your Alpaca API credentials:
   - Copy `config.py` and add your API keys
   - Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
   - **Important**: Never commit `config.py` to version control

3. Run the script:
```bash
python crossover_detector.py
```

## How It Works

The script:
1. Fetches the last 51 days of price data for a symbol (default: AAPL)
2. Calculates 20-day and 50-day Simple Moving Averages
3. Compares the relationship between SMAs on the previous day vs the current day
4. Detects if a crossover occurred (Golden Cross or Death Cross)
5. Prints the signal result

## Project Structure

```
├── crossover_detector.py  # Main script
├── config.py              # API credentials (not in git)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── instructions.md       # Tutorial instructions
└── .gitignore           # Git ignore rules
```

## Safety

- This script uses the **paper trading environment** by default
- All API calls are wrapped in try/except blocks for error handling
- API keys are stored separately in `config.py` (excluded from git)

## License

Educational project for learning algorithmic trading concepts.
