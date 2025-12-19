Lesson 28: Faster Than HTTP – Streaming Real-Time Data with WebSockets
Welcome to Lesson 28. Until now, your bot has likely been "polling" the Alpaca API—asking for the latest price every minute or every few seconds. This works, but it's like a child in the back of a car asking, "Are we there yet?" over and over. It's inefficient, slow, and you might miss important events that happen between your requests.

In this lesson, you will learn how to upgrade your bot to a professional, event-driven model by using WebSockets to stream market data in real-time.

The Problem with Polling (The HTTP Request/Response Model)
When your bot makes a standard API call (an HTTP request), it follows this pattern:

Open a connection to the Alpaca server.

Ask: "What's the latest price for SPY?"

Receive the answer.

Close the connection.

Wait 60 seconds.

Repeat.

This has major drawbacks:

Latency: You only get new information when you ask for it. If the price of a stock spikes and crashes within your 60-second wait period, your bot will be completely oblivious to it.

Inefficiency: Each request has overhead (establishing connections, sending headers). Most of the time, the price hasn't changed, making the request wasteful.

API Rate Limits: Many services limit the number of requests you can make per minute. Polling aggressively can get you temporarily blocked.

The Solution: WebSockets for Real-Time Streaming
A WebSocket connection is different. It's a persistent, two-way communication channel between your bot and the Alpaca server.

Instead of your bot repeatedly asking for data, the server pushes the data to your bot the instant it becomes available.

It's like telling the driver, "Just let me know the moment we arrive." You can relax until you get the information you need.

This is how modern, real-time applications work, and it's essential for any trading strategy that needs to react quickly to market changes.

Setting Up a WebSocket Stream with Alpaca
We'll use the StockDataStream client from the Alpaca library. Working with streams requires using Python's asyncio library, which allows for asynchronous programming. Don't worry if the async and await syntax is new; the pattern is straightforward.

1. Install Libraries:
The Alpaca library already includes the necessary components. Ensure you have it up-to-date.

2. The Asynchronous Handler:
First, we need to create a function that will be executed every time a new piece of data arrives from the stream. This is called a "handler" or "callback." It must be an async function.

python
async def trade_handler(trade):
    """
    This function is called for every new trade data point.
    """
    # The 'trade' object contains the data
    print("--- New Trade ---")
    print(f"Symbol:   {trade.symbol}")
    print(f"Price:    {trade.price}")
    print(f"Volume:   {trade.size}")
    print(f"Timestamp:{trade.timestamp}")
3. The Main Streaming Logic:
Next, we'll write the main part of our script. This will also be an async function that sets up the connection and tells the stream which data we're interested in.

python
import asyncio
from alpaca.data.live import StockDataStream

# --- Your Alpaca API Credentials ---
# Best to load these from your config.json file
API_KEY = 'YOUR_API_KEY' 
API_SECRET = 'YOUR_SECRET_KEY'

async def main():
    """
    This is the main function that runs the data stream.
    """
    # 1. Instantiate the stream client
    stream = StockDataStream(API_KEY, API_SECRET)

    # 2. Subscribe to the data we want
    # We can subscribe to trades, quotes, or bars for one or more symbols.
    # The '*' symbol means subscribe to all trades.
    stream.subscribe_trades(trade_handler, "SPY", "TSLA") 
    # stream.subscribe_quotes(quote_handler, "AAPL") # Example for quotes

    # 3. Start the stream
    # This is a blocking call that will run forever,
    # calling our handler function as new data arrives.
    await stream.run()


if __name__ == '__main__':
    # This runs the main async function
    asyncio.run(main())
Running the Code
When you run this script, your terminal won't do anything for a moment. But as soon as a trade for "SPY" or "TSLA" occurs on the market, the trade_handler function will execute, and you will see the trade details printed to your console in real-time. To stop the script, you'll need to press Ctrl+C.

Integrating Streaming into Your Bot
This event-driven model fundamentally changes your bot's architecture. Instead of a while True: loop with a sleep() call, your bot now idles until the stream "wakes it up" by calling a handler.

Your bot's core logic will move inside the handler function.

python
# A conceptual example of what your bot becomes

# Global variables or a class to hold state
current_price = 0.0
moving_average = 0.0
is_in_position = False # Loaded from state file at startup

async def trade_handler(trade):
    global current_price, moving_average, is_in_position

    # 1. Update your indicators with the new price
    current_price = trade.price
    # ... code to recalculate moving_average ...

    # 2. Check your strategy rules
    if current_price > moving_average and not is_in_position:
        print("BUY SIGNAL!")
        # ... code to submit a buy order ...
        # ... update state file and send Discord notification ...
    
    elif current_price < moving_average and is_in_position:
        print("SELL SIGNAL!")
        # ... code to submit a sell order ...
        # ... update state file and send Discord notification ...
Conclusion
You have taken a massive leap forward. By switching from polling to WebSockets, your bot is no longer a slow-reacting machine but a nimble, event-driven system capable of acting on market information the instant it becomes available. This is the foundation upon which nearly all serious, short-term trading strategies are built.

In the next lesson, we will use this real-time data stream to build and deploy a live trading strategy.