import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def dailyreturns(dailyprice) :

    if 'Date' in dailyprice.columns :
        # Set Date to index
        dailyprice['Date'] = pd.to_datetime(dailyprice['Date'])
        dailyprice = dailyprice.set_index('Date')
        
        # Calculate daily returns
        daily_returns = dailyprice.pct_change(fill_method='ffill')
    
        # Drop first line
        daily_returns = daily_returns.iloc[1:]
    
        # Convert the index to datetime objects
        daily_returns.index = pd.to_datetime(daily_returns.index)
    
        return daily_returns 

    else :
        
        # Calculate daily returns
        daily_returns = dailyprice.pct_change(fill_method='ffill')
    
        # Drop first line
        daily_returns = daily_returns.iloc[1:]
    
        # Convert the index to datetime objects
        daily_returns.index = pd.to_datetime(daily_returns.index)
    
        return daily_returns


#Functions for Optimization

# Define a function to calculate the portfolio risk (standard deviation)
def portfolio_risk(weights, cov_matrix):

    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

# Define a function to calculate the risk contribution of each asset in the portfolio
def risk_contribution(weights, cov_matrix):

    portfolio_std = portfolio_risk(weights, cov_matrix)
    # Marginal contribution to risk
    marginal_contribution = np.dot(cov_matrix, weights) / portfolio_std
    # Risk contribution
    risk_contrib = weights * marginal_contribution
    return risk_contrib

# Define a function to minimize, which aims to equalize the risk contributions
def objective_function(weights, cov_matrix):

    risk_contribs = risk_contribution(weights, cov_matrix)
    # We want all risk contributions to be equal, so minimize the sum of squared differences
    # from the average risk contribution.
    return np.sum((risk_contribs - np.mean(risk_contribs))**2)*1000


#ERC Portfolio
def erc_portfolio(returns):

    # store cumulative returns for each year
    portfolio_returns_by_year = []

    # Iterate through the years from 2016 to 2025
    for year in range(2016, 2025):

        # Filter data for the current year
        daily_returns_year = returns.loc[returns.index.year == year]

        # Drop columns with any NaN values in this year
        daily_returns_year = daily_returns_year.dropna(axis=1)

        # Store the column names for the current year
        columns = daily_returns_year.columns

        covariance_matrix_year = daily_returns_year.cov()

        # Calculate ERC weights for the current year
        num_assets_year = len(covariance_matrix_year.columns)
        initial_weights_year = np.array(num_assets_year * [1. / num_assets_year])

        constraints_year = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
        bounds_year = tuple((0, 1) for asset in range(num_assets_year))
        options = {'ftol': 1e-8, 'maxiter': 1000}


        result_year = minimize(objective_function, initial_weights_year, args=(covariance_matrix_year,),
                                  method='SLSQP', bounds=bounds_year, constraints=constraints_year,
                                  options=options, tol=1e-10)

        erc_weights_year = result_year.x

        #Calculate the daily portfolio returns for the current year using the weights
        daily_returns_expost = returns.loc[returns.index.year == year+1]
        daily_returns_expost = daily_returns_expost[daily_returns_expost.columns.intersection(columns)]

        weights = erc_weights_year
        year_port_daily_returns = []

        for t in range(len(daily_returns_expost)):
            # Calculate portfolio return for the current day
            firstportfolio_return = np.dot(weights, daily_returns_expost.iloc[t])

            year_port_daily_returns.append(firstportfolio_return)

            # Adjust weights for the next day (if it's not the last day)
            if t < len(daily_returns_expost)-1:
                weights_numerator = weights * (1 + daily_returns_expost.iloc[t])
                weights = weights_numerator / (1 + firstportfolio_return)


        portfolio_returns_by_year.append(year_port_daily_returns)

    return portfolio_returns_by_year


#Performance of Porfolio
def erc_performance(portreturns, returns , startyear):


    # Flatten the list of daily returns into a single list
    flattened_returns = [item for sublist in portreturns for item in sublist]

    # Create a DataFrame from the flattened list
    flattened_returns_df = pd.DataFrame(flattened_returns, columns=['Daily Returns'])

    # Extract indexes to add to df
    daily_returns_start_onwards = returns[returns.index.year >= returns.index.year[0]+1]
    daily_returns_start_onwards_index = daily_returns_start_onwards.index

    # Set the index of flattened_returns_df and convert to date objects
    flattened_returns_df.index = daily_returns_start_onwards_index

    # Set start date
    flattened_returns_df = flattened_returns_df[flattened_returns_df.index.year >= startyear]

    # Assuming 252 trading days in a year
    trading_days_per_year = 252

    # 1. Annualized Average Return
    daily_average_return = flattened_returns_df['Daily Returns'].mean()
    annualized_average_return = daily_average_return * trading_days_per_year

    # 2. Annualized Volatility
    daily_volatility = flattened_returns_df['Daily Returns'].std()
    annualized_volatility = daily_volatility * np.sqrt(trading_days_per_year)

    # 3. Sharpe Ratio (assuming a risk-free rate of 0 for simplicity)
    risk_free_rate = 0.015
    sharpe_ratio = (annualized_average_return - risk_free_rate) / annualized_volatility

    # 4. Cumulative Return
    cumulative_return = (1 + flattened_returns_df['Daily Returns']).prod() - 1


    return flattened_returns_df, annualized_average_return, annualized_volatility, sharpe_ratio, cumulative_return




#Performance of PBonds
def bonds_performance(bonds_returns, startyear):

    returns = bonds_returns.rename(columns={'AGG': 'Daily Returns'})
    
    returns = returns[returns.index.year >= startyear]
    
    # Assuming 252 trading days in a year
    trading_days_per_year = 252
    
    # 1. Annualized Average Return
    daily_average_return = returns['Daily Returns'].mean()
    annualized_average_return = daily_average_return * trading_days_per_year
    
    # 2. Annualized Volatility
    daily_volatility = returns['Daily Returns'].std()
    annualized_volatility = daily_volatility * np.sqrt(trading_days_per_year)
    
    # 3. Sharpe Ratio (assuming a risk-free rate of 0.015)
    risk_free_rate = 0.015
    sharpe_ratio = (annualized_average_return - risk_free_rate) / annualized_volatility
    
    # 4. Cumulative Return
    cumulative_return = (1 + returns['Daily Returns']).prod() - 1

    return returns, annualized_average_return, annualized_volatility, sharpe_ratio, cumulative_return

    
   

# Graph of cumulative return
def cumu_graph(flatportreturns):
    # Calculate cumulative returns
    cumulative_returns_plot = (1 + flatportreturns['Daily Returns']).cumprod()

    # Create the figure object
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the cumulative returns on the axes
    ax.plot(cumulative_returns_plot.index, cumulative_returns_plot.values)
    
    # Set labels and title on the axes
    ax.set_title('Cumulative Portfolio Returns')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Return')
    ax.grid(True)
   
    # Return the Matplotlib figure object
    return fig

    

# Define Optimization Functions (Utility Maximization) ---
def port_return(weights, means):
    """Calculates the portfolio return."""
    return np.dot(weights, means)

def port_volatility(weights, cov_matrix):
    """Calculates the portfolio volatility."""
    return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

def negative_utility_function(weights, means, cov_matrix, risk_aversion_coeff):
    """
    Calculates the negative of the utility function to be minimized..
    """
    p_return = port_return(weights, means)
    p_volatility = port_volatility(weights, cov_matrix)
    p_variance = p_volatility**2

    utility = p_return - 0.5 * risk_aversion_coeff * p_variance
    return -utility


#Combine and choose asset classes for portoflio
def combine_returns(equity, equityESG, commodity, commodityESG, crypto, bonds, choice):
    dfs_to_concat = []
    df_names = ['Equity Returns', 'EquityESG Returns', 'Commodity Returns', 'CommodityESG Returns', 'Crypto Returns', 'Bonds Returns']
    input_dfs = [equity, equityESG, commodity, commodityESG, crypto, bonds]

    # Iterate through the choice list and corresponding input DataFrames
    for i, include in enumerate(choice):
        if include == 1:
            current_df = input_dfs[i]
            current_name = df_names[i]

            if current_df is not None:
                # Rename the 'Daily Returns' column to a unique name for concatenation
                renamed_df = current_df.rename(columns={'Daily Returns': current_name})
                dfs_to_concat.append(renamed_df)
            else:
                # Warn if a DataFrame is requested but not provided
                print(f"Warning: choice[{i}] is 1 but {current_name} DataFrame was not provided (is None). Skipping this asset.")

    if not dfs_to_concat:
        raise ValueError("No DataFrames selected for combination based on the 'choice' variable.")

    # Concatenate the selected and renamed dataframes along the columns
    combined_returns = pd.concat(dfs_to_concat, axis=1)

    # Drop rows with any NaN values
    combined_returns = combined_returns.dropna()

    # Ensure the index is in datetime format
    combined_returns.index = pd.to_datetime(combined_returns.index)

    return combined_returns



#Mean-Var Portfolio
def meanvar_portfolio(combined_returns,risk_aversion):

    combined_returns.index = pd.to_datetime(combined_returns.index) # Ensure datetime index

    # Define the risk_aversion_coefficient.
    risk_aversion_coefficient = risk_aversion

    all_monthly_portfolio_returns = [] # List to store daily returns for each monthly period

    # Define the start and end dates for the monthly loop
    start_loop_date = pd.Timestamp('2018-01-01')
    end_loop_date = pd.Timestamp('2025-10-01') # Loop until October 2025

    # Generate a sequence of month start dates
    monthly_periods = pd.date_range(start=start_loop_date, end=end_loop_date, freq='MS')

    # Loop through each month
    for month_start in monthly_periods:

        # Define the lookback period
        lookback_data = combined_returns.loc[combined_returns.index < month_start].tail(63)

        # Calculate annualized mean returns and annualized covariance matrix
        asset_means_lookback = lookback_data.mean() * 252
        annualized_cov_matrix_lookback = lookback_data.cov() * 252

        num_assets = len(asset_means_lookback)
        initial_weights = np.array([1 / num_assets] * num_assets)

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))

        # Optimization for optimal weights for the current month, based on lookback data
        optimization_result = minimize(
            negative_utility_function,
            initial_weights,
            args=(asset_means_lookback.values, annualized_cov_matrix_lookback.values, risk_aversion_coefficient),
            method='SLSQP',
            bounds=bounds,
            constraints=constraints,
            tol=1e-20
        )

        optimal_weights = optimization_result.x


        # Get daily returns for the current month
        next_month_start = month_start + pd.DateOffset(months=1)
        combined_returns_expost = combined_returns.loc[(combined_returns.index >= month_start) & (combined_returns.index < next_month_start)]

        weights = optimal_weights
        month_port_daily_returns = [] # Changed name to reflect monthly loop

        for t in range(len(combined_returns_expost)):
            # Calculate portfolio return for the current day
            portfolio_return = np.dot(weights, combined_returns_expost.iloc[t])

            month_port_daily_returns.append(portfolio_return)

            # Adjust weights for the next day (if it's not the last day)
            if t < len(combined_returns_expost)-1:
                weights_numerator = weights * (1 + combined_returns_expost.iloc[t])
                weights = weights_numerator / (1 + portfolio_return)

        all_monthly_portfolio_returns.append(month_port_daily_returns)

    return all_monthly_portfolio_returns




def equity_to_esg(equity_data) : 

    #list of commonly excluded firms of green fonds
    excluded = [ 'MO', 'PM', 'XOM', 'CVX', 'COP', 'EOG', 'SLB', 'MPC', 'PSX', 'VLO', 'OXY', 'HES', 'DVN', 'FANG', 'MRO', 'APA', 'HAL', 'BKR', 'TRGP', 'WMB', 'KMI', 'OKE', 'LNG', 'EQT', 'CTRA', 'CF', 'MOS', 'CCJ', 'FCX', 'NEM', 'NUE', 'STLD', 'LMT', 'RTX', 'NOC', 'GD', 'BA', 'LHX', 'HWM', 'TXT', 'TSLA', 'META', 'GOOGL', 'GOOG', 'AMZN', 'NFLX', 'ORCL', 'CRM', 'INTC', 'AMD', 'NVDA', 'QCOM', 'AVGO', 'TXN', 'ADI', 'NKE', 'SBUX', 'MCD', 'YUM', 'CMG', 'DRI', 'GM', 'F', 'JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'DHR', 'ABT', 'BMY', 'AMGN', 'GILD', 'CVS', 'CI', 'BRK.B', 'JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'SCHW', 'USB', 'PNC', 'TFC', 'AXP', 'COF', 'DFS', 'NEE', 'DUK', 'SO', 'D', 'EXC', 'AEP', 'XEL', 'ED']
    
    # Filter equity_data to exclude the columns present in excluded_tickers
    equity_data_esg = equity_data.drop(columns=excluded, errors='ignore')
    
    return equity_data_esg
    

def commodity_to_esg(commodity_data) : 

    #list of  excluded commodity
    excluded_commo = [ 'CL=F', 'BZ=F','NG=F','HO=F','RB=F']
    
    # Filter commo_data to exclude the columns present in excluded_tickers
    commodity_data_esg = commodity_data.drop(columns=excluded_commo, errors='ignore')

    return commodity_data_esg













        
