# Lesson 5: **What Happened to My Order? – Checking Status & Positions**

Welcome to Lesson 5 of the Alpaca Trading Course! This lesson demonstrates how to check the status of your submitted orders and view your current open positions using the Alpaca Trading API. Understanding order status and position management is crucial for building reliable trading systems.

## The Problem: No Visibility into Order Status and Positions

After placing an order, you need to know whether it was filled, rejected, or is still pending. Without the ability to check order status and view positions, you cannot track your trades, manage your portfolio, or verify that your trading bot is working correctly.

| Problem/Challenge | Description |
|---|---|
| **Unknown Order Status** | Cannot determine if an order was filled, rejected, or is still pending |
| **No Position Tracking** | Cannot see what positions you currently hold after orders are filled |
| **Uncertain Trade Execution** | Cannot verify that your trading strategy is executing trades correctly |
| **No Portfolio Management** | Cannot manage multiple positions or track your overall portfolio state |

## The Solution: Query Order Status and List Positions Using Alpaca API

The solution is to use Alpaca's API to check order status and list your current positions. This allows you to track the lifecycle of your orders (from submission to fill) and monitor your open positions in real-time.

### Step 5.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 5.2: Configure API Credentials

1. Copy `config.py.template` to `config.py`
2. Add your Alpaca API credentials to `config.py`
3. Get your credentials from: https://app.alpaca.markets/paper/dashboard/overview

### Step 5.3: Run the Status Check Script

Execute the script to check order status and view positions:

```bash
python check_status.py
```

The script will:
1. List all open orders (orders that haven't been filled or canceled)
2. Check the status of a specific order by its ID
3. Display all current open positions (stocks you own after buy orders are filled)

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Monitor Order Lifecycle** | Orders go through states: accepted → pending_new → filled/canceled |
| **Check Positions Regularly** | Verify positions match your expectations after order fills |
| **Handle Order IDs** | Save order IDs when placing orders so you can check their status later |
| **Understand Order States** | Learn the difference between filled, partially_filled, canceled, and rejected |
| **Track Position Details** | Monitor entry price, current price, and unrealized P/L for each position |

## Conclusion

You've successfully learned how to check order status and view your current positions! This is essential for building reliable trading bots that can track their trades and manage positions. Understanding the order lifecycle (from submission to fill) and being able to query your positions are fundamental skills for algorithmic trading. In the next lesson, you'll learn how to build the main loop structure that allows your bot to run continuously.
