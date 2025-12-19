# Lesson 4: **Place Market Order**

Welcome to Lesson 4 of the Alpaca Trading Course! This lesson demonstrates how to place a MARKET order to buy or sell a stock using the Alpaca Trading API. This is your first step toward executing trades programmatically.

## The Problem: No Way to Execute Trades Programmatically

Without the ability to place orders through the API, you cannot automate trading decisions or execute trades based on your trading strategies. You would be limited to manual trading through the web interface, which defeats the purpose of algorithmic trading.

| Problem/Challenge | Description |
|---|---|
| **No Automated Execution** | Cannot execute trades automatically based on trading signals or strategies |
| **Manual Trading Required** | Must manually place orders through web interface, which is slow and error-prone |
| **No Strategy Implementation** | Cannot implement algorithmic trading strategies that require automatic order placement |
| **Missed Opportunities** | Cannot react quickly to market conditions or trading signals |

## The Solution: Place Market Orders Using Alpaca Trading API

The solution is to use Alpaca's Trading API to place market orders programmatically. A market order executes immediately at the best price currently available on the market. This allows you to automate trade execution based on your trading logic and strategies.

### Step 4.1: Install Required Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `alpaca-trade-api` - Official Alpaca Python SDK for trading
- `pandas` - Data manipulation library

### Step 4.2: Configure Your API Keys

1. Create a `config.py` file in the `Alpaca04` folder (if you haven't already)
2. Add your Alpaca API credentials:
   ```python
   API_KEY = "YOUR_PAPER_API_KEY_HERE"
   SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"
   BASE_URL = "https://paper-api.alpaca.markets"
   ```

⚠️ **VERY IMPORTANT!** Use your Alpaca Paper Trading Account. Running this on a Live Account will execute a real trade with real money.

### Step 4.3: Execute the Market Order Script

Run the script to place a market order:

```bash
python place_order.py
```

The script will check if the market is open, place a market order, and display the order confirmation including Order ID, Symbol, Quantity, and Status.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Always Use Paper Trading First** | Test all order placement logic in paper trading before using real money |
| **Check Market Hours** | Market orders can only be placed during market hours (9:30 AM - 4:00 PM ET) |
| **Verify Order Status** | Always check order status after submission to confirm it was filled |
| **Handle Errors Gracefully** | Wrap order placement in try-except blocks to handle API errors and rejections |
| **Understand Order Types** | Market orders execute immediately; learn about limit orders for price control |

## Conclusion

You've successfully placed your first market order through the Alpaca API! You now understand how to execute trades programmatically, which is essential for building automated trading bots. Market orders are the simplest type of order and execute immediately at the best available price. In the next lesson, you'll learn how to check the status of your orders and view your current positions.
