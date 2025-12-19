# Lesson 19: **Signal Confirmation – Combining Two Indicators**

Welcome to Lesson 19 of the Alpaca Trading Course! This lesson teaches you how to build more robust trading strategies by combining two different types of indicators to confirm trading signals before entering positions. You'll learn why single indicators can produce false signals and how confirmation improves trade quality.

## The Problem: False Signals from Single Indicators

Single indicators can be misleading. RSI might signal oversold conditions, but the price continues falling in a strong downtrend. MACD might show a bullish crossover, but it could be a weak move that quickly reverses. Without confirmation, you risk entering trades based on unreliable signals.

| Problem/Challenge | Description |
|---|---|
| **False Signals** | Single indicators can generate misleading buy/sell signals |
| **Weak Confirmation** | No way to verify signals with additional analysis |
| **Poor Trade Quality** | Entering trades on unconfirmed signals leads to losses |
| **No Signal Validation** | Cannot distinguish between strong and weak signals |

## The Solution: Multi-Indicator Confirmation

The solution is to require confirmation from multiple indicators before taking action. This is like getting a "second opinion" from a different type of analysis. We combine RSI (momentum oscillator) and MACD (trend indicator) so that both must agree before entering a trade.

### Step 19.1: Install Required Packages

Install the required packages:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `alpaca-trade-api` - For connecting to Alpaca
- `pandas` - For data manipulation
- `pandas-ta` - For technical indicator calculations

### Step 19.2: Configure Your API Keys

1. Copy the example config:
   ```bash
   cp config.example.py config.py
   ```

2. Edit `config.py` with your Alpaca API credentials:
   ```python
   API_KEY = "your_alpaca_api_key_here"
   SECRET_KEY = "your_alpaca_secret_key_here"
   BASE_URL = "https://paper-api.alpaca.markets"
   ```

3. Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

⚠️ **IMPORTANT:** Never commit `config.py` to GitHub!

### Step 19.3: Run the Confirmation Bot

Execute the bot:

```bash
python confirmation_bot.py
```

**Trading Logic:**
- **BUY Signal (High-Confidence Entry)**: Enter ONLY when BOTH conditions are true:
  1. RSI Signal: RSI crosses above 30 (exiting oversold territory)
  2. MACD Signal: MACD line crosses above signal line (bullish crossover)
- **SELL Signal**: Exit when MACD shows bearish crossover (MACD line crosses below signal line)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Require Both Signals** | Use `and` operator to ensure both indicators agree before trading |
| **Reduce False Signals** | Multi-indicator confirmation significantly reduces false signals |
| **Complementary Indicators** | Combine different indicator types (momentum + trend) for best results |
| **Trade Quality Over Quantity** | Fewer, higher-quality trades are better than many low-quality trades |
| **Patience Required** | Confirmed signals are rarer but more reliable |

## Conclusion

You've successfully learned how to combine multiple indicators for signal confirmation! This approach significantly improves trade quality by requiring agreement from different types of analysis. Multi-indicator confirmation reduces false signals and increases the probability of successful trades. In the next lesson, you'll learn about multi-timeframe analysis, which uses different timeframes to identify trends and entry points.
