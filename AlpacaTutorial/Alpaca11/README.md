# Lesson 11: **Bracket Orders - Stop-Loss & Take-Profit**

Welcome to Lesson 11 of the Alpaca Trading Course! This lesson teaches you one of the most critical aspects of risk management: how to automatically protect your trades using bracket orders. You'll learn how to set stop-loss orders to limit potential losses and take-profit orders to lock in gains.

## The Problem: Unprotected Trades

Without automatic stop-loss and take-profit orders, your trades are exposed to unlimited risk. A winning trade can turn into a loss if you don't exit at the right time, and a losing trade can wipe out significant capital if not stopped out.

| Problem/Challenge | Description |
|---|---|
| **Unlimited Loss Risk** | Without stop-losses, a single bad trade can destroy your account |
| **Profit Erosion** | Winning trades can reverse and turn into losses if not exited at the right time |
| **Emotional Decision Making** | Manual exit decisions are influenced by fear and greed |
| **No Risk Management** | Cannot systematically limit losses or secure profits |

## The Solution: Bracket Orders for Automatic Risk Management

The solution is to use bracket orders, which combine three orders into one: your entry order, a take-profit order (automatically sells at +5% profit), and a stop-loss order (automatically sells at -2% loss). When one exit order triggers, the other is automatically canceled (One-Cancels-Other).

### Step 11.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 11.2: Configure Your API Keys

Copy the example config file and add your Alpaca Paper Trading API keys:

```bash
copy config.example.py config.py
```

Then edit `config.py`:
```python
API_KEY = "YOUR_PAPER_TRADING_API_KEY"
SECRET_KEY = "YOUR_PAPER_TRADING_SECRET_KEY"
BASE_URL = "https://paper-api.alpaca.markets"
```

⚠️ **Never commit your `config.py` file!** It's already in `.gitignore`.

### Step 11.3: Run the Bracket Order Bot

Execute the bot:

```bash
python bracket_bot.py
```

The bot uses a Golden Cross strategy with automatic risk management:
- **Entry**: Market buy order when 20-day SMA crosses above 50-day SMA
- **Take-Profit**: +5% above entry price
- **Stop-Loss**: -2% below entry price

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Risk/Reward Ratio** | Default is 2.5:1 (risk $2 to make $5) - a professional standard |
| **Stop-Loss Distance** | 2% is conservative; adjust based on stock volatility |
| **Take-Profit Targets** | 5% is reasonable for swing trading; adjust for your timeframe |
| **Position Sizing** | Combine with dynamic position sizing (Lesson 13) for best results |
| **Paper Trading First** | Always test bracket orders in paper trading before live trading |

## Conclusion

You've successfully learned how to implement bracket orders for automatic risk management! This is a critical skill that protects your capital and locks in profits automatically. Bracket orders ensure you never forget to set a stop-loss and never let winning trades turn into losers. In the next lesson, you'll dive deeper into take-profit strategies and learn how to optimize your profit targets.
