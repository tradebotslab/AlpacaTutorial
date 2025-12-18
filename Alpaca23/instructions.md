Lesson 23: What If the Bot Restarts? – Managing Position State
Welcome to Lesson 23. So far, we've built a bot that can make decisions, log its actions, and load its configuration from an external file. But what happens if the bot crashes or needs to be restarted? It loses its memory. A stateless bot is a dangerous bot, as it might try to buy a stock it already owns or sell a position it has already closed.

In this lesson, you'll learn how to manage your bot's state by saving its current position status to a file, making it resilient to restarts.

The Problem: Bot Amnesia
Imagine this scenario:

Your bot decides to buy 10 shares of SPY. It is now "in a position".

The server running your bot reboots for a system update.

Your bot script starts again.

Since it has no memory of the past, it checks the market data, and its logic tells it to buy 10 shares of SPY... again.

You have now doubled your intended position and increased your risk, all because the bot forgot what it had already done. The internal state of the bot (like a simple boolean variable is_in_position) is reset to its default value on every restart.

The Solution: An External State File
Just as we separated our configuration into a config.json file, we can save the bot's operational state to another file, let's call it state.json. This file will act as the bot's persistent memory.

Our bot's logic will be:

On Startup: Read the state.json file to restore the last known state.

During Operation: Check the in-memory state before making any decisions.

After an Action: Write the new state to state.json immediately after a state-changing action (like a successful buy or sell order).

Step 1: Create the state.json File
Create a new file named state.json in your project folder. We'll start with a default state, assuming the bot is not currently in a position.

JSON
{
  "is_in_position": false
}
Step 2: Load and Save State in Python
We need two helper functions: one to load the state from the file and one to save it back.

python
import json

STATE_FILE = 'state.json'

def load_state():
    """Loads the bot's state from the state file."""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, return a default state
        return {'is_in_position': False}

def save_state(state):
    """Saves the bot's state to the state file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

Step 3: Integrate State Management into the Bot Logic
Now, let's weave this into our main trading logic. The bot will load the state at the beginning, use it to make decisions, and save it after every trade.

Here is a full example combining concepts from previous lessons:

python
import json
import logging
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# --- Basic Configuration ---
CONFIG_FILE = 'config.json'
STATE_FILE = 'state.json'

logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- State Management Functions ---
def load_state():
    """Loads the bot's state from the state file."""
    try:
        with open(STATE_FILE, 'r') as f:
            logging.info("State file found. Loading state.")
            return json.load(f)
    except FileNotFoundError:
        logging.warning("State file not found. Starting with default state.")
        return {'is_in_position': False}

def save_state(state):
    """Saves the bot's state to the state file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    logging.info(f"State saved: {state}")


# --- Main Bot Logic ---
if __name__ == '__main__':
    logging.info("Bot starting up...")

    # Load configuration
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    # Load state
    bot_state = load_state()
    is_in_position = bot_state.get('is_in_position', False)

    # Initialize Alpaca Client
    trading_client = TradingClient(config['api_key'], config['api_secret'], paper=config['paper_trading'])
    
    # Simple trading logic for demonstration
    # In a real bot, this would be based on market data analysis
    buy_signal = True # Assume a buy signal is generated

    if not is_in_position and buy_signal:
        logging.info("Buy signal triggered and not in a position. Submitting BUY order.")
        try:
            market_order_data = MarketOrderRequest(
                symbol=config['trade_symbol'],
                qty=config['trade_quantity'],
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            trading_client.submit_order(order_data=market_order_data)
            
            # --- IMPORTANT: Update and save state AFTER confirming the action ---
            bot_state['is_in_position'] = True
            save_state(bot_state)

        except Exception as e:
            logging.error(f"Failed to submit BUY order: {e}")
    
    elif is_in_position and not buy_signal: # Assuming a sell signal
        logging.info("Sell signal triggered and in a position. Submitting SELL order.")
        try:
            # Sells the entire position
            trading_client.close_position(config['trade_symbol'])

            # --- IMPORTANT: Update and save state AFTER confirming the action ---
            bot_state['is_in_position'] = False
            save_state(bot_state)

        except Exception as e:
            logging.error(f"Failed to submit SELL order: {e}")
    else:
        logging.info("No action taken. In position: %s, Buy Signal: %s", is_in_position, buy_signal)

    logging.info("Bot finished cycle.")

A More Robust Approach: Query the Broker
Relying on a local file is good, but the ultimate source of truth is always the broker. A more advanced bot should verify its position with the Alpaca API at startup. This protects against cases where the state file might be corrupted or was not saved correctly before a crash.

You can get your current position for a symbol like this:

python
try:
    position = trading_client.get_open_position(config['trade_symbol'])
    # If this doesn't raise an exception, you have a position.
    is_in_position = True
    logging.info(f"Found existing position on Alpaca: {position.qty} shares of {position.symbol}.")
except Exception:
    # An exception means no open position was found for that symbol.
    is_in_position = False
    logging.info("No existing position found on Alpaca for this symbol.")

# Update the local state file to match the broker's reality
bot_state['is_in_position'] = is_in_position
save_state(bot_state)
The best practice is a hybrid approach: check with the broker at startup to synchronize your state, and then use the local state file for quick checks during the bot's run cycle.