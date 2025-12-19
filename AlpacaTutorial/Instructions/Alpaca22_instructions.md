Lesson 22: Stop Digging in the Code – Using an External Config File
Welcome to Lesson 22 of the Alpaca Trading Course! In this section, we'll learn how to move all our settings—such as API keys, strategy parameters, and other variables—to an external config.json file. This is a simple yet incredibly powerful technique that will make managing your bot much easier and more secure.

The Problem with "Hardcoding" Settings
Until now, you've likely kept your API keys and other parameters directly in your Python code. This approach, known as "hardcoding," is simple at first but quickly becomes problematic.

Problem	Description
Lack of Flexibility	Want to test the bot on a different stock symbol? You have to find the right line and change the code. Want to adjust a strategy parameter? Again, digging through the code.
Security Risk	Accidentally sharing your code (e.g., on GitHub) means sharing your secret API keys. This is a direct path to losing your funds!
Management Difficulty	As the bot grows, settings will be scattered across multiple files, making them hard to find and modify.
The Solution: A config.json File
The ideal solution is to separate the configuration from the application logic. We will use a file in JSON (JavaScript Object Notation) format for this, as it is human-readable and easy for Python to process.

Step 1: Create the config.json file
In the same folder where your Python script is located, create a new file named config.json. Paste the following content into it and fill in your details.

JSON
{
  "api_key": "YOUR_API_KEY",
  "api_secret": "YOUR_API_SECRET",
  "paper_trading": true,
  "trade_symbol": "SPY",
  "trade_quantity": 10,
  "strategy_parameters": {
    "short_window": 40,
    "long_window": 100
  }
}
Step 2: Load the Configuration in Python
Now, let's modify our bot to load these settings at startup. We will need the built-in json library for this.

Add the following code snippet at the beginning of your script:

python
import json

# --- Loading Configuration ---
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found. Please make sure the file exists.")
    exit()

API_KEY = config['api_key']
API_SECRET = config['api_secret']
IS_PAPER_TRADING = config['paper_trading']
SYMBOL = config['trade_symbol']
QUANTITY = config['trade_quantity']

print("Configuration loaded successfully.")
# You can now use the variables API_KEY, SYMBOL, etc. in the rest of your code
This code safely opens the config.json file, loads its contents into a dictionary named config, and then assigns the values to individual variables.

Step 3: Refactor the Bot's Code
Now, go through your code and replace all the "hardcoded" values with the new variables loaded from the configuration file.

Example BEFORE the change:

python
# --- Initialize Alpaca Trading Client ---
trading_client = TradingClient('YOUR_API_KEY', 'YOUR_SECRET_KEY', paper=True)

# ...

# Prepare and submit a market order
market_order_data = MarketOrderRequest(
    symbol="SPY",
    qty=10,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY
)
Example AFTER the change:

python
import json
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# --- Loading Configuration ---
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("Error: config.json not found. Please make sure the file exists.")
    exit()

API_KEY = config['api_key']
API_SECRET = config['api_secret']
IS_PAPER_TRADING = config['paper_trading']
SYMBOL = config['trade_symbol']
QUANTITY = config['trade_quantity']

# --- Initialize Alpaca Trading Client ---
trading_client = TradingClient(API_KEY, API_SECRET, paper=IS_PAPER_TRADING)

# ...

# Prepare and submit a market order
market_order_data = MarketOrderRequest(
    symbol=SYMBOL,
    qty=QUANTITY,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY
)
Extremely Important: Secure Your Keys!
Now that your API keys are in a separate file, you must ensure that it never ends up in a public code repository (like GitHub).

Create a file named .gitignore (with a dot at the beginning) and add one line to it:

config.json
This will make the Git version control system ignore this file, protecting your data.

Summary
Congratulations! You have just implemented one of the most important professional practices in software development. Your bot is now:

More Secure: Keys are separated from the code.

More Flexible: Changing parameters doesn't require modifying the logic.

Better Organized: All settings are in one, dedicated place.

In the next lesson, we will focus on implementing simple trading strategies. See you there!