# Lesson 30: **A Step Towards PRO – Statistical Arbitrage (Pairs Trading)**

Welcome to Lesson 30 of the Alpaca Trading Course! This final lesson teaches you about pairs trading, a market-neutral statistical arbitrage strategy used by professional quantitative traders. Unlike directional strategies that bet on market direction, pairs trading profits from temporary distortions in the price relationship between two highly correlated assets.

## The Problem: Directional Trading Limitations

Directional strategies (like moving average crossovers) have a fundamental weakness: if you predict the market's direction incorrectly, you lose money. If the market goes sideways for months, you make no money. Your profitability is entirely dependent on being right about the market's future direction.

| Problem/Challenge | Description |
|---|---|
| **Market Direction Dependency** | Profitability depends entirely on correctly predicting market direction |
| **Sideways Market Losses** | Cannot profit when markets don't trend |
| **High Risk** | Wrong direction prediction results in losses |
| **Limited Strategy Options** | Only profitable in trending markets |

## The Solution: Market-Neutral Pairs Trading

The solution is pairs trading - a market-neutral strategy that doesn't care if the overall market is bullish or bearish. Instead, it profits from temporary distortions in the price relationship between two highly correlated assets. Key benefits: market neutrality (profit from relative performance, not market direction), reduced risk (losses on one position are buffered by gains on the other), statistical foundation (based on quantitative analysis, not gut feelings), and works in sideways markets (can profit even when markets don't trend).

### Step 30.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `alpaca-py` - Alpaca API client
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `statsmodels` - Statistical analysis (cointegration tests)

### Step 30.2: Configure Your API Credentials

Copy the example configuration:

```bash
copy config.example.py config.py
```

Edit `config.py` with your Alpaca API credentials.

⚠️ **IMPORTANT:** Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview

### Step 30.3: Run the Pairs Trading Bot

Execute the bot:

```bash
python pairs_trading_bot.py
```

The bot will:
1. Fetch historical data for both assets
2. Test for cointegration (statistical relationship)
3. Calculate current spread and Z-score
4. Generate trading signals
5. Execute pairs trades when appropriate

**Trading Logic:**
- **Enter Long Spread** when Z-score < -2 (spread is too narrow, will widen)
- **Enter Short Spread** when Z-score > +2 (spread is too wide, will narrow)
- **Exit** when Z-score returns to near 0 (spread has reverted to mean)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Cointegration Testing** | Only trade pairs that are statistically cointegrated (p-value < 0.05) |
| **Z-Score Thresholds** | Enter when |Z| > 2, exit when |Z| < 0.5 (adjustable) |
| **Simultaneous Execution** | Both legs must execute together to maintain market neutrality |
| **Regular Re-Testing** | Cointegration can break down; re-test relationship periodically |
| **Capital Requirements** | Pairs trading requires capital for both positions (long and short) |

## Conclusion

Congratulations on completing the Alpaca Trading Course! You've learned pairs trading, an advanced market-neutral strategy used by professional quantitative traders. You now have the skills to build complete trading systems, manage risk, backtest strategies, deploy to production, and implement both directional and market-neutral strategies. The world of quantitative finance is vast - continue learning, experimenting, and building!
