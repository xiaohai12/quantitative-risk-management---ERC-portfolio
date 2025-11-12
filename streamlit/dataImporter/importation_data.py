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
def import_cryptos(start_date):
    response = requests.get("https://min-api.cryptocompare.com/data/all/coinlist")
    coinlist = response.json()['Data']
    coinlist_ids = list(coinlist.keys())

    def get_hist_all(symbol, currency='USD', limit=1500, start_date=None, sleep=0.25):
        """
        Fetch daily history for `symbol` going back until `start_date` (inclusive).
        Uses paging (toTs) and finally slices to start_date to avoid overshooting.
        """
        url = "https://min-api.cryptocompare.com/data/v2/histoday"
        frames = []
        end_ts = None

        start_ts = None
        if start_date is not None:
            start_ts = int(pd.to_datetime(start_date).timestamp())

        while True:
            params = {'fsym': symbol, 'tsym': currency, 'limit': limit}
            if end_ts is not None:
                params['toTs'] = end_ts

            r = requests.get(url, params=params).json()
            if r.get('Response') != 'Success':
                print("API error:", r.get('Message'))
                break

            data = r['Data']['Data']
            if not data:
                break

            df = pd.DataFrame(data)
            frames.append(df)

            earliest = int(df['time'].min())

            # stop if we've reached or passed requested start_date (give one-day tolerance)
            if start_ts is not None and earliest <= start_ts + 86400:
                break

            # if API returned fewer than limit points, no more older data available
            if len(df) < limit:
                break

            # set next toTs to one day before earliest to avoid overlap
            end_ts = earliest - 86400
            time.sleep(sleep)

        if not frames:
            return None

        full = pd.concat(frames, ignore_index=True).drop_duplicates(subset='time').sort_values('time')
        full['time'] = pd.to_datetime(full['time'], unit='s')
        full = full.set_index('time')

        # enforce start_date slice to avoid extra history
        if start_date is not None:
            full = full[full.index >= pd.to_datetime(start_date)]

        # keep only close column renamed to symbol
        full = full[['close']].rename(columns={'close': symbol})
        return full

    price_dfs = []
    # Example: get top 10 coins
    symbols = [
        "BTC", "ETH", "BNB", "XRP", "SOL", "DOGE", "TRX", "ADA",
        "AVAX", "DOT", "MATIC", "LTC", "SHIB", "LINK", "BCH", "ALGO", "NEAR", "XLM",
        "ATOM", "VET", "EOS", "FIL", "APE", "ICP", "SUI", "FTM", "AAVE", "GRT",
        "HBAR", "XMR", "THETA", "MANA", "ZEC", "NEKO", "MKR", "LDO", "SNX", "CRO"
    ]
    for sym in symbols:
        df = get_hist_all(sym, start_date=start_date )
        if df is not None:
            price_dfs.append(df)
        time.sleep(0.1)  # Respect rate limit

    df_all = pd.concat(price_dfs, axis=1)
    df_all = df_all.reset_index()

    df_all.to_csv('cryptos_data.csv')

start_date = '2016-01-01'
end_date = '2025-10-31'
#import_equity(start_date, end_date)
start_date = '2020-01-01'
import_cryptos(start_date)