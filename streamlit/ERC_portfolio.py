import streamlit as st
import numpy as np
import pandas as pd
import utils.web_util as wu
from statics import IMG_DIR
import utils.utilities as ut
import os

# Define the pages

st.set_page_config(page_title="Portfolios", layout="wide", initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()

# Override the horizontal padding for this page only
st.markdown("""
    <style>
    .block-container {
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1200px !important;
    }

    /* Hero section for title */
    .hero-assessment {
        background: linear-gradient(135deg, #CC6600 0%, #FF8C42 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }
     </style>
""", unsafe_allow_html=True)

# Nav bar
wu.render_navbar(IMG_DIR)

# Hero section
st.markdown("""
    <div class="hero-assessment">
        <h1>Design Your Investment Strategy</h1>
    </div>
""", unsafe_allow_html=True)

c1, c2 = st.columns([4, 1])



st.divider()
# ---
# 1. Asset & ESG Selection
# ---
col_header, col_link = st.columns([4, 1])

with col_header:
    st.header("1. Select Your Asset Classes")

with col_link:
    st.markdown(
        """
        <a href="https://xiaohai12-quantitative-risk-manag-streamlitstreamlit-app-w9wlfm.streamlit.app/~/+/LLM" 
           target="_blank" 
           style="display: inline-block; 
                  padding: 8px 16px; 
                  background-color: #FFCC99; 
                  color: #000; 
                  text-decoration: none; 
                  border-radius: 5px; 
                  font-weight: 600;
                  border: 2px solid #CC6600;
                  transition: all 0.3s ease;
                  text-align: center;
                  margin-top: 5px;">
            💬 Ask Amber for Help
        </a>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
    <p style="color: #666; font-size: 14px; margin-top: -10px;">
        Not sure which assets to choose? <strong>Chat with Amber</strong>, our AI assistant, 
        to get personalized investment recommendations based on your goals and risk profile.
    </p>
""", unsafe_allow_html=True)

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
    is_esg = st.toggle("Prioritize ESG",
                       help="If selected, this will use ESG-compliant versions of Equity and Commodities where available.")

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

# ---
# 2. Risk Level Selection
# ---
col_header, col_link = st.columns([4, 1])

with col_header:
    st.header("2. Set Your Risk level")

with col_link:
    st.markdown(
        """
        <a href="https://xiaohai12-quantitative-risk-manag-streamlitstreamlit-app-w9wlfm.streamlit.app/~/+/risk_preference" 
           target="_blank" 
           style="display: inline-block; 
                  padding: 8px 16px; 
                  background-color: #FFCC99; 
                  color: #000; 
                  text-decoration: none; 
                  border-radius: 5px; 
                  font-weight: 600;
                  border: 2px solid #CC6600;
                  transition: all 0.3s ease;
                  text-align: center;
                  margin-top: 5px;">
            📊 Take Risk Assessment
        </a>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
    <p style="color: #666; font-size: 14px; margin-top: -10px;">
        Unsure about your risk tolerance? <strong>Take our risk assessment quiz</strong> 
        to discover your ideal risk profile through a series of personalized questions.
    </p>
""", unsafe_allow_html=True)

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
            <h1 style="margin: 0px 0; font-size: 30px; font-weight: bold;">Score: {st.session_state.risk_score}</h1>
            <h1 style="margin: 0px 0; font-size: 24px;">{color} {profile} Profile</h2> 
            <p style="margin: 0px 0; font-size: 20px; color: #666;">{delta_label}</p>
        </div>
    """, unsafe_allow_html=True)

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

        
            # Load data
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))

            equity_data = pd.read_csv(BASE_DIR + "/dataImporter/equity_data.csv")
            commodity_data = pd.read_csv(BASE_DIR + "/dataImporter/commodities_data.csv")
            crypto_data = pd.read_csv(BASE_DIR + "/dataImporter/cryptos_data.csv")
            bonds_data = pd.read_csv(BASE_DIR + "/dataImporter/bonds_data.csv")
            equity_data_esg = pd.read_csv(BASE_DIR + "/dataImporter/equity_data_esg.csv")
            commodity_data_esg = pd.read_csv(BASE_DIR + "/dataImporter/commodity_data_esg.csv")

            equity_returns = pd.read_csv(BASE_DIR + "/dataImporter/equity_returns.csv")
            equity_esg_returns = pd.read_csv(BASE_DIR + "/dataImporter/equity_esg_returns.csv")
            commodity_returns = pd.read_csv(BASE_DIR + "/dataImporter/commodity_returns.csv")
            commodity_esg_returns = pd.read_csv(BASE_DIR + "/dataImporter/commodity_esg_returns.csv")
            crypto_returns = pd.read_csv(BASE_DIR + "/dataImporter/crypto_returns.csv")
            bonds_returns = pd.read_csv(BASE_DIR + "/dataImporter/bonds_returns.csv")

            # ERC portfolio
            equity_erc_returns = ut.erc_portfolio(equity_returns, weights_file= BASE_DIR + "/dataImporter/erc_weights_equity.csv")
            equity_esg_erc_returns = ut.erc_portfolio(equity_esg_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_equity_esg.csv")
            commodity_erc_returns = ut.erc_portfolio(commodity_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_commodity.csv")
            commodity_esg_erc_returns = ut.erc_portfolio(commodity_esg_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_commodity_esg.csv")
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
            col1, col2,col3 = st.columns([3,1, 2])
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
            col1, col2,col3 = st.columns([4,1, 4])
            with col1:
                st.pyplot(ut.plot_drawdown(all_portfolio_returns))

            with col3:
                st.pyplot(ut.plot_risk_contribution(risk_contrib_df, combined_returns))
