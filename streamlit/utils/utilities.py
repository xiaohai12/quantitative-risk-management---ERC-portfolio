import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import seaborn as sns

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



def erc_portfolio(returns, weights_file='erc_weights.csv'):
    """
    Calculate portfolio returns using pre-computed weights from CSV
    """
    # Load weights from CSV
    weights_df = pd.read_csv(weights_file)
    print(f"Loaded weights from {weights_file}")
    
    portfolio_returns_by_year = []
    
    # Iterate through each row in weights_df
    for idx, row in weights_df.iterrows():
        year = int(row['year'])
        print(f"Calculating returns for year {year} (applied to {year+1})...")
        
        # Extract weights and asset names for this year
        weight_dict = row.drop('year').dropna().to_dict()
        columns = list(weight_dict.keys())
        erc_weights_year = np.array(list(weight_dict.values()))
        
        # Get ex-post returns for the next year
        daily_returns_expost = returns.loc[returns.index.year == year + 1]
        
        # Filter to only include assets that were in the training period
        daily_returns_expost = daily_returns_expost[
            daily_returns_expost.columns.intersection(columns)
        ]
        
        # Ensure weights match the available assets
        available_columns = daily_returns_expost.columns.tolist()
        weights = np.array([weight_dict[col] for col in available_columns])
        
        # Normalize weights in case some assets are missing
        weights = weights / np.sum(weights)
        
        # Calculate daily portfolio returns with daily rebalancing
        year_port_daily_returns = []
        
        for t in range(len(daily_returns_expost)):
            # Calculate portfolio return for the current day
            portfolio_return = np.dot(weights, daily_returns_expost.iloc[t])
            year_port_daily_returns.append(portfolio_return)
            
            # Adjust weights for the next day (if it's not the last day)
            if t < len(daily_returns_expost) - 1:
                weights_numerator = weights * (1 + daily_returns_expost.iloc[t])
                weights = weights_numerator / (1 + portfolio_return)
        
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
def cumu_graph(flatportreturns: pd.DataFrame):
    # Set the Seaborn style
    sns.set_theme(style="whitegrid")

    # 1. Calculate cumulative returns
    cumulative_returns_series = (1 + flatportreturns['Daily Returns']).cumprod()

    start_date = cumulative_returns_series.index[0] - pd.Timedelta(days=1)
        
    start_value = pd.Series(1.0, index=[start_date])

    # Combine the start value with the calculated returns
    cumulative_returns_plot = pd.concat([start_value, cumulative_returns_series])

    # 2. Create the figure object
    fig, ax = plt.subplots(figsize=(14, 7))

    # 3. Plot the cumulative returns
    ax.plot(
        cumulative_returns_plot.index, 
        cumulative_returns_plot.values, 
        label='Portfolio Return',
        color='#1f77b4',
        linewidth=1.8
    )

    # 4. Set labels and title (rest of the code is unchanged and good)
    ax.set_title('Cumulative Portfolio Performance', fontsize=18, fontweight='bold', pad=15)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Cumulative Growth (Growth of $1)', fontsize=14)
    
    ax.axhline(y=1.0, color='red', linestyle='--', linewidth=1)
    ax.tick_params(axis='both', which='major', labelsize=12)
    sns.despine(ax=ax, top=True, right=True)
    ax.legend(loc='upper left', frameon=True, fontsize=12)

    # 5. Return the Matplotlib figure object
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



#Mean-Var Portfolio with Weight Tracking
def meanvar_portfolio(combined_returns, risk_aversion):
    combined_returns.index = pd.to_datetime(combined_returns.index)
    risk_aversion_coefficient = risk_aversion
    all_portfolio_returns = []
    all_weights = []  # Store weights with dates and asset names
    
    start_loop_date = pd.Timestamp('2018-01-01')
    end_loop_date = pd.Timestamp('2025-10-01')
    monthly_periods = pd.date_range(start=start_loop_date, end=end_loop_date, freq='MS')
    
    asset_names = [col.replace(" Returns", "") for col in combined_returns.columns]
    
    for month_start in monthly_periods:
        lookback_data = combined_returns.loc[combined_returns.index < month_start].tail(63)
        asset_means_lookback = lookback_data.mean() * 252
        annualized_cov_matrix_lookback = lookback_data.cov() * 252
        num_assets = len(asset_means_lookback)
        initial_weights = np.array([1 / num_assets] * num_assets)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0, 1) for _ in range(num_assets))
        
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
        
        next_month_start = month_start + pd.DateOffset(months=1)
        combined_returns_expost = combined_returns.loc[
            (combined_returns.index >= month_start) & (combined_returns.index < next_month_start)
        ]
        
        weights = optimal_weights
        month_port_daily_returns = []
        
        # Store initial weights for this month
        weight_dict = {'date': month_start}
        for i, asset in enumerate(asset_names):
            weight_dict[asset] = weights[i]
        all_weights.append(weight_dict)
        
        for t in range(len(combined_returns_expost)):
            portfolio_return = np.dot(weights, combined_returns_expost.iloc[t])
            month_port_daily_returns.append(portfolio_return)
            
            if t < len(combined_returns_expost) - 1:
                weights_numerator = weights * (1 + combined_returns_expost.iloc[t])
                weights = weights_numerator / (1 + portfolio_return)
        
        all_portfolio_returns.append(month_port_daily_returns)
    
    # Convert weights to DataFrame
    weights_df = pd.DataFrame(all_weights)
    weights_df.set_index('date', inplace=True)
    
    return all_portfolio_returns, weights_df




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


def riskscore_to_aversion(risk_score):

    # Define the mapping
    aversion_map = {
        0: 200,
        1: 130,
        2: 80,
        3: 50,
        4: 30,
        5: 20,
        6: 10,
        7: 5,
        8: 1,
        9: 0.5,
        10: 0
    }
    
    return aversion_map[risk_score]


def plot_portfolio_composition(weights_df, title="Portfolio Composition Over Time"):
    """
    Creates a pie chart showing average portfolio composition.
   
    """
    import matplotlib.pyplot as plt
    
    # Calculate average weights across all periods
    avg_weights = weights_df.mean()
    
    # Filter out assets with very small average weights (< 0.5%)
    significant_weights = avg_weights[avg_weights > 0.005]
    other_weight = avg_weights[avg_weights <= 0.005].sum()
    
    if other_weight > 0:
        significant_weights['Other'] = other_weight
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = plt.cm.Set3(range(len(significant_weights)))
    
    wedges, texts, autotexts = ax.pie(
        significant_weights.values,
        labels=significant_weights.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 10}
    )
    
    # Enhance text visibility
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    return fig











        
