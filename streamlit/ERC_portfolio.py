import streamlit as st
import numpy as np
import pandas as pd
import utils.web_util as wu
from statics import IMG_DIR
# Define the pages

st.set_page_config(page_title="Portfolios",layout="wide",initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()
# Nav bar
wu.render_navbar(IMG_DIR)


st.title("Design Your Investment Strategy ")

c1, c2 = st.columns([4, 1])


with c1:
    st.caption("Use the options below to configure your portfolio.")

with c2:
    load_button = st.button("Load Data")

if load_button:
    
    with st.spinner("This might take a minute..."):
            
        # Portfolio construction code :
        import os
        import utils.utilities as ut
        
        # Load data
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
        equity_data = pd.read_csv(BASE_DIR + "/dataImporter/equity_data.csv")
        commodity_data = pd.read_csv(BASE_DIR +"/dataImporter/commodities_data.csv")
        crypto_data = pd.read_csv(BASE_DIR +"/dataImporter/cryptos_data.csv")
        bonds_data = pd.read_csv(BASE_DIR +"/dataImporter/bonds_data.csv")

        # Create ESG data
        equity_data_esg = ut.equity_to_esg(equity_data)
        commodity_data_esg = ut.commodity_to_esg(commodity_data)

        # Clean crypto to adjust trading days
        crypto_data['Date'] = pd.to_datetime(crypto_data['Date'])
        crypto_data = crypto_data.set_index('Date')
        crypto_data = crypto_data.loc[crypto_data.index.isin(equity_data['Date'])]

        # Compute daily returns
        st.session_state.equity_returns = ut.dailyreturns(equity_data)
        st.session_state.equity_esg_returns = ut.dailyreturns(equity_data_esg)
        st.session_state.commodity_returns = ut.dailyreturns(commodity_data)
        st.session_state.commodity_esg_returns = ut.dailyreturns(commodity_data_esg)
        st.session_state.crypto_returns = ut.dailyreturns(crypto_data)
        st.session_state.bonds_returns = ut.dailyreturns(bonds_data)

        # ERC portfolio
        st.session_state.equity_erc_returns = ut.erc_portfolio(st.session_state.equity_returns)
        st.session_state.equity_esg_erc_returns = ut.erc_portfolio(st.session_state.equity_esg_returns)
        st.session_state.commodity_erc_returns = ut.erc_portfolio(st.session_state.commodity_returns)
        st.session_state.commodity_esg_erc_returns = ut.erc_portfolio(st.session_state.commodity_esg_returns)
        st.session_state.crypto_erc_returns = ut.erc_portfolio(st.session_state.crypto_returns)
        
        st.success("Data loaded successfully !")         

st.divider()
# ---
# 1. Asset & ESG Selection
# ---
st.header("1. Select Your Asset Classes")

# Define the 6 asset classes based on your logic:
# [ Equity(Std), Equity(ESG) ,Commodity(Std), Commodity(ESG), Crypto, Bonds]
asset_labels = [
    'Equity (Standard)',
    'Equity (ESG)',
    'Commodity (Standard)',
    'Commodity (ESG)',
    'Crypto',
    'Bonds'
]

# Initialize the 6-element list
selected_assets_list = [0, 0, 0, 0, 0, 0]

# Use columns for a clean layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Available Assets")
    # Use toggles to represent the user's "base" choices
    select_bonds = st.toggle("Bonds", value=True)
    select_equity = st.toggle("Equity", value=True)
    select_commodity = st.toggle("Commodity")
    select_crypto = st.toggle("Cryptocurrency")

with col2:
    st.subheader("ESG Preference")
    # The global ESG switch
    is_esg = st.toggle("Prioritize ESG", help="If selected, this will use ESG-compliant versions of Equity and Commodities where available.")

# ---
# Logic to build the 6-element list
# ---

# 1. Bonds (Index 5)
if select_bonds:
    selected_assets_list[5] = 1

# 2. Crypto (Index 4)
if select_crypto:
    selected_assets_list[4] = 1

# 3. Equity (Index 0 or 1)
if select_equity:
    if is_esg:
        selected_assets_list[1] = 1  # Index 1 is Equity (ESG)
    else:
        selected_assets_list[0] = 1  # Index 0 is Equity (Standard)

# 4. Commodity (Index 2 or 3)
if select_commodity:
    if is_esg:
        selected_assets_list[3] = 1  # Index 3 is Commodity (ESG)
    else:
        selected_assets_list[2] = 1  # Index 2 is Commodity (Standard)


# ---
# Feedback for the user
# ---
st.subheader("Your Current Selection")

# Create a friendly list of names for the user to see
selected_names = [asset_labels[i] for i, val in enumerate(selected_assets_list) if val == 1]

if not selected_names:
    st.warning("Please select at least one asset class.")
else:
    st.info(f"**Selected Assets:** {', '.join(selected_names)}")


st.divider()



st.header("2. Set Your Risk level")
st.markdown("Use the slider below to set your risk tolerance level.")
st.write(" ")
st.write(" ")

# Initialize session state for risk_score if it doesn't exist
if 'risk_score' not in st.session_state:
    st.session_state.risk_score = 5  # Default value

# Horizontal slider for risk scale with a unique key
risk_score = st.slider(
    "Select your risk level (0 = Conservative, 10 = Aggressive):",
    min_value=0,
    max_value=10,
    value=st.session_state.risk_score,
    step=1,
    format="%d",
    help="Drag the slider to set your risk tolerance level",
    key="risk_slider"  # Add a unique key
)

# Update session state whenever the slider changes
if risk_score != st.session_state.risk_score:
    st.session_state.risk_score = risk_score

# Display the selected score with visual feedback
st.write(" ")


st.write(" ")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Determine profile based on score
    if st.session_state.risk_score <= 3:
        color = "🟢"
        profile = "Conservative"
        delta_label = "Low Risk Tolerance"
    elif st.session_state.risk_score <= 6:
        color = "🟡"
        profile = "Moderate"
        delta_label = "Medium Risk Tolerance"
    elif st.session_state.risk_score <= 8:
        color = "🟠"
        profile = "Growth-Oriented"
        delta_label = "High Risk Tolerance"
    else:
        color = "🔴"
        profile = "Aggressive"
        delta_label = "Very High Risk Tolerance"
    
    # Custom HTML for larger, centered metric
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: "#F0F2F6"; border-radius: 10px;">
            <h1 style="margin: 0px 0; font-size: 24px;">{color} {profile} Profile</h2>
            <h1 style="margin: 0px 0; font-size: 30px; font-weight: bold;">Score: {st.session_state.risk_score}</h1>
            <p style="margin: 0px 0; font-size: 20px; color: #666;">{delta_label}</p>
        </div>
    """, unsafe_allow_html=True)

    

# Visual progress bar
st.markdown("### Risk Tolerance Scale")
st.progress(st.session_state.risk_score / 10)

# Info about the selection
if st.session_state.risk_score <= 3:
    st.info("💼 **Conservative**: You prefer stability and capital preservation. Low-risk investments suit you best.")
elif st.session_state.risk_score <= 6:
    st.info(
        "⚖️ **Moderate**: You seek balance between risk and return. Diversified portfolios align with your preferences.")
elif st.session_state.risk_score <= 8:
    st.warning(
        "📊 **Growth-Oriented**: You're comfortable with volatility for higher returns. Stock-heavy portfolios fit your profile.")
else:
    st.error(
        "🚀 **Aggressive**: You have high risk tolerance and seek maximum returns. You accept potential short-term losses.")


st.divider()

# ---
# 3. Launch & Display Results
# ---
st.header("3. Your Portfolio Performance")
launch_button = st.button("Launch Portfolio Construction")

if launch_button:
    # Check if at least one asset is selected
    if sum(selected_assets_list) == 0:
        st.error("Cannot build portfolio. Please select at least one asset class above.")
    else:
        # This block runs only when the button is clicked
        with st.spinner("Constructing your optimal portfolio..."):

            import utilities as ut
            
            # ERC performmance
            equity_flat, equity_mean, equity_vol, equity_sharpe, equity_cumu = ut.erc_performance(st.session_state.equity_erc_returns, st.session_state.equity_returns,2017)
            equity_esg_flat, equity_esg_mean, equity_esg_vol, equity_esg_sharpe, equity_esg_cumu = ut.erc_performance(st.session_state.equity_esg_erc_returns, st.session_state.equity_esg_returns,2017)
            commodity_flat, commodity_mean, commodity_vol, commodity_sharpe, commodity_cumu = ut.erc_performance(st.session_state.commodity_erc_returns, st.session_state.commodity_returns,2017)
            commodity_esg_flat, commodity_esg_mean, commodity_esg_vol, commodity_esg_sharpe, commodity_esg_cumu = ut.erc_performance(st.session_state.commodity_esg_erc_returns, st.session_state.commodity_esg_returns,2017)
            crypto_flat, crypto_mean, crypto_vol, crypto_sharpe, crypto_cumu = ut.erc_performance(st.session_state.crypto_erc_returns, st.session_state.crypto_returns,2017)
            
            #Bonds performance
            bonds_flat, bonds_mean, bonds_vol, bonds_sharpe, bonds_cumu = ut.bonds_performance(st.session_state.bonds_returns, 2017)
            
            # Cumulative return plots
            cumu_grap_equity = ut.cumu_graph(equity_flat)
            cumu_graph_equity_esg = ut.cumu_graph(equity_esg_flat)
            cumu_graph_commodity = ut.cumu_graph(commodity_flat)
            cumu_graph_commodity_esg = ut.cumu_graph(commodity_esg_flat)
            cumu_graph_crypto = ut.cumu_graph(crypto_flat)
            cumu_graph_bonds = ut.cumu_graph(bonds_flat)

            # Combine returns
            combined_returns = ut.combine_returns(equity_flat, equity_esg_flat, commodity_flat, commodity_esg_flat, crypto_flat, bonds_flat,selected_assets_list)

            #Transform risk score into risk aversion coefficient
            risk_aversion = ut.riskscore_to_aversion(st.session_state.risk_score)
            
            #Final portfolio
            all_monthly_portfolio_returns = ut.meanvar_portfolio(combined_returns, risk_aversion)
            MeanVar_flat, MeanVar_mean, MeanVar_vol, MeanVar_sharpe, MeanVar_cumu = ut.erc_performance(all_monthly_portfolio_returns, combined_returns, 2018)
            cumu_graph_final = ut.cumu_graph(MeanVar_flat)
            
            st.success("Portfolio construction complete!")

            # --- Results Section ---
            st.subheader("📈 Simulated Performance")

            # Display  metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Expected Annual Return", f"{MeanVar_mean * 100:.2f}%" )
            col2.metric("Annual Volatility", f"{MeanVar_vol * 100:.2f}%")
            col3.metric("Sharpe Ratio", f"{MeanVar_sharpe:.2f}")
            col4.metric("Cumulative Return", f"{MeanVar_cumu:.2f}" )
            

            # Display  graph
            st.subheader("Portfolio Growth Simulation")
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.pyplot(cumu_graph_final)
                        

            












    

