Lesson 21: The Bot's "Black Box" – Logging Every Decision to a File
Welcome to Lesson 21 of the Alpaca Trading Course! In this lesson, we'll delve into a crucial aspect of building a robust trading bot: creating a "black box" of its every move. We'll be using Python's built-in logging library to save all of your bot's actions and any potential errors to a .log file for later review.

Why is Logging So Important in Algorithmic Trading?
Think of a log file as your bot's diary. It's a chronological record of everything it has done, from the decisions it made to the errors it encountered. Without a proper logging system, you're essentially flying blind. If your bot makes an unexpected trade or crashes in the middle of the night, you'll have no way of knowing what went wrong. 
 

Here's why logging is non-negotiable for any serious trading bot:

Benefit	Description
Debugging	When errors occur, a detailed log file is your best friend. It can show you the exact line of code that caused the problem and the state of your bot at that moment. 
Performance Analysis	By logging every trade, you can go back and analyze your bot's performance. You can see which strategies are working and which aren't.
Audit Trail	In the world of finance, having a clear audit trail is essential. A log file provides an indisputable record of all trading activity.
Peace of Mind	Knowing that your bot is meticulously recording its every move will give you the confidence to let it run autonomously.
Introducing Python's logging Library
Python comes with a powerful and flexible logging library that's perfect for our needs. It's more powerful than using simple print() statements for a few key reasons:

Severity Levels: You can categorize your log messages by severity (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL). This allows you to filter and prioritize messages.

Flexible Output: You can send your logs to various destinations, including the console, files, and even email or web servers. 

Customizable Formatting: You can control the format of your log messages, adding valuable information like timestamps, the name of the logger, and the severity level. 
 

Getting Started: Basic Logging Configuration
Let's start by configuring a basic logger that writes to a file. Create a new Python file (e.g., trading_bot.py) and add the following code:

python
import logging

logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('Bot started.')
Let's break down what's happening here: 
 

import logging: This line imports the logging library.

logging.basicConfig(...): This function configures the root logger.

filename='trading_bot.log': This specifies the name of the file where the logs will be saved.

level=logging.INFO: This sets the minimum severity level for messages to be logged. In this case, we're logging INFO messages and above (WARNING, ERROR, and CRITICAL).

format='%(asctime)s - %(levelname)s - %(message)s': This defines the format of our log messages.

%(asctime)s: The time the log message was created.

%(levelname)s: The severity level of the message.

%(message)s: The log message itself.

logging.info('Bot started.'): This is an example of a log message.

If you run this script, it will create a file named trading_bot.log with the following content:

2025-12-18 06:04:39,123 - INFO - Bot started.
Logging Trading Decisions
Now, let's see how we can use logging to record our bot's trading decisions. Imagine your bot has a function that decides whether to buy, sell, or hold a particular stock. We can add logging to this function to record its decisions.

python
import logging
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# --- Your Alpaca API Credentials ---
API_KEY = 'YOUR_API_KEY'
API_SECRET = 'YOUR_API_SECRET'

# --- Initialize Logging ---
logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Initialize Alpaca Trading Client ---
trading_client = TradingClient(API_KEY, API_SECRET, paper=True)

def make_trade_decision(symbol):
    """
    A simple trading logic example.
    In a real bot, this would be much more complex.
    """
    # Replace this with your actual trading logic
    decision = 'BUY'  # or 'SELL' or 'HOLD'

    if decision == 'BUY':
        logging.info(f'Decision for {symbol}: {decision}')
        try:
            # Prepare and submit a market order
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=1,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY
            )
            market_order = trading_client.submit_order(
                order_data=market_order_data
            )
            logging.info(f'Submitted BUY order for {symbol}: {market_order.id}')
        except Exception as e:
            logging.error(f'Error submitting BUY order for {symbol}: {e}')
    elif decision == 'SELL':
        logging.warning(f'Decision for {symbol}: {decision}')
        # ... (code to submit a SELL order) ...
    else:
        logging.debug(f'Decision for {symbol}: {decision}')

# --- Main Bot Loop ---
if __name__ == '__main__':
    logging.info('Bot started.')
    make_trade_decision('AAPL')
    logging.info('Bot finished.')
In this example, we've added logging statements to record the trading decision and the outcome of the order submission. If an error occurs when submitting the order, we log it as an ERROR with the details of the exception. 
 

Best Practices for Logging
Here are some best practices to keep in mind when logging in your trading bot: 

Use a structured format: A consistent format makes it easier to parse and analyze your logs.

Log exceptions: Always wrap your code in try...except blocks and log any exceptions that occur.

Use the right log level: Don't log everything as INFO. Use the different severity levels to categorize your messages appropriately.

Rotate your log files: Log files can grow very large over time. Consider using a RotatingFileHandler or TimedRotatingFileHandler to automatically rotate your logs. 

