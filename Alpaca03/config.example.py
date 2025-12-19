# config.example.py
# Configuration template for Alpaca API credentials
# 
# INSTRUCTIONS:
# 1. Copy this file to config.py: cp config.example.py config.py
# 2. Replace the placeholder values below with your actual API keys
# 3. Never commit config.py to version control!

# Alpaca API Keys for the paper trading account
API_KEY = "YOUR_PAPER_API_KEY_HERE"  # <--- REPLACE WITH YOUR API KEY
SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE"  # <--- REPLACE WITH YOUR SECRET KEY

# Always default to the paper trading URL for tutorials
BASE_URL = "https://paper-api.alpaca.markets"

# IMPORTANT: Never share this file or upload it to public repositories like GitHub!
# The config.py file is protected by .gitignore

