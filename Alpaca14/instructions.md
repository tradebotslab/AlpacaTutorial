Tutorial 14: Protecting Your Profits – What is a Trailing Stop-Loss?
Objective: This tutorial provides a conceptual explanation of one of the most powerful tools for profit protection: the trailing stop-loss. You will understand how it works and why it's superior to a fixed stop-loss for letting winning trades run while securing gains.

1. The Limitation of a Standard Stop-Loss
In our previous tutorials, we set a fixed stop-loss. For example, we'd buy a stock at $100 and set a stop-loss at $98. This is an excellent safety net to prevent a large loss.

However, it has one major flaw. What happens if the trade is a big winner?

You buy at $100. Your stop-loss is at $98.

The stock price soars to $150. You have a large "paper profit" of $50 per share.

The trend then reverses, and the price starts to fall. It drops to $140... $120... $100...

Your fixed stop-loss is still at $98. The trade finally stops out, and you exit with a $2 loss, having watched your entire $50 paper profit evaporate.

A fixed stop-loss protects your downside but does nothing to protect your upside.

2. The Solution: The Trailing Stop-Loss
A Trailing Stop-Loss is a dynamic stop order that automatically moves up as the price of your stock moves up. It "trails" the price at a set distance you define.

The key rule is:

It only moves in one direction—in your favor.

If you are in a buy trade, the trailing stop will only ever move up. It will never move down.

This allows you to give a winning trade room to grow while continuously raising your safety net behind it.

3. How a Trailing Stop-Loss Works: An Example
Let's imagine you buy a stock and set a 10% trailing stop-loss.

Step 1: Entry

You buy the stock at $100.

Your initial stop-loss is automatically set at $90 ($100 - 10%).

Step 2: Price Rises

The stock price moves up to a new high of $110.

Your trailing stop automatically recalculates and moves up to $99 ($110 - 10%).

You have now locked in a minimum breakeven trade (minus commissions/fees).

Step 3: Price Rises Further

The stock has a great week and hits a new high of $140.

Your trailing stop follows it up, moving to $126 ($140 - 10%).

You have now guaranteed yourself a minimum profit of $26 per share, even if the trade turns against you.

Step 4: Price Dips (but doesn't crash)

The stock pulls back from its high of $140 and drops to $135.

Your trailing stop STAYS at $126. It does not move down.

Step 5: The Exit

The trend finally reverses for good, and the stock price falls, eventually hitting $126.

Your trailing stop order is triggered, and your position is automatically sold.

Result: You exit the trade with a $26 profit per share. Without a trailing stop, you would have watched the price fall much further, potentially all the way back to your original entry point or stop-loss.

4. The Benefits
Protects Unrealized Profits: It systematically turns "paper profits" into locked-in, real profits.

Lets Your Winners Run: It stops you from selling too early. As long as the uptrend continues, you remain in the trade, allowing you to capture the majority of a large move.

Emotion-Free Risk Management: It provides a logical, automated exit based on a change in the stock's behavior, removing the guesswork and emotional stress of deciding when to take profits.

5. Implementation with the Alpaca API
The Alpaca API makes this incredibly easy by supporting trailing stops directly within an order submission. You don't have to write complex code to manually adjust your stop-loss; the broker handles it for you.

When submitting an order, instead of a simple stop_loss, you provide a trail_percent or trail_price.

Conceptual Code Example:

python
# This is not a full script, just the order submission part.

# Option 1: Using a Percentage
api.submit_order(
    symbol="AAPL",
    qty=10,
    side='buy',
    type='market',
    time_in_force='day',
    order_class='trailing_stop',
    trail_percent=5.0  # Set a 5% trailing stop-loss
)

# Option 2: Using a Fixed Dollar Amount
api.submit_order(
    symbol="NVDA",
    qty=5,
    side='buy',
    type='market',
    time_in_force='day',
    order_class='trailing_stop',
    trail_price='2.50' # Set a $2.50 trailing stop-loss
)
By using this order type, you can build a bot that not only enters trades intelligently but also manages them with a sophisticated, profit-protecting exit strategy.