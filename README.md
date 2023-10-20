# Portfolio-Analysis-Coding-Challenge
Coding Challenge for Stevens Student Managed Investment Fund

In this challenge, I was given a set of dummy data to simulate a portfolio for the Stevens Student Managed Investment Fund with a starting portfolio value of $200,000. Within the Portfolio Analysis program, I created the following methods with the following purposes:

clean_data()- accurately deals with any discrepancies in the input data and returns usable data. Any missing (NA) values must be calculated for or found from yfinance accordingly.  

asset_value()- calculates the total market value of each equity as well as the Net Asset Value at the end of each month

unrealized_returns()- calculates the unrealized returns of each stock.

plot_portfolio()- builds a plot of the portfolio's value over time, from the end of June to the end of September

plot_liquidity()- builds a plot of the ratio between the cash on hand and the portfolio's total value, from the end of June to the end of September

In the Risk program, I was asked to identify various financial ratios such as volatility, Sharpe Ratio, 95% VaR, Maximum Drawdown, and Beta for the portfolio. I also created a time-weighted and money-weighted method to value the returns from the portfolio with respect to time and size of the investment.
