# Lesson 2: **"Hello, Alpaca!" - Connect & Check Your Account Status**

Welcome to Lesson 2 of the Alpaca Trading Course! This lesson demonstrates how to connect to the Alpaca API and retrieve basic information about your paper trading account, such as your current equity and buying power. This is your first hands-on experience writing code that interacts with a real trading platform.

## The Problem: No Way to Programmatically Check Account Status

Without the ability to connect to Alpaca's API, you cannot programmatically check your account status, verify your connection, or retrieve account information like equity, buying power, or cash balance. You would be limited to manually checking the web dashboard.

| Problem/Challenge | Description |
|---|---|
| **No Programmatic Connection** | Cannot verify API keys work or check account status through code |
| **Manual Verification Required** | Must manually log into the web dashboard to check account information |
| **No Automation Foundation** | Cannot build automated trading systems without the ability to connect to the API |
| **Unclear Account State** | Cannot programmatically determine available buying power or account equity |

## The Solution: Connect to Alpaca API Using Python SDK

The solution is to use the Alpaca Python SDK (`alpaca-trade-api`) to establish a connection to Alpaca's API using your API keys. This allows you to programmatically retrieve account information, verify your connection, and build the foundation for automated trading.

### Step 2.1: Install Required Dependencies

Open your terminal and navigate to the project directory, then install the required packages:

```bash
cd path/to/Alpaca02
pip install -r requirements.txt
```

This installs:
- `alpaca-trade-api` - Official Alpaca Python SDK for trading
- `pandas` - Data manipulation library (used by alpaca-trade-api)

### Step 2.2: Configure Your API Keys

1. Open the `config.py` file in your code editor
2. Replace the placeholder values with your actual Alpaca API keys:
   ```python
   API_KEY = "YOUR_PAPER_API_KEY_HERE"  # Replace with your actual API key
   SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"  # Replace with your actual secret key
   ```
3. Ensure `BASE_URL` is set to `https://paper-api.alpaca.markets` for paper trading

⚠️ **Important:** Never share your API keys publicly or commit `config.py` to version control.

### Step 2.3: Run Your First Connection Script

Execute the script to connect to Alpaca and display your account information:

```bash
python hello_alpaca.py
```

If everything is configured correctly, you should see output showing your account status, current equity, buying power, cash, and portfolio value.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Always Use Paper Trading** | Use paper trading keys during development and testing to avoid accidental real trades |
| **Verify Connection First** | Always test your API connection before building more complex trading logic |
| **Handle Errors Gracefully** | Wrap API calls in try-except blocks to handle connection errors and API issues |
| **Check Market Hours** | Be aware that some API calls may behave differently when markets are closed |
| **Protect Your Keys** | Never commit API keys to version control or share them publicly |

## Conclusion

You've successfully connected to the Alpaca API and retrieved your account information programmatically! This is the foundation for all future trading bot development. You now understand how to authenticate with Alpaca and retrieve account data. In the next lesson, you'll learn how to fetch historical market data, which is essential for building trading strategies.
