# Alpaca Trading Course - Tutorial 5

## What Happened to My Order? – Checking Status & Positions

This tutorial demonstrates how to check the status of your submitted orders and view your current open positions using the Alpaca Trading API.

## Prerequisites

- Completed Tutorial 4: You should have already run the `place_order.py` script to submit an order
- An Order ID: Have an Order ID ready from the output of the `place_order.py` script
- Paper Trading Account: This script should be run against your Paper Trading account where the order was placed

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Credentials**
   - Copy `config.py.template` to `config.py`
   - Add your Alpaca API credentials to `config.py`
   - Get your credentials from: https://app.alpaca.markets/paper/dashboard/overview

3. **Run the Script**
   ```bash
   python check_status.py
   ```

## What This Script Does

1. **Lists Open Orders**: Shows all orders that haven't been filled or canceled yet
2. **Checks Specific Order**: Allows you to check the status of a particular order by its ID
3. **Displays Current Positions**: Shows all stocks you currently own after buy orders have been filled

## Understanding the Workflow

1. **Submit Order**: Run `place_order.py` to submit a buy order. The API returns an Order object with a unique ID and status like `accepted`.
2. **Order Fills**: The exchange processes your order, and its status changes to `filled`.
3. **Check Status**: Run `check_status.py` to confirm the order was filled.
4. **Position Opens**: Once the order is filled, `api.list_positions()` will show your new holding as an open position.

## Important Notes

- **API Keys**: Never commit `config.py` to version control. It's already in `.gitignore`.
- **Paper Trading**: This script uses the paper trading environment by default for safe learning.
- **Order ID**: To check a specific order, replace `YOUR_ORDER_ID_HERE` in the script with an actual Order ID from a previous trade.

## Error Handling

All API calls are wrapped in try-except blocks with logging to help you understand what went wrong if something fails.

## License

This is an educational project for learning algorithmic trading with Alpaca.
