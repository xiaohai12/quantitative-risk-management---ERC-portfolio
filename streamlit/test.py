import streamlit as st
import pandas as pd
import plotly.express as px
import utils.utilities as ut
import os
import seaborn as sns

# Load data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

equity_returns = pd.read_csv(BASE_DIR + "/dataImporter/equity_returns.csv")
equity_esg_returns = pd.read_csv(BASE_DIR + "/dataImporter/equity_esg_returns.csv")
commodity_returns = pd.read_csv(BASE_DIR + "/dataImporter/commodity_returns.csv")
commodity_esg_returns = pd.read_csv(BASE_DIR + "/dataImporter/commodity_esg_returns.csv")
crypto_returns = pd.read_csv(BASE_DIR + "/dataImporter/crypto_returns.csv")
bonds_returns = pd.read_csv(BASE_DIR + "/dataImporter/bonds_returns.csv")

# ERC portfolio
equity_erc_returns = ut.erc_portfolio(equity_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_equity.csv")
equity_esg_erc_returns = ut.erc_portfolio(equity_esg_returns,
                                          weights_file=BASE_DIR + "/dataImporter/erc_weights_equity_esg.csv")
commodity_erc_returns = ut.erc_portfolio(commodity_returns,
                                         weights_file=BASE_DIR + "/dataImporter/erc_weights_commodity.csv")
commodity_esg_erc_returns = ut.erc_portfolio(commodity_esg_returns,
                                             weights_file=BASE_DIR + "/dataImporter/erc_weights_commodity_esg.csv")
crypto_erc_returns = ut.erc_portfolio(crypto_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_crypto.csv")

# ERC performmance
equity_flat, equity_mean, equity_vol, equity_sharpe, equity_cumu = ut.erc_performance(
    equity_erc_returns, equity_returns, 2017)
equity_esg_flat, equity_esg_mean, equity_esg_vol, equity_esg_sharpe, equity_esg_cumu = ut.erc_performance(
    equity_esg_erc_returns, equity_esg_returns, 2017)
commodity_flat, commodity_mean, commodity_vol, commodity_sharpe, commodity_cumu = ut.erc_performance(
    commodity_erc_returns, commodity_returns, 2017)
commodity_esg_flat, commodity_esg_mean, commodity_esg_vol, commodity_esg_sharpe, commodity_esg_cumu = ut.erc_performance(
    commodity_esg_erc_returns, commodity_esg_returns, 2017)
crypto_flat, crypto_mean, crypto_vol, crypto_sharpe, crypto_cumu = ut.erc_performance(
    crypto_erc_returns, crypto_returns, 2017)

# Bonds performance
bonds_flat, bonds_mean, bonds_vol, bonds_sharpe, bonds_cumu = ut.bonds_performance(
    bonds_returns, 2017)

# Cumulative return plots
cumu_grap_equity = ut.cumu_graph(equity_flat)
cumu_graph_equity_esg = ut.cumu_graph(equity_esg_flat)
cumu_graph_commodity = ut.cumu_graph(commodity_flat)
cumu_graph_commodity_esg = ut.cumu_graph(commodity_esg_flat)
cumu_graph_crypto = ut.cumu_graph(crypto_flat)
cumu_graph_bonds = ut.cumu_graph(bonds_flat)

# Combine returns
combined_returns = ut.combine_returns(equity_flat, equity_esg_flat, commodity_flat, commodity_esg_flat,
                                      crypto_flat, bonds_flat, selected_assets_list)

# Transform risk score into risk aversion coefficient
risk_aversion = ut.riskscore_to_aversion(st.session_state.risk_score)

# Final portfolio
all_portfolio_returns, weights_df = ut.meanvar_portfolio(combined_returns, risk_aversion)
MeanVar_flat, MeanVar_mean, MeanVar_vol, MeanVar_sharpe, MeanVar_cumu = ut.erc_performance(
    all_portfolio_returns, combined_returns, 2018)

risk_contrib_df = ut.calculate_risk_contribution(weights_df, combined_returns)

st.success("Portfolio construction complete!")

# --- Results Section ---
st.subheader("Historic  Portfolio Performance :")

st.markdown("<br><br>", unsafe_allow_html=True)
# Display  graph
col1, col2, col3 = st.columns([3, 1, 2])
with col1:
    cumu_graph_final = ut.cumu_graph_vol(MeanVar_flat)
    st.pyplot(cumu_graph_final)

with col3:
    fig1 = ut.plot_portfolio_composition(weights_df, "Average Portfolio Composition")
    st.pyplot(fig1)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# Display  metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Expected Annual Return", f"{MeanVar_mean * 100:.2f}%")
col2.metric("Annual Volatility", f"{MeanVar_vol * 100:.2f}%")
col3.metric("Sharpe Ratio", f"{MeanVar_sharpe:.2f}")
col4.metric(
    "Cumulative Return",
    f"{MeanVar_cumu * 100:.2f}%",
    delta=None
)

st.markdown("<br><br>", unsafe_allow_html=True)
# Display  graph
col1, col2, col3 = st.columns([4, 1, 4])
with col1:
    st.pyplot(ut.plot_drawdown(all_portfolio_returns))

with col3:
    st.pyplot(ut.plot_risk_contribution(risk_contrib_df, combined_returns))