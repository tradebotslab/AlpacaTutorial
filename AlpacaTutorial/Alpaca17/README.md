# Lesson 17: **The Magic of Volatility – A Bollinger Bands® Bot**

Welcome to Lesson 17 of the Alpaca Trading Course! This lesson teaches you how to build an advanced trading bot that capitalizes on volatility changes using Bollinger Bands®. You'll implement a powerful "squeeze breakout" strategy that aims to catch explosive price moves right as they begin.

## The Problem: No Way to Measure and Trade Volatility

Without tools to measure volatility, you cannot identify consolidation periods (low volatility) that often precede significant price moves, or detect when volatility is expanding (breakouts). You need a way to measure volatility and trade based on volatility changes.

| Problem/Challenge | Description |
|---|---|
| **No Volatility Measurement** | Cannot identify when markets are consolidating or breaking out |
| **Missed Breakout Opportunities** | Cannot systematically catch explosive price moves as they begin |
| **No Consolidation Detection** | Cannot identify "squeeze" periods that often precede big moves |
| **Limited Strategy Diversity** | Only price-based strategies without volatility analysis |

## The Solution: Bollinger Bands® for Volatility Trading

The solution is to use Bollinger Bands®, a volatility indicator consisting of three lines: a middle band (SMA), an upper band (SMA + 2 standard deviations), and a lower band (SMA - 2 standard deviations). When bands narrow (squeeze), it indicates low volatility and potential breakout incoming. When bands widen, it indicates high volatility and strong trending moves.

### Step 17.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `alpaca-trade-api` - For executing trades
- `pandas` - For data manipulation
- `pandas-ta` - For technical indicators

### Step 17.2: Configure Your API Keys

1. Copy the example configuration:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` with your API credentials:
   ```python
   API_KEY = "your_actual_api_key_here"
   SECRET_KEY = "your_actual_secret_key_here"
   BASE_URL = "https://paper-api.alpaca.markets"
   ```

⚠️ **IMPORTANT**: Never commit `config.py` to Git!

### Step 17.3: Run the Bollinger Bands Bot

Execute the bot:

```bash
python bollinger_bot.py
```

**Strategy Logic:**
- **Entry Signal (BUY)**: Previous bar showed low volatility (bandwidth < threshold) AND current price breaks above the upper band
- **Exit Signal (SELL)**: Price reverts below the middle band (mean reversion)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Squeeze Detection** | Look for periods when bands narrow significantly (low bandwidth) |
| **Breakout Confirmation** | Wait for price to break above upper band after squeeze for entry |
| **Mean Reversion Exit** | Exit when price returns to middle band to lock in profits |
| **Volatility Cycles** | Markets alternate between low volatility (squeeze) and high volatility (expansion) |
| **False Breakouts** | Not all breakouts succeed; use stop-losses to protect against failed breakouts |

## Conclusion

You've successfully built a Bollinger Bands® volatility trading bot! This strategy capitalizes on the natural cycle of volatility: periods of consolidation (squeeze) followed by explosive moves (breakouts). Bollinger Bands help you identify these opportunities and trade them systematically. In the next lesson, you'll learn about MACD (Moving Average Convergence Divergence) for momentum-based trading strategies.
