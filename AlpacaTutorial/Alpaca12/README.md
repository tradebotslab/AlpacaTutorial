# Lesson 12: **Take Your Profits! – Setting a Take-Profit Order**

Welcome to Lesson 12 of the Alpaca Trading Course! This lesson focuses on the offensive side of risk management: setting automatic take-profit orders. While stop-losses protect you from losses, take-profit orders ensure you don't let winning trades turn into losers.

## The Problem: Letting Profits Slip Away

Markets are volatile. A stock that hits your profit goal can quickly reverse, turning a winning trade into a loss. Without automatic take-profit orders, you might hold positions too long, hoping for more gains, only to watch profits disappear.

| Problem/Challenge | Description |
|---|---|
| **Profit Erosion** | Winning trades can reverse and turn into losses if not exited |
| **Greed-Driven Decisions** | Manual profit-taking is influenced by emotions ("just a little more") |
| **No Systematic Exits** | Cannot automatically lock in gains at predetermined levels |
| **Missed Opportunities** | Holding too long prevents capital from being deployed in new opportunities |

## The Solution: Automatic Take-Profit Orders

The solution is to set take-profit orders that automatically sell your shares when the price reaches your target. A take-profit is a limit order that executes when your profit goal is reached, removing emotion from the exit decision.

### Step 12.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 12.2: Configure Your API Keys

Copy the example config file:

```bash
copy config.example.py config.py
```

Then edit `config.py` and add your Alpaca Paper Trading API keys.

⚠️ **Never commit your `config.py` file!**

### Step 12.3: Run the Take-Profit Bot

Execute the bot:

```bash
python bracket_bot.py
```

The bot implements a complete risk-managed strategy:
- **Entry Signal**: Golden Cross (20-day SMA crosses above 50-day SMA)
- **Take-Profit**: +5% above entry price (your profit goal)
- **Stop-Loss**: -2% below entry price (your safety net)
- **Risk/Reward Ratio**: 2.5:1 (risk $2 to make $5)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Risk/Reward Ratios** | 2:1 minimum, 2.5:1 balanced, 3:1 aggressive - always risk less than potential reward |
| **Profit Target Calculation** | Take-profit price = Entry price × (1 + profit_percentage / 100) |
| **Discipline Over Greed** | Automated exits remove emotion and ensure consistent profit-taking |
| **Combine with Stop-Loss** | Always use both take-profit and stop-loss for complete risk management |
| **Adjust for Timeframe** | Shorter timeframes may need tighter targets; longer timeframes can aim higher |

## Conclusion

You've successfully learned how to implement take-profit orders! This completes the offensive side of risk management. Combined with stop-losses, you now have a complete exit strategy that automatically protects your capital and secures your profits. The best traders protect their capital AND secure their profits. In the next lesson, you'll learn about dynamic position sizing, which ensures you risk the same percentage of capital on every trade.
