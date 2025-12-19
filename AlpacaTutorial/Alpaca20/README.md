# Lesson 20: **The Bigger Picture – Analyzing Multiple Timeframes**

Welcome to Lesson 20 of the Alpaca Trading Course! This advanced lesson teaches you one of the most powerful techniques used by professional traders: Multi-Timeframe Analysis. You will build a bot that first identifies the primary trend on a high timeframe (the Daily chart) and then looks for precise entry points on a lower timeframe (the Hourly chart).

## The Problem: Trading on a Single Timeframe

Trading on a single timeframe is like navigating with only a compass. You know your immediate direction, but you can't see the overall landscape. You might be buying in what looks like a small uptrend on the hourly chart, while completely ignoring that you're in the middle of a massive, long-term downtrend on the daily chart.

| Problem/Challenge | Description |
|---|---|
| **No Context** | Single timeframe doesn't show the bigger picture trend |
| **Low-Probability Trades** | May trade against the "main current" of the market |
| **Poor Entry Timing** | Cannot distinguish between pullbacks and reversals |
| **Reduced Win Rate** | Trading against the primary trend significantly reduces success rate |

## The Solution: Multi-Timeframe Analysis (Top-Down Approach)

The solution is to use a "top-down" approach: first identify the dominant trend on a higher timeframe, then use a lower timeframe to find the optimal entry point within that trend. Our bot uses Daily charts (50-day SMA) to establish the primary trend direction, then uses Hourly charts (14-period RSI) to find precise entry points during pullbacks.

### Step 20.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 20.2: Configure Your API Keys

Copy the example config file and add your Alpaca Paper Trading API keys:

```bash
copy config.example.py config.py
```

⚠️ **Never commit your `config.py` file!**

### Step 20.3: Run the Multi-Timeframe Bot

Execute the bot:

```bash
python mtf_bot.py
```

**Strategy Logic:**
- **Higher Timeframe (Daily) - The Gatekeeper**: If Price > 50-day SMA → Primary trend is UP (proceed). If Price < 50-day SMA → Primary trend is DOWN (no trades allowed).
- **Lower Timeframe (Hourly) - The Entry Signal**: Wait for RSI to cross above 30 (oversold recovery) for entry timing.
- **Trading Mantra**: "Trade with the trend, enter on the pullback."

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Gatekeeper Pattern** | Higher timeframe acts as a filter - only trade in direction of primary trend |
| **Separate Data Fetches** | Make distinct API calls for daily and hourly timeframes |
| **Trend is Your Friend** | Trading with the primary trend dramatically increases win rate |
| **Enter on Pullbacks** | Use lower timeframe to find optimal entry points within the trend |
| **Context is Everything** | Understanding both big picture and precise timing improves trade quality |

## Conclusion

You've successfully learned multi-timeframe analysis, a professional trading technique! This approach provides both context (the big picture trend) and precision (optimal entry timing). By using higher timeframes for direction and lower timeframes for timing, you dramatically improve your win rate and trade quality. This is how professional traders analyze markets. In the next lesson, you'll learn about logging and creating an audit trail of all trading decisions.
