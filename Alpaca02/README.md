# Tutorial 2: "Hello, Alpaca!" - Connect & Check Your Account Status

This tutorial demonstrates how to connect to the Alpaca API and retrieve basic information about your paper trading account, such as your current equity and buying power.

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8 or higher** (Python 3.10+ recommended)
  - Check your Python version: `python --version`
- **An Alpaca Paper Trading Account**
  - Sign up at [https://alpaca.markets](https://alpaca.markets) if you don't have one
- **Alpaca API Keys**
  - Generate your API keys from the Alpaca dashboard
  - You'll need both `API_KEY` and `SECRET_KEY`

## 🚀 Installation Steps

### Step 1: Install Python Dependencies

Open your terminal or command prompt and navigate to the project directory:

```bash
cd path/to/Alpaca02
```

Install the required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install:
- `alpaca-trade-api` - Official Alpaca Python SDK for trading
- `pandas` - Data manipulation library (used by alpaca-trade-api)

**Alternative installation method:**

If you prefer to install packages individually:

```bash
pip install alpaca-trade-api pandas
```

### Step 2: Verify Installation

To verify that the packages were installed correctly, you can test the import:

```bash
python -c "import alpaca_trade_api; print('Installation successful!')"
```

If you see "Installation successful!" without any errors, you're ready to proceed.

## ⚙️ Configuration

### Step 3: Configure Your API Keys

1. Open the `config.py` file in your code editor.

2. Replace the placeholder values with your actual Alpaca API keys:

   ```python
   API_KEY = "YOUR_PAPER_API_KEY_HERE"  # Replace with your actual API key
   SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"  # Replace with your actual secret key
   ```

3. **Important Security Notes:**
   - Never share your API keys publicly
   - Never commit `config.py` to version control (it should be in `.gitignore`)
   - The `BASE_URL` should remain as `https://paper-api.alpaca.markets` for paper trading

### Where to Find Your API Keys

1. Log in to your Alpaca account at [https://app.alpaca.markets](https://app.alpaca.markets)
2. Navigate to **"Your API Keys"** section (usually found in the dashboard or account settings)
3. Make sure you're viewing **Paper Trading** keys (not Live Trading)
4. Copy the **API Key ID** and **Secret Key**
5. Paste them into your `config.py` file

## ▶️ Running the Program

### Step 4: Execute the Script

Once your API keys are configured, run the script:

```bash
python hello_alpaca.py
```

### Expected Output

If everything is configured correctly, you should see output similar to this:

```
Connecting to Alpaca API...

==================================================
ACCOUNT SUMMARY
==================================================
Account Status: ACTIVE
Current Equity: $100,000.00
Buying Power: $200,000.00
Cash: $100,000.00
Portfolio Value: $100,000.00
==================================================

Successfully connected to Alpaca! Your account information is shown above.
```

## 📊 Understanding the Output

The script displays the following account information:

- **Account Status**: The current status of your account (typically "ACTIVE" for paper trading)
- **Current Equity**: Total value of your account (cash + positions)
- **Buying Power**: Maximum amount you can use to purchase securities
- **Cash**: Available cash in your account
- **Portfolio Value**: Total value of your portfolio

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'alpaca_trade_api'`

**Solution:** Install the required packages:
```bash
pip install -r requirements.txt
```

### Error: `Error connecting to Alpaca API: 401 Client Error: Unauthorized`

**Possible causes:**
- Invalid API keys in `config.py`
- API keys are for Live Trading instead of Paper Trading
- API keys have been revoked or expired

**Solution:**
1. Double-check your API keys in `config.py`
2. Verify you're using Paper Trading keys (not Live Trading)
3. Generate new API keys from your Alpaca dashboard if necessary

### Error: `Error connecting to Alpaca API: Connection timeout` or network errors

**Possible causes:**
- No internet connection
- Firewall blocking the connection
- Alpaca API is temporarily unavailable

**Solution:**
1. Check your internet connection
2. Verify you can access [https://paper-api.alpaca.markets](https://paper-api.alpaca.markets) in your browser
3. Check if your firewall or antivirus is blocking Python's network access
4. Try again after a few minutes if the API is temporarily down

### Error: `Error connecting to Alpaca API: Invalid URL`

**Solution:** Make sure `BASE_URL` in `config.py` is exactly:
```python
BASE_URL = "https://paper-api.alpaca.markets"
```
(Do not add `/v2` or any other path - the library handles that automatically)

## 📁 Project Structure

```
Alpaca02/
│
├── config.py              # API keys configuration (DO NOT SHARE THIS FILE)
├── hello_alpaca.py        # Main script
├── requirements.txt       # Python dependencies
├── README.md             # This documentation
└── instruction.md        # Tutorial instructions
```

## 🔒 Security Reminders

- ⚠️ **Never commit `config.py` to Git** - Add it to `.gitignore`
- ⚠️ **Never share your API keys** publicly or in screenshots
- ⚠️ **Use Paper Trading keys** for tutorials (not Live Trading)
- ⚠️ **Rotate your keys** if you suspect they've been compromised

## 📚 Next Steps

Once you've successfully connected to Alpaca, you can:

- Learn how to retrieve market data
- Place your first trade
- Build trading strategies
- Monitor your portfolio

## 📞 Support

If you encounter issues:

1. Check the [Alpaca API Documentation](https://alpaca.markets/docs/)
2. Review the error messages for specific details
3. Ensure all prerequisites are met
4. Verify your API keys are correct

## 📝 License

This tutorial is part of an educational course on algorithmic trading with Alpaca.
