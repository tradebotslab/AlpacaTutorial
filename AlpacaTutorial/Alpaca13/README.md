# Lesson 13: **Never Risk Too Much – Calculating Position Size**

Welcome to Lesson 13 of the Alpaca Trading Course! This lesson teaches you the single most important rule of money management: position sizing. You'll learn how to dynamically calculate the number of shares to buy to ensure that you only risk a small, fixed percentage of your total capital on any single trade.

## The Problem: Inconsistent Risk Across Trades

Trading a fixed number of shares (e.g., always buying 10 shares) is fundamentally flawed. Risking 10 shares of a $20 stock is NOT the same as risking 10 shares of a $500 stock. Without proper position sizing, you risk inconsistent amounts of capital on each trade, making it impossible to manage risk systematically.

| Problem/Challenge | Description |
|---|---|
| **Inconsistent Risk** | Fixed quantity trading means different dollar risk on each trade |
| **Account Destruction Risk** | One bad trade on an expensive stock can wipe out your account |
| **No Standardization** | Cannot ensure consistent risk percentage across all trades |
| **Unprofessional Approach** | Professional traders always risk the same percentage per trade |

## The Solution: Dynamic Position Sizing Based on Risk Percentage

The solution is to calculate position size dynamically so that you risk the same percentage of your capital on every trade, regardless of the stock price. This involves: (1) defining your max risk per trade (typically 1-2%), (2) calculating your risk amount in dollars, (3) determining risk per share (entry price - stop-loss price), and (4) calculating shares to buy (risk amount ÷ risk per share).

### Step 13.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 13.2: Configure Your API Keys

Copy the example config file and add your Alpaca Paper Trading API keys:

```bash
copy config.example.py config.py
```

⚠️ **Never commit your `config.py` file!**

### Step 13.3: Run the Dynamic Position Sizing Bot

Execute the bot:

```bash
python dynamic_sizing_bot.py
```

The bot implements professional-grade risk management:
- **Entry Signal**: Golden Cross (20-day SMA crosses above 50-day SMA)
- **Position Sizing**: Dynamic calculation based on 1% risk
- **Take-Profit**: +3% above entry price (3:1 reward-to-risk ratio)
- **Stop-Loss**: -1% below entry price (risk control)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Risk Percentage** | Professionals use 1-2% per trade maximum; never risk more than 2% |
| **Position Size Formula** | Shares = (Account Equity × Risk %) ÷ (Entry Price - Stop-Loss Price) |
| **Account Protection** | Dynamic sizing makes account blow-up mathematically impossible |
| **Consistent Risk** | Every trade risks the same percentage, regardless of stock price |
| **Adapts Automatically** | Position size adjusts to account growth and stock price changes |

## Conclusion

You've successfully learned dynamic position sizing, the foundation of professional risk management! This ensures you risk the same percentage of capital on every trade, making your account blow-up mathematically impossible. Position sizing is what separates amateurs from professionals. In the next lesson, you'll learn about trailing stop-losses, which protect your profits as trades move in your favor.
