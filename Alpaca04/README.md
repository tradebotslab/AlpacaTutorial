# Tutorial 4: Place Market Order

This tutorial demonstrates how to place a MARKET order to buy or sell a stock using the Alpaca Trading API.

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Completed Tutorial 2**: You must have a working `config.py` file with your API keys
- **Python 3.8 or higher** (Python 3.10+ recommended)
- **An Alpaca Paper Trading Account**
- **Alpaca API Keys** (Paper Trading)

⚠️ **VERY IMPORTANT!** Use your Alpaca Paper Trading Account to test this script. Running it on a Live Account will execute a real trade with real money.

## 🚀 Installation Steps

### Step 1: Install Python Dependencies

Open your terminal or command prompt and navigate to the project directory:

```bash
cd path/to/Alpaca04
```

Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install:
- `alpaca-trade-api` - Official Alpaca Python SDK for trading
- `pandas` - Data manipulation library (used by alpaca-trade-api)

## ⚙️ Configuration

### Step 2: Configure Your API Keys

1. Create a `config.py` file in the `Alpaca04` folder (if you haven't already)
2. Add your Alpaca API credentials:

   ```python
   API_KEY = "YOUR_PAPER_API_KEY_HERE"
   SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"
   BASE_URL = "https://paper-api.alpaca.markets"
   ```

3. **Important Security Notes:**
   - Never share your API keys publicly
   - Never commit `config.py` to version control (it should be in `.gitignore`)
   - The `BASE_URL` should remain as `https://paper-api.alpaca.markets` for paper trading

## ▶️ Running the Program

### Step 3: Execute the Script

Once your API keys are configured, run the script:

```bash
python place_order.py
```

### Expected Output

If everything is configured correctly and the market is open, you should see output similar to this:

```
Placing a buy order for 1 share(s) of AAPL...
Order was placed successfully!
Order ID: 12345678-1234-1234-1234-123456789abc
Symbol: AAPL
Quantity: 1
Status: filled
```

If the market is closed, you'll see:

```
The market is currently closed. Cannot place orders.
```

## 📊 Understanding the Code

### What This Script Does

1. **Checks Market Status**: Verifies that the market is open before attempting to place an order
2. **Places Market Order**: Executes a buy or sell order at the current market price
3. **Displays Confirmation**: Shows order details including Order ID, Symbol, Quantity, and Status

### Order Parameters

- **Symbol**: Stock to trade (default: "AAPL")
- **Quantity**: Number of shares (default: 1)
- **Side**: 'buy' to purchase, 'sell' to sell
- **Type**: 'market' - executes immediately at best available price
- **Time in Force**: 'day' - order valid until end of trading day

### Key Concepts

**Market Orders**: A market order executes immediately at the best price currently available on the market. It's the simplest type of order.

**Time in Force**: Specifies how long the order should remain active if not immediately filled. 'day' means the order is valid for the current trading day only. Another popular option is 'gtc' (Good 'til Canceled).

**Order Status**: The initial status of a market order will typically be `accepted` or `pending_new`, and then it will very quickly change to `filled` if there is liquidity in the market.

## 🐛 Troubleshooting

### Error: `The market is currently closed. Cannot place orders.`

**Solution:** This is expected behavior. Market orders can only be placed during market hours (typically 9:30 AM - 4:00 PM ET, Monday-Friday). Wait until the market opens or modify the script to handle this case differently.

### Error: `An error occurred while placing the order: 401 Client Error: Unauthorized`

**Possible causes:**
- Invalid API keys in `config.py`
- API keys are for Live Trading instead of Paper Trading
- API keys have been revoked or expired

**Solution:**
1. Double-check your API keys in `config.py`
2. Verify you're using Paper Trading keys (not Live Trading)
3. Generate new API keys from your Alpaca dashboard if necessary

### Error: `An error occurred while placing the order: Insufficient buying power`

**Solution:** Your paper trading account doesn't have enough buying power to execute the order. Check your account balance in the Alpaca dashboard.

### Error: `An error occurred while placing the order: Invalid symbol`

**Solution:** The stock symbol you're trying to trade doesn't exist or isn't available for trading. Verify the symbol is correct (e.g., "AAPL" for Apple, "MSFT" for Microsoft).

## 📁 Project Structure

```
Alpaca04/
│
├── config.py              # API keys configuration (DO NOT SHARE THIS FILE)
├── place_order.py         # Main script
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
└── instructions.md        # Detailed tutorial instructions
```

## 🔒 Security Reminders

- ⚠️ **Never commit `config.py` to Git** - Add it to `.gitignore`
- ⚠️ **Never share your API keys** publicly or in screenshots
- ⚠️ **Use Paper Trading keys** for tutorials (not Live Trading)
- ⚠️ **Rotate your keys** if you suspect they've been compromised

## 📚 Learning Objectives

- Understanding market orders
- Checking market status before trading
- Placing orders through the Alpaca API
- Handling order confirmations and errors

## 🎯 Next Steps

After completing this tutorial, you can:

- Modify the script to trade different stocks
- Experiment with different order types (limit orders, stop orders)
- Add more sophisticated error handling
- Implement order status tracking
- Build a portfolio management system

## 📞 Support

If you encounter issues:

1. Check the [Alpaca API Documentation](https://alpaca.markets/docs/)
2. Review the error messages for specific details
3. Ensure all prerequisites are met
4. Verify your API keys are correct

## 📝 License

This tutorial is part of an educational course on algorithmic trading with Alpaca.
