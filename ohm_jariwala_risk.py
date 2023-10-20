from ohm_jariwala_portfolio_analysis import PortfolioAnalysis# replace first_last_portfolio_analysis with the file name that holds your PortfolioAnlaysis class

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

class Risk:
    
    def __init__(self, Portfolio):
        self.portfolio = Portfolio


    """
    Implement a financial_ratio() function that calculates and returns the following metrics:
        1. Volatility
        2. Sharpe Ratio
        3. 95% VaR (Value at Risk)
        4. Maximum Drawdown
        5. Beta

    Implement time_weighted() function that calculates the time-weighted return of the portfolio and returns a plot of the returns over time
    
    Implement money_weighted() functions that calculate the money-weighted return of the portfolio and returns a plot of the returns over time
     
    ** Do not use any packages or API that directly compute the returns for you.
    ** Feel free to alter the class the way you wish as long as the output remains the same as defined in the main function.
    """
    
    
    #TODO delete the following line and start building the Risk class.
    pass
    def financial_ratio(self):
        # creating a dictionary to hold the ratios
        ratios={}
        
        #calling asset value dataframe to Risk
        av_dataframe=PortfolioAnalysis('dummy_data.xlsx')
        av_dataframe = av_dataframe.asset_value()
        
        av_dataframe= av_dataframe.T
        
        #creating new dataframe that only considers the NAV
        NAV_dataframe= av_dataframe['NAV']
        NAV_dataframe['2023-06-30']= 200000.00000 #Value of portfolio at 6-30-2023 is starting value of 200,000
        
        #Volatility- percent change of NAV
        #Volatility shows how much the portfolios returns change over time, which shows how consistent the portfolio is in it's returns
        returns_df= NAV_dataframe.pct_change()

        ratios['Volatility']= returns_df.std() *100 
        
        
        #Sharpe Ratio
        #The Sharpe Ratio evaluates how the portfolio performs by adjusting for risk. A negative sharpe ratio shows that the investment has a lower return compared to that of a risk free asset, meaning the risk being taken has some negative impact on returns
        risk_free_rate= 0.058 #treasury
        excess_return= returns_df - risk_free_rate
        sharpe= excess_return.mean() / excess_return.std()
        ratios['Sharpe Ratio']= sharpe
        
        #95% VaR
        #95% Value at Risk shows the max potential loss on an investment at a 95% confidence level, which indicates how much risk a portfolio is taking on
        returns_df= returns_df.fillna(0) 
        var95 = np.percentile(returns_df, 5) * 100
        ratios['95% Value at Risk']= var95
        
        #Maximum Drawdown
        #Max Drawdown is the largest drop from the highest to lowest value that a portfolio has experienced over a certain period of time.

        cumulative_returns = (1 + returns_df).cumprod()#CHATGPT
        
        peak = np.maximum.accumulate(cumulative_returns)
        trough = np.minimum.accumulate(cumulative_returns) #used chatGPT to identify what the accumulate attribute does
        
        drawdowns= (peak-trough) / peak
        
        maximimum_drawdown= np.max(drawdowns)
        ratios['Maximum Drawdown']= maximimum_drawdown * 100
        
        #Beta
        #Beta measures how the portfolio performs relative to the market
        
        benchmark = 'SPY' # S&P 500
        benchmark_data = yf.download(benchmark, start="2023-06-29", end="2023-09-30")["Adj Close"]
        benchmark_returns= benchmark_data.pct_change().dropna()
        

        
        #returning the covariance of the returns
        return_covariance = np.cov(returns_df)

        #returning the covariance of the benchmark
        benchmark_variance = np.var(benchmark_data)

        #formula for beta
        beta = return_covariance / benchmark_variance
        ratios['Beta'] = beta
        

        return ratios
    
    def time_weighted(self):
        #calling asset value dataframe to Risk(copy from earlier methods)
        av_dataframe=PortfolioAnalysis('dummy_data.xlsx')
        av_dataframe = av_dataframe.asset_value()
        
       
        av_dataframe= av_dataframe.T
        
        #creating new dataframe that only considers the NAV
        NAV_dataframe= av_dataframe['NAV']
        NAV_dataframe['2023-06-30']= 200000.00 #Value of portfolio at 6-30-2023 is starting value of 200,000
        
        #time weighted- values returns with consideration for the duration of the investment
        #Pros: the time weighted approach accounts for the stability of returns, which is essential to building a portfolio that can withstand market events and pressures.
        #Cons: this approach doesn't account for the size of the investment. For example, a portfolio could show strong returns but may simply hold a large cash position during down swings.  
        returns_df= NAV_dataframe.pct_change()
        returns_df= returns_df.fillna(0)
        
       
        
        cumulative_returns = (1 + returns_df).cumprod()
        
        daily_returns = cumulative_returns.pct_change()
        time_weighted_returns = (1 + daily_returns).prod()-1
        NAV_dataframe['2023-06-30']= 0
        
        plt.figure(figsize= (10, 6))
        plt.plot(cumulative_returns.index, cumulative_returns.values, label='Time-Weighted Returns', marker='o')
        plt.xlabel('Date')
        plt.ylabel('Time-Weighted Returns')
        plt.title('Time-Weighted Returns Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()
    
        return (time_weighted_returns)
        
    def money_weighted(self):
        
        #calling asset value dataframe to Risk(repeated in time weighted and money)
        av_dataframe=PortfolioAnalysis('dummy_data.xlsx')
        av_dataframe = av_dataframe.asset_value()

        av_dataframe= av_dataframe.T
        
        #creating new dataframe that only considers the NAV
        NAV_dataframe= av_dataframe['NAV']
        NAV_dataframe['2023-06-30']= 200000 #Value of portfolio at 6-30-2023 is starting value of 200,000
        
        
        #money weighted- values returns with onsideration for the size of the investment
        #Pros: the money weighted approach shows how effective an investment is and indicates how effective each dollar is in generating returns
        #Cons: this approach does not account for time in its calculation so the returns could be very short term or long term, but the calculation will not account for that.   
        returns_df= NAV_dataframe.pct_change()
        returns_df= returns_df.fillna(0)
        
        
        cumulative_returns = (1 + returns_df).cumprod()
        
        daily_returns = cumulative_returns.pct_change()
        
        cash_flows=[0, -272.62, 4941.00, -3083.2]
        
        
        pctChange=0
        cumulative_cash_flows = np.cumsum(cash_flows)
        for i in range (len(cumulative_cash_flows)):
            if i ==3:
                continue
            else:
                pctChange= (cumulative_cash_flows[i+1]-cumulative_cash_flows[i])/cumulative_cash_flows[i]

            
        cumulative_cash_flows= pctChange
        
        money_weighted_returns = ((1 + daily_returns) ** (1 + cumulative_cash_flows) - 1)*100 #formula obtained from ChatGPT
        
        
        #Graph style given by ChatGPT
        plt.figure(figsize=(10, 6))
        plt.plot(money_weighted_returns.index, money_weighted_returns.values, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Money-Weighted Returns (%)')
        plt.title('Money-Weighted Returns Over Time')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.show()
        
        return money_weighted_returns

#Financial ratios prints a dictionary that is within the warnings when run on VSCODE


if __name__ == "__main__":  # Do not change anything here - this is how we will test your class as well.
    fake_port = PortfolioAnalysis("dummy_data.xlsx") # use the clean data you have from the Mandatory Challenge
    risk_metrics = Risk(fake_port)
    print(risk_metrics.financial_ratio())
    risk_metrics.time_weighted()
    risk_metrics.money_weighted()