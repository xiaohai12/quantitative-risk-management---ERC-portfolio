def importer_data(start='2016-01-01',end='2025-11-01'):
    import yfinance as yf
    import requests
    import pandas as pd
    import time

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

    import_equity(start_date= start, end_date=end)
    import_cryptos(start_date='2020-01-01', end_date=end)
    import_commodities(start_date=start, end_date=end)
    import_bonds(start_date=start, end_date=end)