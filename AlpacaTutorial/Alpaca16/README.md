# Lesson 16: **Relative Strength – Building an RSI-Based Bot**

Welcome to Lesson 16 of the Alpaca Trading Course! This lesson teaches you how to build a mean-reversion trading bot using one of the most popular momentum indicators: the Relative Strength Index (RSI). The bot identifies overbought and oversold market conditions and trades the expected price reversals.

## The Problem: No Way to Identify Overbought and Oversold Conditions

Without tools to identify when prices have moved too far in one direction, you cannot systematically trade mean-reversion strategies. You need a way to detect when an asset is overextended and likely to reverse back toward its average.

| Problem/Challenge | Description |
|---|---|
| **No Momentum Measurement** | Cannot identify when price moves are overextended |
| **Missed Reversal Opportunities** | Cannot systematically buy dips or sell rallies |
| **No Mean-Reversion Signals** | Cannot detect when price is likely to revert to average |
| **Limited Strategy Options** | Only trend-following strategies without momentum indicators |

## The Solution: RSI Indicator for Mean-Reversion Trading

The solution is to use the Relative Strength Index (RSI), a momentum oscillator that measures the speed and change of price movements. RSI oscillates between 0 and 100: RSI > 70 indicates overbought conditions (potential sell), RSI < 30 indicates oversold conditions (potential buy). The bot trades when RSI crosses these thresholds, indicating momentum shifts.

### Step 16.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `alpaca-trade-api-python` - For API connection
- `pandas` - For data manipulation
- `pandas-ta` - For technical indicator calculations

### Step 16.2: Configure Your API Keys

Copy the example config file:

```bash
copy config.example.py config.py
```

Then edit `config.py` and add your Alpaca Paper Trading API keys.

⚠️ **Never commit your `config.py` file!**

### Step 16.3: Run the RSI Bot

Execute the bot:

```bash
python rsi_bot.py
```

The bot will:
- Display account information
- Monitor BTC/USD every minute
- Print current price and RSI values
- Execute trades when RSI crossover signals occur

**Trading Logic:**
- **BUY** when RSI crosses UP from below 30 (recovery from oversold)
- **SELL** when RSI crosses DOWN from above 70 (correction from overbought)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Crossover Logic** | Trade when RSI crosses thresholds, not just when it's above/below them |
| **Mean-Reversion Strategy** | RSI works best in ranging markets; less effective in strong trends |
| **RSI Period** | 14-period is standard; shorter periods are more sensitive |
| **False Signals** | RSI can stay overbought/oversold in strong trends; use additional confirmation |
| **Timeframe Matters** | RSI on longer timeframes (daily) is more reliable than shorter (minute) |

## Conclusion

You've successfully built an RSI-based mean-reversion trading bot! RSI is a powerful tool for identifying overbought and oversold conditions and can generate profitable trading signals when prices revert to their mean. This adds a new class of strategies (mean-reversion) to your trading toolkit, complementing the trend-following strategies you've learned. In the next lesson, you'll learn about Bollinger Bands for volatility-based trading strategies.
