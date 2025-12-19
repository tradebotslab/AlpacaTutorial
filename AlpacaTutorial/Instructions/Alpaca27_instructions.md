Lesson 27: Understanding Your Results – Analyzing a Backtest Report
Welcome to Lesson 27. You've run your first backtest, and a report full of numbers and charts has appeared on your screen. You see "Return
: 150%" and think you've struck gold. But hold on—the total return is only a tiny part of the story. A profitable strategy might be so risky that it's psychologically impossible to follow.

In this lesson, you will learn how to dissect a backtest report like a professional. We'll focus on four of the most critical metrics: Annual Return, Max Drawdown, Sharpe Ratio, and Win Rate. Understanding them is the key to knowing if your strategy is genuinely robust or just a lucky gamble.

Beyond the Final Number
Looking only at the final return is a classic beginner's mistake. Ask yourself:

How long did it take to achieve that return?

How much did the portfolio value swing up and down along the way?

Would I have panicked and abandoned the strategy during a losing streak?

The metrics below help us answer these questions and paint a complete picture of a strategy's performance and risk profile.

1. Annual Return
The Return [C] % (or Return [%]) in your backtest report shows the total return over the entire period. The Annual Return standardizes this, telling you the average return your strategy would have generated per year.

Metric	Description	Why it Matters
Annual Return	The geometric average amount of money the strategy earned per year.	It provides a normalized basis for comparison. A 50% return over 5 years (approx. 8.4% annually) is very different from a 50% return in 1 year (50% annually). It helps you compare your strategy against benchmarks like the S&P 500's average annual return.
Rule of Thumb: Your strategy's Annual Return should be meaningfully higher than the "Buy & Hold Return" for the same period. If it's not, you took on a lot of complexity and risk for nothing.

2. Max Drawdown
This is arguably the most important risk metric. It measures the largest single drop from a portfolio's peak value to its subsequent lowest point (the trough).

Metric	Description	Why it Matters
Max Drawdown	The maximum "paper loss" your portfolio experienced during the backtest.	This is the metric of psychological pain. It answers the question: "What is the worst losing streak I would have had to endure?" If a strategy has a 50% Max Drawdown, it means at one point, your $10,000 portfolio would have dropped to $5,000. Could you stomach that without panicking and selling everything at the bottom? A low drawdown is a sign of a more stable, less stressful strategy.
Example: If your portfolio grows from $10k to $15k, then drops to $7.5k before recovering, your drawdown is ($15,000 - $7,500) / $15,000 = 50%.

3. Sharpe Ratio
The Sharpe Ratio is the gold standard for measuring risk-adjusted return. It tells you how much return you are getting for each unit of risk you take on (where risk is measured by volatility).

Metric	Description	Why it Matters
Sharpe Ratio	The average return earned in excess of the risk-free rate per unit of volatility.	It helps you compare different strategies. A strategy with a 20% return and wild price swings might be worse than a strategy with a 15% return and a smooth, steady equity curve. The second strategy will have a higher Sharpe Ratio.
General Interpretation:

< 1.0: Not considered great. The returns do not justify the risk taken.

1.0 - 1.99: Considered good.

2.0 - 2.99: Considered very good.

> 3.0: Considered excellent (and may be a sign of a "too good to be true" backtest).

A higher Sharpe Ratio is almost always better.

4. Win Rate
and the Profit Factor
The Win Rate tells you how many of your trades were winners. It's an intuitive metric, but it can be very misleading if viewed in isolation.

Metric	Description	Why it Matters
Win Rate	The percentage of trades that closed with a profit.	It gives you an idea of the strategy's consistency. A high win rate can be psychologically comforting. However, it says nothing about the size of the wins versus the size of the losses.
This is why you must look at it alongside the Profit Factor (stats['Profit Factor']) or the average win vs. average loss.

Scenario A (Bad): Win Rate: 90%. Average Win: $10. Average Loss: $100.

You win 9 out of 10 trades, making 9 * $10 = $90. But your one losing trade costs you $100. You have a net loss of $10.

Scenario B (Good): Win Rate: 40%. Average Win: $100. Average Loss: $20.

You win 4 out of 10 trades, making 4 * $100 = $400. Your six losing trades cost you 6 * $20 = $120. You have a net profit of $280.

Conclusion: A low win rate is perfectly acceptable if your winning trades are significantly larger than your losing trades.

Putting It All Together: A Holistic View
Never judge a strategy by a single number. Analyze the metrics together to understand the full story.

Metric	Strategy A ("Slow & Steady")	Strategy B ("Gambler")	Analysis
Annual Return	15%	25%	B looks better on the surface.
Max Drawdown	-10%	-60%	A is far less risky and easier to stick with. A 60% loss would wipe out most retail traders.
Sharpe Ratio	1.8	0.7	A provides excellent return for its low risk. B's returns do not justify its extreme volatility.
Win Rate	55%	30%	B has very few winning trades, which can be psychologically difficult.
Verdict: Strategy A is vastly superior for almost any real-world investor, even though its annual return is lower. It provides good returns with manageable, predictable risk.

Conclusion
Analyzing a backtest report is a skill. It requires you to look beyond the flashy return percentage and critically evaluate a strategy's risk profile and consistency. By understanding these key metrics, you can make informed decisions, avoid dangerous strategies, and build a trading bot that you can trust to run for the long term.