import streamlit as st
import numpy as np
import pandas as pd
import utils.web_util as wu
from statics import IMG_DIR
import utils.utilities as ut
import os

# Define the pages
st.set_page_config(page_title="Portfolios", page_icon="🔶",  layout="wide", initial_sidebar_state="collapsed")

# Custom style
wu.apply_custom_css()

# Override the horizontal padding for this page only
st.markdown("""
    <style>
    /* Hero section for title */
    .hero-assessment {
        background: linear-gradient(135deg, #CC6600 0%, #FF8C42 100%);
        padding: 40px;
        border-radius: 15px;
        color: white;
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

st.markdown(
    "<p style='font-size: 20px; font-weight: 500; margin-bottom: -25px'>Choose an asset class to learn more about its ERC Portfolio characteristics.</p>",
    unsafe_allow_html=True
)

selected_asset = st.selectbox(
    "",
    options=asset_labels,
    index=0
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Display different content based on selection
if selected_asset == 'Equity (Standard)':
    st.write("""
    **Standard equity investments** include stocks and shares of publicly traded companies.
    These offer potential for capital appreciation and dividend income.
    """)
    
    equity_returns = pd.read_csv(BASE_DIR + "/dataImporter/equity_returns.csv")
    equity_erc_returns = ut.erc_portfolio(equity_returns, weights_file= BASE_DIR + "/dataImporter/erc_weights_equity.csv")
    equity_flat, equity_mean, equity_vol, equity_sharpe, equity_cumu = ut.erc_performance(
    equity_erc_returns, equity_returns, 2017)
    
    cumu_grap_equity = ut.cumu_graph(equity_flat)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Annual Return", f"{equity_mean * 100:.2f}%")
    col2.metric("Annual Volatility", f"{equity_vol * 100:.2f}%")
    col3.metric("Sharpe Ratio", f"{equity_sharpe:.2f}")
    col4.metric(
        "Cumulative Return",
        f"{equity_cumu * 100:.2f}%",
        delta=None)
    
    col1, col2, col3 = st.columns([4.5, 0.6, 5])
    with col1:
        st.pyplot(cumu_grap_equity)
    with col3:
        risk_contrib = pd.read_csv(BASE_DIR + "/dataImporter/erc_risk_contributions_equity.csv")
        fig, ax = ut.plot_risk_contributions_solo(risk_contrib)
        st.pyplot(fig)

elif selected_asset == 'Equity (ESG)':
    st.write("""
    **ESG Equity** excludes brown companies with bad Environmental, Social, and Governance practices.
    Invest in sustainable and socially responsible companies.
    """)
    
    equity_esg_returns = pd.read_csv(BASE_DIR + "/dataImporter/equity_esg_returns.csv")
    equity_esg_erc_returns = ut.erc_portfolio(equity_esg_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_equity_esg.csv")
    equity_esg_flat, equity_esg_mean, equity_esg_vol, equity_esg_sharpe, equity_esg_cumu = ut.erc_performance(
    equity_esg_erc_returns, equity_esg_returns, 2017)
    cumu_graph_equity_esg = ut.cumu_graph(equity_esg_flat)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Annual Return", f"{equity_esg_mean * 100:.2f}%")
    col2.metric("Annual Volatility", f"{equity_esg_vol * 100:.2f}%")
    col3.metric("Sharpe Ratio", f"{equity_esg_sharpe:.2f}")
    col4.metric(
        "Cumulative Return",
        f"{equity_esg_cumu * 100:.2f}%",
        delta=None)
    
    col1, col2, col3 = st.columns([4.5, 0.6, 5])
    with col1:
        st.pyplot(cumu_graph_equity_esg)
    with col3:
        equity_esg_rc = pd.read_csv(BASE_DIR + "/dataImporter/erc_risk_contributions_equity_esg.csv")
        fig, ax = ut.plot_risk_contributions_solo(equity_esg_rc)
        st.pyplot(fig)

elif selected_asset == 'Commodity (Standard)':
    st.write("""
    **Standard commodities** include investments in raw materials like oil, gold, agricultural products, etc.
    Good for portfolio diversification and inflation hedging.
    """)
    
    commodity_returns = pd.read_csv(BASE_DIR + "/dataImporter/commodity_returns.csv")
    commodity_erc_returns = ut.erc_portfolio(commodity_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_commodity.csv")
    commodity_flat, commodity_mean, commodity_vol, commodity_sharpe, commodity_cumu = ut.erc_performance(
    commodity_erc_returns, commodity_returns, 2017)
    cumu_graph_commodity = ut.cumu_graph(commodity_flat)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Annual Return", f"{commodity_mean * 100:.2f}%")
    col2.metric("Annual Volatility", f"{commodity_vol * 100:.2f}%")
    col3.metric("Sharpe Ratio", f"{commodity_sharpe:.2f}")
    col4.metric(
        "Cumulative Return",
        f"{commodity_cumu * 100:.2f}%",
        delta=None)
    
    col1, col2, col3 = st.columns([4.5, 0.6, 5])
    with col1:
        st.pyplot(cumu_graph_commodity)
    with col3:
        risk_contrib = pd.read_csv(BASE_DIR + "/dataImporter/erc_risk_contributions_commodity.csv")
        fig, ax = ut.plot_risk_contributions_solo(risk_contrib)
        st.pyplot(fig)
    
elif selected_asset == 'Commodity (ESG)':
    st.write("""
    **ESG Commodities** excludes environmentally harmful commodities, including fossil fuels and natural gas
    """)
    
    commodity_esg_returns = pd.read_csv(BASE_DIR + "/dataImporter/commodity_esg_returns.csv")
    commodity_esg_erc_returns = ut.erc_portfolio(commodity_esg_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_commodity_esg.csv")
    commodity_esg_flat, commodity_esg_mean, commodity_esg_vol, commodity_esg_sharpe, commodity_esg_cumu = ut.erc_performance(
    commodity_esg_erc_returns, commodity_esg_returns, 2017)
    cumu_graph_commodity_esg = ut.cumu_graph(commodity_esg_flat)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Annual Return", f"{commodity_esg_mean * 100:.2f}%")
    col2.metric("Annual Volatility", f"{commodity_esg_vol * 100:.2f}%")
    col3.metric("Sharpe Ratio", f"{commodity_esg_sharpe:.2f}")
    col4.metric(
        "Cumulative Return",
        f"{commodity_esg_cumu * 100:.2f}%",
        delta=None)
    
    col1, col2, col3 = st.columns([4.5, 0.6, 5])
    with col1:
        st.pyplot(cumu_graph_commodity_esg)
    with col3:
        risk_contrib = pd.read_csv(BASE_DIR + "/dataImporter/erc_risk_contributions_commodity_esg.csv")
        fig, ax = ut.plot_risk_contributions_solo(risk_contrib)
        st.pyplot(fig)
    
elif selected_asset == 'Crypto':
    st.write("""
    **Cryptocurrency** investments include Bitcoin, Ethereum, and other digital assets.
    High volatility with potential for significant gains or losses.
    """)
    
    crypto_returns = pd.read_csv(BASE_DIR + "/dataImporter/crypto_returns.csv")
    crypto_erc_returns = ut.erc_portfolio(crypto_returns, weights_file=BASE_DIR + "/dataImporter/erc_weights_crypto.csv")
    crypto_flat, crypto_mean, crypto_vol, crypto_sharpe, crypto_cumu = ut.erc_performance(
    crypto_erc_returns, crypto_returns, 2017)
    cumu_graph_crypto = ut.cumu_graph(crypto_flat)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Annual Return", f"{crypto_mean * 100:.2f}%")
    col2.metric("Annual Volatility", f"{crypto_vol * 100:.2f}%")
    col3.metric("Sharpe Ratio", f"{crypto_sharpe:.2f}")
    col4.metric(
        "Cumulative Return",
        f"{crypto_cumu * 100:.2f}%",
        delta=None)
    
    col1, col2, col3 = st.columns([4.5, 0.6, 5])
    with col1:
        st.pyplot(cumu_graph_crypto)
    with col3:
        risk_contrib = pd.read_csv(BASE_DIR + "/dataImporter/erc_risk_contributions_crypto.csv")
        fig, ax = ut.plot_risk_contributions_solo(risk_contrib)
        st.pyplot(fig)
    
elif selected_asset == 'Bonds':
    st.write("""
    **Bonds** are fixed-income securities that provide regular interest payments.
    Lower risk compared to equities, ideal for conservative investors.
    """)
    
    bonds_returns = pd.read_csv(BASE_DIR + "/dataImporter/bonds_returns.csv")
    bonds_flat, bonds_mean, bonds_vol, bonds_sharpe, bonds_cumu = ut.bonds_performance(
    bonds_returns, 2017)
    cumu_graph_bonds = ut.cumu_graph(bonds_flat)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Expected Annual Return", f"{bonds_mean * 100:.2f}%")
    col2.metric("Annual Volatility", f"{bonds_vol * 100:.2f}%")
    col3.metric("Sharpe Ratio", f"{bonds_sharpe:.2f}")
    col4.metric(
        "Cumulative Return",
        f"{bonds_cumu * 100:.2f}%",
        delta=None)
    
    col1, col2, col3 = st.columns([4.5, 0.6, 5])
    with col1:
        st.pyplot(cumu_graph_bonds)
    with col3:
        st.write("**Risk Contribution**")
        st.write("Bonds is a single index and hence has a single absolute risk contribution of 1.0")

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


# Initialize the 6-element list
selected_assets_list = [0, 0, 0, 0, 0, 0]

# Use columns for a clean layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Available ERC Portfolios")
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

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Determine profile based on score
    if st.session_state.risk_score <= 3:
        color = "🟢"
        profile = "Conservative"
    elif st.session_state.risk_score <= 6:
        color = "🟡"
        profile = "Moderate"
    elif st.session_state.risk_score <= 8:
        color = "🟠"
        profile = "Growth-Oriented"
    else:
        color = "🔴"
        profile = "Aggressive"

    # Custom HTML for larger, centered metric
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: "#F0F2F6"; border-radius: 10px;">
            <h1 style="margin: 0px 0; font-size: 30px; font-weight: bold;">Score: {st.session_state.risk_score}</h1>
            <h1 style="margin: 0px 0; font-size: 24px;">{color} {profile} Profile</h2> 
        </div>
    """, unsafe_allow_html=True)

# Info about the selection
if st.session_state.risk_score <= 3:
    st.info("💼 **Low Risk Tolerance**: You prefer stability and capital preservation. Low-risk investments suit you best.")
elif st.session_state.risk_score <= 6:
    st.info(
        "⚖️ **Medium Risk Tolerance**: You seek balance between risk and return. Diversified portfolios align with your preferences.")
elif st.session_state.risk_score <= 8:
    st.warning(
        "📊 **High Risk Tolerance**: You're comfortable with volatility for higher returns. Stock-heavy portfolios fit your profile.")
else:
    st.error(
        "🚀 **Very High Risk Tolerance**: You have high risk tolerance and seek maximum returns. You accept potential short-term losses.")

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
