import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date

st.set_page_config(page_title="Yahoo Finance Long-History Downloader", layout="wide")
st.title("📈 Yahoo Finance – Long-Term Data Downloader")

st.write("""
Use this app to download and visualize long-term price data (up to 30+ years)
for multiple tickers from Yahoo Finance.
""")

# --- User Inputs ---
default_tickers = "AAPL, MSFT, NVDA, AMZN, META, GOOGL, SPY"
tickers_input = st.text_input("Enter tickers (comma-separated):", default_tickers)
start_date = st.date_input("Start Date", value=date(2020, 1, 1))
end_date = st.date_input("End Date", value=date.today())

# --- Cache Yahoo Finance Data ---
@st.cache_data(ttl=10, show_spinner=True)  # cache for 1 day
def load_long_data(tickers, start_date, end_date):
    st.write(f'the tickers are {tickers}, with start date {start_date} and end date {end_date}')
    start_date = '2020-01-01'
    end_date = '2025-10-31'

    sp500_tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "SPY"]

    data = yf.download(sp500_tickers, start=start_date, end=end_date)['Close']
    st.write(f"Data downloaded successfully, shape: {data.shape}")
    return data 

# --- Button to trigger download ---
if st.button("🚀 Download Data"):
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    if not tickers:
        st.warning("Please enter at least one valid ticker.")
    else:
        with st.spinner("Downloading data... This may take a minute ⏳"):
            df = load_long_data(tickers, start_date, end_date)
        
        if df.empty:
            st.error("No data returned. Please check the tickers or date range.")
        else:
            st.success(f"✅ Data successfully downloaded for {len(tickers)} tickers.")
            
            # --- Display sample data ---
            st.write("### 📊 Data Preview")
            st.dataframe(df.head(10))
            
            # --- Select ticker for plotting ---
            ticker_choice = st.selectbox("Select a ticker to visualize:", tickers)
            try:
                st.write(f"### 📉 Adjusted Close Price: {ticker_choice}")
                st.line_chart(df[ticker_choice]["Adj Close"])
            except Exception as e:
                st.error(f"Unable to plot {ticker_choice}: {e}")

            # --- Show summary info ---
            st.write("### ℹ️ Dataset Summary")
            st.write(df.describe())
    
if st.button("🚀 Refresh Data"):
    st.cache_data.clear()