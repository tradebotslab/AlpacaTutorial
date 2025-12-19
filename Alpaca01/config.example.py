# config.example.py
# This is an example configuration file
# Copy this file to config.py and add your real API keys
#
# IMPORTANT: Never commit config.py to version control!
# Add config.py to .gitignore to protect your API keys

# Your Alpaca API credentials (Paper Trading)
# Get these from: https://app.alpaca.markets/paper/dashboard/overview
API_KEY = "YOUR_API_KEY_HERE"
SECRET_KEY = "YOUR_SECRET_KEY_HERE"

# Paper trading URL (for safe testing)
# Use this URL for paper trading - it uses simulated money
BASE_URL = "https://paper-api.alpaca.markets"

# For live trading (NOT recommended for beginners), use:
# BASE_URL = "https://api.alpaca.markets"

