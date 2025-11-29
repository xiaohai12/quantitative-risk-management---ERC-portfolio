def importer_data(start='2016-01-01',end='2025-11-01'):
    import yfinance as yf
    import os
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    import utils.utilities as ut
    import requests
    import pandas as pd
    import time
    from scipy.optimize import minimize
    import numpy as np
    
    # Equity
    def import_equity(start_date, end_date):
        sp500_tickers = ['A', 'AAL', 'AAPL', 'ABBV', 'ABNB', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM','ADP', 'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'AON', 'AOS', 'APA', 'APD', 'APH', 'APO', 'APP', 'APTV', 'ARE', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXON', 'AXP', 'AZO', 'BA', 'BAC', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF-B', 'BIIB', 'BK', 'BKNG', 'BLK', 'BMY', 'BR', 'BRK-B', 'BSX', 'BWA', 'BX', 'BXP', 'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CCL', 'CDNS', 'CDW', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COIN', 'COO', 'COP', 'COR', 'COST', 'CPB', 'CPRT', 'CPT', 'CRL', 'CRM', 'CRWD', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTRA', 'CTSH', 'CVS', 'CVX', 'D', 'DAL', 'DASH', 'DD', 'DE', 'DECK', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EG', 'EIX', 'EL', 'ELV', 'EME',  'EMN', 'EMR', 'EOG', 'EPAM', 'EQIX', 'EQT', 'ERJ', 'ES', 'ESS', 'ETN',  'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FAST', 'FCX', 'FDS', 'FDX', 'FE', 'FFIV', 'FI', 'FICO', 'FIS', 'FITB', 'FMC', 'FOX', 'FOXA', 'FRT', 'FSLR', 'FTNT', 'FTV', 'GD', 'GE', 'GEHC', 'GEV', 'GEN', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC',
            'GPN', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HOOD', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUBB', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF',  'ILMN', 'INCY', 'INTC', 'INTU', 'INVH', 'IP', 'IPG', 'IQV', 'IR', 'IRM',  'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBL', 'JCI', 'JKHY', 'JNJ', 'JPM', 'K', 'KDP', 'KHC', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR', 'KVUE', 'L', 'LDOS', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNT', 'LOW', 'LRCX', 'LULU', 'LUV', 'LVS', 'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH',  'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE', 'NEM', 'NFLX',  'NI', 'NKE', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OKE', 'OMC', 'ON', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PANW', 'PAYC', 'PAYX', 'PCAR', 'PCG',
            'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PLD', 'PLTR', 'PM', 'PNC', 'PNR', 'PNW', 'PODD', 'PPG', 'PPL', 'PRU', 'PSX', 'PTC', 'PWR', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX', 'RVTY', 'SBUX', 'SCHW', 'SHW', 'SJM', 'SLB', 'SMCI', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STLD', 'STT', 'STX', 'STZ', 'SWK', 'SWKS',  'SYF', 'SYK', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC',  'TFX', 'TGT', 'TJX', 'TKO', 'TMUS', 'TMO', 'TPR', 'TRGP', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TT', 'TTWO', 'TXN', 'TXT', 'UAL', 'UBER', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VEEV', 'VLO', 'VLTO', 'VMC', 'VRSK', 'VRSN', 'VRTX', 'VST', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBD', 'WCN', 'WDC', 'WEC', 'WELL', 'WFC', 'WM', 'WMB', 'WMT', 'WRB', 'WST', 'WY', 'WYNN', 'XEL', 'XOM', 'XRAY', 'XYL', 'YUM',
            'ZBH', 'ZBRA', 'ZTS' ]

        equity_data = yf.download(sp500_tickers, start=start_date, end=end_date)['Close']

        equity_data.to_csv('equity_data.csv')

    # Cryptos
    def import_cryptos(start_date, end_date):
        crypto_tickers = [
            # --- Top Tier (High Market Cap & Volume) ---
            'BTC-USD',  # Bitcoin
            'ETH-USD',  # Ethereum
            'BNB-USD',  # BNB (Binance Coin)
            'SOL-USD',  # Solana
            'XRP-USD',  # XRP
            'DOGE-USD',  # Dogecoin
            'ADA-USD',  # Cardano
            'AVAX-USD',  # Avalanche
            'DOT-USD',  # Polkadot
            'LINK-USD',  # Chainlink

            # --- Other High-Volume/Major Ecosystem Coins ---
            'TRX-USD',  # TRON
            'LTC-USD',  # Litecoin
            'BCH-USD',  # Bitcoin Cash
            'XLM-USD',  # Stellar
            'SHIB-USD',  # Shiba Inu
            'TON-USD',  # Toncoin
            'ICP-USD',  # Internet Computer
            'NEAR-USD',  # NEAR Protocol
            'XMR-USD',  # Monero
            'VET-USD',  # VeChain
            'ATOM-USD',  # Cosmos
            'DASH-USD',  # Dash
            'ZEC-USD',  # Zcash

            # --- DeFi, Gaming, and Web3 Majors ---
            'AAVE-USD',  # Aave
            'FIL-USD',  # Filecoin
            'ETC-USD',  # Ethereum Classic
        ]

        crypto_data = yf.download(crypto_tickers, start=start_date, end=end_date)['Close']
        crypto_data = crypto_data.reset_index()

        # Clean crypto to adjust trading days
        crypto_data['Date'] = pd.to_datetime(crypto_data['Date'])
        crypto_data = crypto_data.set_index('Date')

        # Load equity data to match dates
        equity_data = pd.read_csv('equity_data.csv')
        equity_data['Date'] = pd.to_datetime(equity_data['Date'])
        crypto_data = crypto_data.loc[crypto_data.index.isin(equity_data['Date'])]

        crypto_data.to_csv('cryptos_data.csv')

    # Commodities
    def import_commodities(start_date, end_date):
        commodity_tickers = [
            # Energy
            'CL=F',  # WTI Crude Oil
            'BZ=F',  # Brent Crude Oil
            'NG=F',  # Natural Gas
            'HO=F',  # Heating Oil
            'RB=F',  # RBOB Gasoline

            # Precious Metals
            'GC=F',  # Gold
            'SI=F',  # Silver
            'PL=F',  # Platinum
            'PA=F',  # Palladium

            # Industrial Metals
            'HG=F',  # Copper
            'ALI=F',  # Aluminum
            'TIO=F',  # Iron Ore

            # Agriculture
            'ZC=F',  # Corn
            'ZS=F',  # Soybeans
            'ZW=F',  # Wheat

            # Softs
            'KC=F',  # Coffee
            'SB=F',  # Sugar
            'CC=F',  # Cocoa
            'CT=F',  # Cotton
            'OJ=F',  # Frozen Concentrated Orange Juice

            # Livestock
            'LE=F',  # Live Cattle
            'HE=F',  # Lean Hogs
            'GF=F',  # Feeder Cattle
        ]

        commodities_data = yf.download(commodity_tickers, start=start_date, end=end_date)['Close']
        commodities_data.to_csv('commodities_data.csv')

    # ETF Bonds
    def import_bonds(start_date, end_date):
        agg_close = yf.download('AGG', start_date, end_date)['Close']
        agg_close.to_csv('bonds_data.csv')

    import_equity(start_date=start, end_date=end)
    import_cryptos(start_date=start, end_date=end)
    import_commodities(start_date=start, end_date=end)
    import_bonds(start_date=start, end_date=end)

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    equity_data = pd.read_csv(BASE_DIR + "/equity_data.csv")
    commodity_data = pd.read_csv(BASE_DIR + "/commodities_data.csv")
    crypto_data = pd.read_csv(BASE_DIR + "/cryptos_data.csv")
    bonds_data = pd.read_csv(BASE_DIR + "/bonds_data.csv")

    equity_data_esg = ut.equity_to_esg(equity_data)
    commodity_data_esg = ut.commodity_to_esg(commodity_data)

    equity_data_esg.to_csv(BASE_DIR + "/equity_data_esg.csv")
    commodity_data_esg.to_csv(BASE_DIR + "/commodity_data_esg.csv")

    # Compute daily returns
    equity_returns = ut.dailyreturns(equity_data)
    equity_esg_returns = ut.dailyreturns(equity_data_esg)
    commodity_returns = ut.dailyreturns(commodity_data)
    commodity_esg_returns = ut.dailyreturns(commodity_data_esg)
    crypto_returns = ut.dailyreturns(crypto_data)
    bonds_returns = ut.dailyreturns(bonds_data)

    # Save returns as CSV
    equity_returns.to_csv(BASE_DIR + "/equity_returns.csv")
    equity_esg_returns.to_csv(BASE_DIR + "/equity_esg_returns.csv")
    commodity_returns.to_csv(BASE_DIR + "/commodity_returns.csv")
    commodity_esg_returns.to_csv(BASE_DIR + "/commodity_esg_returns.csv")
    crypto_returns.to_csv(BASE_DIR + "/crypto_returns.csv")
    bonds_returns.to_csv(BASE_DIR + "/bonds_returns.csv")


    # Com^pute ERC weights
    def portfolio_risk(weights, cov_matrix):
        """Calculate the portfolio risk (standard deviation)"""
        return np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    def risk_contribution(weights, cov_matrix):
        """Calculate the risk contribution of each asset in the portfolio"""
        portfolio_std = portfolio_risk(weights, cov_matrix)
        # Marginal contribution to risk
        marginal_contribution = np.dot(cov_matrix, weights) / portfolio_std
        # Risk contribution
        risk_contrib = weights * marginal_contribution
        return risk_contrib
    
    def objective_function(weights, cov_matrix):
        """Minimize function to equalize risk contributions"""
        risk_contribs = risk_contribution(weights, cov_matrix)
        # We want all risk contributions to be equal, so minimize the sum of squared differences
        # from the average risk contribution.
        return np.sum((risk_contribs - np.mean(risk_contribs))**2) * 1000
    
    def compute_erc_weights(returns, output_file='erc_weights.csv', risk_contrib_file='erc_risk_contributions.csv'):
        """
        Compute ERC weights for each year and export to CSV
        Also saves risk contributions to a separate CSV file
        """
        weights_data = []
        risk_contrib_data = []
        
        # Iterate through the years from 2016 to 2024
        for year in range(2016, 2025):
            print(f"Computing weights for year {year}...")
            
            # Filter data for the current year
            daily_returns_year = returns.loc[returns.index.year == year]
            
            # Drop columns with any NaN values in this year
            daily_returns_year = daily_returns_year.dropna(axis=1)
            
            # Store the column names for the current year
            columns = daily_returns_year.columns.tolist()
            
            # Calculate covariance matrix
            covariance_matrix_year = daily_returns_year.cov()
            
            # Calculate ERC weights for the current year
            num_assets_year = len(covariance_matrix_year.columns)
            initial_weights_year = np.array(num_assets_year * [1. / num_assets_year])
            constraints_year = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
            bounds_year = tuple((0, 1) for asset in range(num_assets_year))
            options = {'ftol': 1e-10, 'maxiter': 1000}
            
            result_year = minimize(objective_function, initial_weights_year, 
                                  args=(covariance_matrix_year,),
                                  method='SLSQP', bounds=bounds_year, 
                                  constraints=constraints_year,
                                  options=options, tol=1e-10)
            
            erc_weights_year = result_year.x
            
            # Check the risk contributions for the optimized ERC weights
            erc_risk_contributions = risk_contribution(erc_weights_year, covariance_matrix_year)
            
            erc_risk_contributions_df = pd.DataFrame({'Risk Contribution': erc_risk_contributions}, index=covariance_matrix_year.columns)
            
            # Store weights with asset names
            weight_dict = {'year': year}
            for asset, weight in zip(columns, erc_weights_year):
                weight_dict[asset] = weight
            
            weights_data.append(weight_dict)
            
            # Store risk contributions with asset names
            risk_contrib_dict = {'year': year}
            for asset, risk_contrib in zip(columns, erc_risk_contributions):
                risk_contrib_dict[asset] = risk_contrib
            
            risk_contrib_data.append(risk_contrib_dict)
        
        # Create DataFrames
        weights_df = pd.DataFrame(weights_data)
        risk_contrib_df = pd.DataFrame(risk_contrib_data)
        
        # Export to CSV
        weights_df.to_csv(output_file, index=False)
        print(f"\nWeights exported to {output_file}")
        
        risk_contrib_df.to_csv(risk_contrib_file, index=False)
        print(f"Risk contributions exported to {risk_contrib_file}")
        
        return weights_df, risk_contrib_df
    
    
    weights_eq, risk_contrib_eq = compute_erc_weights(equity_returns, output_file='erc_weights_equity.csv', risk_contrib_file='erc_risk_contributions_equity.csv')
    weights_eqesg, risk_contrib_eqesg = compute_erc_weights(equity_esg_returns, output_file='erc_weights_equity_esg.csv', risk_contrib_file='erc_risk_contributions_equity_esg.csv')
    weights_com, risk_contrib_com = compute_erc_weights(commodity_returns, output_file='erc_weights_commodity.csv', risk_contrib_file='erc_risk_contributions_commodity.csv')
    weights_comseg, risk_contrib_comseg = compute_erc_weights(commodity_esg_returns, output_file='erc_weights_commodity_esg.csv', risk_contrib_file='erc_risk_contributions_commodity_esg.csv')
    weights_crypto, risk_contrib_crypto = compute_erc_weights(crypto_returns, output_file='erc_weights_crypto.csv', risk_contrib_file='erc_risk_contributions_crypto.csv')

importer_data(start='2016-01-01',end='2025-11-01')
