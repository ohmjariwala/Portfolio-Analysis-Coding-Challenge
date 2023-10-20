# Name: Ohm Jariwala

# You may not import any additional libraries for this challenge besides the following
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf



class PortfolioAnalysis:
    """
    Create a constructor that reads in the excel file and calls all necessary methods
    You may set the output of these methods to be attributes of the class that you may
    access later on in other challenges.

    Create a method called `clean_data` which accurately deals with any discrepancies
    in the input data and returns usable data that you can access for the rest of your tasks
    You must have comments explaining why you chose to make any of the changes you did. Any
    missing (NA) values must be calculated for or found from yfinance accordingly.
    The cleaned data should be exported to an excel file with 3 sheets, all of the same format
    as the original data. The file name should be called `cleaned_data.xlsx`.
    
    #NOTE:
    You may import and use this cleaned data file for any of the optional challenges, as needed.
    You may also import this file and create an instance of the PortfolioAnalysis class to use
    in any of the optional challenges, as needed.

    Create a method called `asset_value` that calculates the total market value of each equity
    in the portfolio at the end of the month, with tickers in the rows and dates in the columns
    as well as another row that keeps track of the portfolio's Net Asset Value (NAV) at the end
    of each month. If there is no position for a certain equity during a given month, its value
    should be 0. This data should be kept track of from the end of June to the end of September

    Create a method called `unrealized_returns` that calculates the unrealized returns of each stock.
    The output should be a dataframe that has tickers in the rows, dates in the columns, and the
    unrealized gain/loss of each ticker at the end of each month.
    If there is no unrealized loss to be calculated for a given stock during a given month, its
    value should be 0.

    Create a method called `plot_portfolio` that builds a plot of the portfolio's value over time,
    from the end of June to the end of September

    Create a method called `plot_liquidity` that builds a plot of the ratio between the cash on
    hand and the portfolio's total value, from the end of June to the end of September
    """
    #TODO delete the following line and start building the PortfolioAnalysis class.
    pass
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.cleandata=self.clean_data()
        self.asset_values = self.asset_value()
        self.unrealized_pnl=self.unrealized_returns()
    
        

    def clean_data(self):
        
        #Defining a method that takes in a value and removes all the string attributes of the input and returns the value as a float [A]
        def strToNum(value):
            if type(value)== str:
                value=value.strip("'").strip('"').strip("+")
                return float(value)

        with pd.ExcelWriter('cleaned_data.xlsx', engine='xlsxwriter') as writer: #ChatGPT 
            for date in ['2023-07-31', '2023-08-31', '2023-09-30']:
                
                #Creating a data frame that reads in every sheet in the excel file
                current_df = pd.read_excel(self.excel_file_path, sheet_name=date)
                current_df= current_df.fillna(0)

                new_df= pd.DataFrame()
                stockarray= current_df['Stock']
                quantityarray= []
                unitcostarray=[]
                marketpricearray=[]
                
                
                #[A]
                # replaces string quantities in each column to an array if string is identified. The modified values are populated to empty arrays
                for quantity in current_df['Quantity']:
                    if type(quantity)== float:
                        quantityarray.append(quantity)
                    else:
                        quantity= strToNum(quantity)
                        quantityarray.append(quantity)
                
                for unitcost in current_df['UnitCost']:
                    if type(unitcost)==float or type(unitcost)==int:
                        unitcostarray.append(unitcost)
                    else:
                        unitcost= strToNum(unitcost)
                        unitcostarray.append(unitcost)
                    
                    
                for marketprice in current_df['MarketPrice']:
                    if type(marketprice)==float or type(marketprice)==int:
                            marketpricearray.append(marketprice)
                    else:
                        marketprice= strToNum(marketprice) 
                        marketpricearray.append(marketprice)
                
                #Use the populated arrays to make a new dataframe with the cleaned data (NA values still not corrected at this point)
                new_df['Stock']= stockarray
                new_df['Quantity']= quantityarray
                new_df['UnitCost']= unitcostarray
                new_df['MarketPrice']= marketpricearray
                

                #Replacing NA Values
                #Calculating XOM's Unit Price by using portfolio value and calculating total cash spent
                starting_port_val = 200000 #From Instructions
                
                cash_spent = 0
                
                for i in range(len(new_df)):
                    if new_df['Stock'][i] == 'XOM' and date == '2023-07-31' : 
                        continue 
                    else:
                        cash_spent += (float(new_df['Quantity'][i]) * float(new_df['UnitCost'][i]))
                    
                #replacing NA for XOM's unit cost with value from portfolio cost
                if (date=='2023-07-31'):
                    xom_unitCost = (starting_port_val - cash_spent) / new_df['Quantity'][7]
                    new_df['UnitCost'][7]= xom_unitCost
                
                #replacing the NA for JNJ's market price in September Sheet through yf
                if (date=='2023-09-30'):
                    new_df['MarketPrice'][7] = yf.download('JNJ', '2023-09-29', '2023-09-30')['Adj Close']

                new_df.to_excel(writer, sheet_name=date, index=False)
                
            return new_df
                        
    def asset_value(self):
        #create a list of all the stocks and dates across the 3 sheets in dummy_data.xlsx
        PortfolioAnalysis.clean_data(self)
        stocks = ['AAPL', 'AMZN', 'META', 'MSFT', 'NVDA', 'TSLA', 'GOOG', 'XOM', 'JPM', 'JNJ', 'SPY']
        dates = [ '2023-06-30','2023-07-31', '2023-08-31', '2023-09-30']
        
        av_df = pd.DataFrame(index=dates, columns=stocks)
        
        for date in ['2023-07-31', '2023-08-31', '2023-09-30']:
            clean_df = pd.read_excel('cleaned_data.xlsx', sheet_name=date)
    
    # Group by stock and sum the product of Quantity and MarketPrice (ChatGPT to understand how to merge the differently formatted sheets)
            grouped_data = clean_df.groupby('Stock').apply(lambda x: (x['Quantity'] * x['MarketPrice']).sum())
    
    # Update av_df based on the grouped data
            for stock, value in grouped_data.items():
                av_df.at[date, stock] = value
        
        av_df['NAV'] = av_df.sum(axis=1) #Adding NAV to the dataframe by summing across the rows and displaying sum at the end of the table in a new NAV column
        
        av_df=av_df.fillna(0)
        av_df= av_df.T
    #take the transpose of the dataframe to meet formatting requirements
        return av_df

    def unrealized_returns(self):
        PortfolioAnalysis.asset_value(self)
        stocks = ['AAPL', 'AMZN', 'META', 'MSFT', 'NVDA', 'TSLA', 'GOOG', 'XOM', 'JPM', 'JNJ', 'SPY']
        dates = ['2023-06-30', '2023-07-31', '2023-08-31', '2023-09-30']

#Copy pasted from asset_value method to establish av(asset value) dataframe in this method
        av_df = pd.DataFrame(index=dates, columns=stocks)
        
        for date in ['2023-07-31', '2023-08-31', '2023-09-30']:
            clean_df = pd.read_excel('cleaned_data.xlsx', sheet_name=date)
    
    # Group by stock and sum the product of Quantity and MarketPrice (ChatGPT to understand how to merge the differently formatted sheets)
            grouped_data = clean_df.groupby('Stock').apply(lambda x: (x['Quantity'] * x['MarketPrice']).sum())
    
    # Update av_df based on the grouped data
            for stock, value in grouped_data.items():
                av_df.at[date, stock] = value
        
        av_df['NAV'] = av_df.sum(axis=1) #Adding NAV to the dataframe
        
        av_df=av_df.fillna(0)
        
        av_df= av_df.T
        
#End copy portion


        #Create an empty data frame for unrealized returns
        unrealized_df = pd.DataFrame(index=stocks, columns=dates)
        
        # Loop through the stocks
        for stock in stocks:
        #Calculate unrealized gains/losses for each month through asset value dataframe
            for i in range(1, len(dates)):
                unrealized_df.at[stock, dates[i]] = av_df.at[stock, dates[i]] - av_df.at[stock, dates[i-1]]

        # Fill NaN values with 0
        unrealized_df = unrealized_df.fillna(0)
        
        unrealized_df.loc['Unrealized Returns'] = unrealized_df.sum()
        

        # Return the resulting DataFrame- the dataframe also shows uneralized returns between each stock for each month
        return unrealized_df

    def plot_portfolio(self):
        
        dates= self.asset_values.columns

#plotting the portfolios NAV vs Date
        plt.plot(dates, self.asset_values.loc['NAV'], label='Net Asset Value', linestyle='-')

        # Add labels and legend
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.title('Portfolio Value Over Time')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        
        # Show the plot
        plt.show()

    def plot_liquidity(self):
        # Calculate the ratio between Cash and NAV for each date
        dates= self.asset_values.columns
        liquidity_ratio = self.asset_values.loc['Cash'] / self.asset_values.loc['NAV']

        # Plot the liquidity ratio over time
        plt.plot(dates, liquidity_ratio, marker='o', linestyle='-', color='b')

        # Add labels and title
        plt.xlabel('Date')
        plt.ylabel('Liquidity Ratio')
        plt.title('Liquidity Ratio Over Time')
        plt.grid(True, linestyle='--', alpha=0.7)#ChatGPT to make plot more visually appealing
        plt.tick_params(axis='x', rotation=45)
        plt.tight_layout()

        # Show the plot
        plt.show()
    

if __name__ == "__main__":  # Do not change anything here - this is how we will test your class as well.
    
    fake_port = PortfolioAnalysis("dummy_data.xlsx")
    print(fake_port.asset_values)
    print(fake_port.unrealized_pnl)
    fake_port.plot_portfolio()
    fake_port.plot_liquidity()