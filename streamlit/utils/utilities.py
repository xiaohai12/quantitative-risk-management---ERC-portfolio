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
    
    returns['Date'] = pd.to_datetime(returns['Date'])
    returns.set_index('Date', inplace=True)
    
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
    
    returns['Date'] = pd.to_datetime(returns['Date'])
    returns.set_index('Date', inplace=True)
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



def calculate_drawdown(portfolio_returns):
    """
    Calculate drawdown series and key drawdown metrics
   
    """
    # Flatten returns if nested list
    if isinstance(portfolio_returns, list):
        flat_returns = [ret for month in portfolio_returns for ret in month]
        returns_series = pd.Series(flat_returns)
    else:
        returns_series = portfolio_returns
    
    # Calculate cumulative wealth
    cumulative_wealth = (1 + returns_series).cumprod()
    
    # Calculate running maximum
    running_max = cumulative_wealth.cummax()
    
    # Calculate drawdown
    drawdown_series = (cumulative_wealth - running_max) / running_max
    
    # Maximum drawdown
    max_drawdown = drawdown_series.min()
    
    # Find drawdown periods
    in_drawdown = drawdown_series < 0
    drawdown_periods = []
    
    if in_drawdown.any():
        # Identify separate drawdown episodes
        drawdown_start = None
        for i, is_dd in enumerate(in_drawdown):
            if is_dd and drawdown_start is None:
                drawdown_start = i
            elif not is_dd and drawdown_start is not None:
                drawdown_end = i - 1
                dd_period = drawdown_series.iloc[drawdown_start:drawdown_end+1]
                drawdown_periods.append({
                    'start_idx': drawdown_start,
                    'end_idx': drawdown_end,
                    'duration': drawdown_end - drawdown_start + 1,
                    'depth': dd_period.min(),
                    'recovery_idx': i if cumulative_wealth.iloc[i] >= running_max.iloc[drawdown_start] else None
                })
                drawdown_start = None
        
        # Handle if still in drawdown at end
        if drawdown_start is not None:
            dd_period = drawdown_series.iloc[drawdown_start:]
            drawdown_periods.append({
                'start_idx': drawdown_start,
                'end_idx': len(drawdown_series) - 1,
                'duration': len(drawdown_series) - drawdown_start,
                'depth': dd_period.min(),
                'recovery_idx': None  # Not recovered yet
            })
    
    # Create DataFrame of drawdown periods
    if drawdown_periods:
        drawdown_info = pd.DataFrame(drawdown_periods)
        drawdown_info = drawdown_info.sort_values('depth').head(5)
    else:
        drawdown_info = pd.DataFrame()
    
    # Maximum drawdown duration
    max_dd_duration = max([dp['duration'] for dp in drawdown_periods]) if drawdown_periods else 0
    
    return drawdown_series, max_drawdown, max_dd_duration, drawdown_info


def plot_drawdown(portfolio_returns, dates=None):
    """
    Plot only the drawdown visualization.
    """
    # 1. Calculate drawdown and associated metrics
    drawdown_series, max_dd, max_duration, dd_info = calculate_drawdown(portfolio_returns)
    
    # 2. Flatten returns (Kept for robust handling of input format)
    if isinstance(portfolio_returns, list):
        # Flatten list of lists
        flat_returns = [ret for month in portfolio_returns for ret in month]
        returns_series = pd.Series(flat_returns)
    else:
        # Use the input directly if it's already a Series/DataFrame
        returns_series = portfolio_returns
    
    # We use a figsize that is wider and shorter, suitable for a single plot.
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    
    # 4. Drawdown Series Plot (Adapted from the original ax2)
    ax.fill_between(
        range(len(drawdown_series)),
        drawdown_series.values * 100, # Drawdown values as percentage
        0,                             # Fill down to the zero line
        alpha=0.5, 
        color='red'
    )
    ax.plot(drawdown_series.values * 100, color='darkred', linewidth=1.5)
    
    # 5. Set labels and title
    ax.set_ylabel('Drawdown (%)', fontsize=12)
    ax.set_xlabel('Trading Days', fontsize=12)
    ax.set_title(
        f'Drawdown Over Time (Max DD: {max_dd*100:.2f}%, Max Duration: {max_duration} days)',
        fontsize=20, 
        fontweight='bold'
    )
    
    # 6. Add grid and zero line
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    plt.tight_layout()
    plt.show()



def calculate_risk_contribution(weights_df, combined_returns):
    """
    Calculate marginal and component risk contributions for each asset

    """
    combined_returns.index = pd.to_datetime(combined_returns.index)
    asset_names = [col.replace(" Returns", "") for col in combined_returns.columns]
    
    risk_contributions = []
    
    for date in weights_df.index:
        # Get weights for this period
        weights = weights_df.loc[date].values
        
        # Get lookback data (same 63-day window as optimization)
        lookback_data = combined_returns.loc[combined_returns.index < date].tail(63)
        
        if len(lookback_data) < 63:
            continue
        
        # Calculate covariance matrix (annualized)
        cov_matrix = lookback_data.cov().values * 252
        
        # Portfolio variance
        portfolio_variance = np.dot(weights, np.dot(cov_matrix, weights))
        portfolio_vol = np.sqrt(portfolio_variance)
        
        # Marginal contribution to risk (MCR)
        # MCR_i = (Cov * w) / portfolio_vol
        marginal_contrib = np.dot(cov_matrix, weights) / portfolio_vol
        
        # Component contribution to risk (CCR)
        # CCR_i = w_i * MCR_i
        component_contrib = weights * marginal_contrib
        
        # Percentage contribution to risk
        pct_contrib = component_contrib / portfolio_vol * 100
        
        # Store results
        contrib_dict = {
            'date': date,
            'portfolio_vol': portfolio_vol * 100  # Convert to percentage
        }
        
        for i, asset in enumerate(asset_names):
            contrib_dict[f'{asset}_weight'] = weights[i] * 100
            contrib_dict[f'{asset}_risk_contrib'] = pct_contrib[i]
            contrib_dict[f'{asset}_mcr'] = marginal_contrib[i] * 100
        
        risk_contributions.append(contrib_dict)
    
    risk_contrib_df = pd.DataFrame(risk_contributions)
    risk_contrib_df.set_index('date', inplace=True)
    
    return risk_contrib_df


def plot_risk_contribution(risk_contrib_df: pd.DataFrame, combined_returns: pd.DataFrame):
    """
    Visualize the AVERAGE risk contributions by asset (Bar Plot only).
    """
    
    # 1. Data Preparation (Identical to original function)
    asset_names = [col.replace(" Returns", "") for col in combined_returns.columns]
    
    # Extract risk contribution columns and rename
    risk_cols = [col for col in risk_contrib_df.columns if col.endswith('_risk_contrib')]
    risk_data = risk_contrib_df[risk_cols]
    risk_data.columns = [col.replace('_risk_contrib', '') for col in risk_data.columns]
    
    # Calculate average risk contribution
    avg_risk = risk_data.mean()
    
    # 2. Create the Figure (Single Subplot)
    fig, ax = plt.subplots(figsize=(12, 6)) # Adjusted size for a cleaner single plot
    
    # 3. Plot 1: Average Risk Contribution by Asset (Bar Plot)
    x_pos = np.arange(len(asset_names))
    bars = ax.bar(x_pos, avg_risk.values, alpha=0.8, edgecolor='black', linewidth=1.0)
    
    # Sticking to original logic (normalized by max):
    colors = plt.cm.RdYlGn_r(avg_risk.values / avg_risk.max()) 
    
    for bar, color in zip(bars, colors):
        bar.set_color(color)
        
    ax.set_xticks(x_pos)
    ax.set_xticklabels(asset_names, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Average Risk Contribution (%)', fontsize=12, fontweight='bold')
    ax.set_title('Average Risk Contribution by Asset', fontsize=16, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, axis='y')
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    # Add value labels on bars
    for i, (bar, val) in enumerate(zip(bars, avg_risk.values)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}%',
                ha='center', va='bottom' if height >= 0 else 'top',
                fontsize=9, fontweight='bold', color='black')
    
    # 4. Final Formatting
    plt.tight_layout()
    plt.show()


def cumu_graph_vol(flatportreturns: pd.DataFrame):
    """
    Create enhanced portfolio performance visualization with cumulative returns and rolling volatility.
    
    """
    # Set modern style
    sns.set_theme(style="white")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    
    # Calculate cumulative returns
    cumulative_returns_series = (1 + flatportreturns['Daily Returns']).cumprod()
    start_date = cumulative_returns_series.index[0] - pd.Timedelta(days=1)
    start_value = pd.Series(1.0, index=[start_date])
    cumulative_returns_plot = pd.concat([start_value, cumulative_returns_series])
    
    # Calculate rolling volatility (30-day annualized)
    rolling_vol = flatportreturns['Daily Returns'].rolling(window=30).std() * np.sqrt(252) * 100
    
    # Create figure with two subplots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.5, 1], hspace=0.25)
    
    # ===== SUBPLOT 1: Cumulative Returns =====
    ax1 = fig.add_subplot(gs[0])
    
    # Create gradient effect using fill_between
    ax1.fill_between(
        cumulative_returns_plot.index,
        1.0,
        cumulative_returns_plot.values,
        where=(cumulative_returns_plot.values >= 1.0),
        alpha=0.15,
        color='#2ecc71',
        label='_nolegend_'
    )
    ax1.fill_between(
        cumulative_returns_plot.index,
        1.0,
        cumulative_returns_plot.values,
        where=(cumulative_returns_plot.values < 1.0),
        alpha=0.15,
        color='#e74c3c',
        label='_nolegend_'
    )
    
    # Main line plot with improved styling
    ax1.plot(
        cumulative_returns_plot.index,
        cumulative_returns_plot.values,
        label='Portfolio Value',
        color='#3498db',
        linewidth=2.5,
        alpha=0.9
    )
    
    # Baseline at 1.0
    ax1.axhline(y=1.0, color='#95a5a6', linestyle='--', linewidth=1.5, alpha=0.7, label='Initial Investment')
    
    # Calculate and display key metrics
    final_value = cumulative_returns_plot.values[-1]
    total_return = (final_value - 1) * 100
    
    # Add text box with performance metrics
    textstr = f'Total Return: {total_return:+.2f}%\nFinal Value: ${final_value:.2f}'
    props = dict(boxstyle='round,pad=0.8', facecolor='white', alpha=0.9, edgecolor='#bdc3c7', linewidth=1.5)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=11,
             verticalalignment='top', bbox=props, family='monospace')
    
    # Styling
    ax1.set_title('Cumulative Portfolio Performance', fontsize=14, fontweight='bold', pad=20, color='#2c3e50')
    ax1.set_xlabel('Date', fontsize=13, fontweight='600', color='#34495e')
    ax1.set_ylabel('Cumulative Growth (Growth of $1)', fontsize=13, fontweight='600', color='#34495e')
    ax1.tick_params(axis='both', which='major', labelsize=11, colors='#34495e')
    ax1.grid(True, alpha=0.25, linestyle='-', linewidth=0.8, color='#bdc3c7')
    ax1.set_facecolor('#f8f9fa')
    ax1.legend(loc='upper left', frameon=True, fontsize=11, shadow=True, fancybox=True)
    
    # Format y-axis as currency
    from matplotlib.ticker import FuncFormatter
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'${y:.2f}'))
    
    # ===== SUBPLOT 2: Rolling Volatility =====
    ax2 = fig.add_subplot(gs[1])
    
    # Plot volatility with gradient fill
    ax2.plot(
        rolling_vol.index,
        rolling_vol.values,
        color='#e67e22',
        linewidth=2.5,
        alpha=0.9,
        label='30-Day Rolling Volatility'
    )
    
    ax2.fill_between(
        rolling_vol.index,
        0,
        rolling_vol.values,
        alpha=0.2,
        color='#e67e22'
    )
    
    # Add mean volatility line
    mean_vol = rolling_vol.mean()
    ax2.axhline(y=mean_vol, color='#c0392b', linestyle='--', linewidth=1.5, 
                alpha=0.7, label=f'Mean Volatility: {mean_vol:.2f}%')
    
    # Calculate current volatility
    current_vol = rolling_vol.iloc[-1]
    textstr_vol = f'Current Vol: {current_vol:.2f}%\nMean Vol: {mean_vol:.2f}%'
    ax2.text(0.02, 0.98, textstr_vol, transform=ax2.transAxes, fontsize=11,
             verticalalignment='top', bbox=props, family='monospace')
    
    # Styling
    ax2.set_title('Portfolio Volatility (Annualized)', fontsize=15, fontweight='bold', pad=15, color='#2c3e50')
    ax2.set_xlabel('Date', fontsize=13, fontweight='600', color='#34495e')
    ax2.set_ylabel('Volatility (%)', fontsize=13, fontweight='600', color='#34495e')
    ax2.tick_params(axis='both', which='major', labelsize=11, colors='#34495e')
    ax2.grid(True, alpha=0.25, linestyle='-', linewidth=0.8, color='#bdc3c7')
    ax2.set_facecolor('#f8f9fa')
    ax2.legend(loc='upper left', frameon=True, fontsize=11, shadow=True, fancybox=True)
    
    # Format y-axis with percentage
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}%'))
    
    # Add subtle border to entire figure
    fig.patch.set_facecolor('white')
    fig.patch.set_edgecolor('#bdc3c7')
    fig.patch.set_linewidth(2)
    
    plt.tight_layout()
    
    return fig

        
