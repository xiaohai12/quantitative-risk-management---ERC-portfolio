import streamlit as st
import pandas as pd
import numpy as np
import os
import utils.web_util as wu
from statics import IMG_DIR
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Amber Quant | Premium Investment Portfolios",
    page_icon="🔶",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom style
wu.apply_custom_css()

st.markdown("""
<style>
.feature-card {
    background-color: #FFCC99;
    padding: 20px;
    border-radius: 12px;
    min-height: 120px;    /* force same box height */
    display: flex;
    align-items: center;
    font-size: 16px;
}
.feature-title {
    font-size: 22px !important;
    font-weight: 700;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)
# -----------------------------------------------------------------------------
# STATE MANAGEMENT
# -----------------------------------------------------------------------------
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

def navigate_to(page):
    st.session_state.page = page

# -----------------------------------------------------------------------------
# HELPER FUNCTIONS (Data & Charts)
# -----------------------------------------------------------------------------
def get_portfolios_cumulative_returns():
    """Calculates cumulative returns for two portfolios."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Load portfolio returns (already cumulative based on filenames)
    portfolio1 = pd.read_csv(BASE_DIR + "/dataImporter/tradi_cumu.csv", index_col=0, parse_dates=True)
    portfolio2 = pd.read_csv(BASE_DIR + "/dataImporter/crypto_cumu.csv", index_col=0, parse_dates=True)

    # Since files are named "cumu", they likely already contain cumulative returns
    # So we DON'T need to calculate cumprod() again

    # Get dates from index
    dates = portfolio1.index

    # Get portfolio-level cumulative returns (average across assets if multiple columns)
    if portfolio1.shape[1] > 1:
        cum_return_portfolio1 = portfolio1.mean(axis=1)
    else:
        cum_return_portfolio1 = portfolio1.iloc[:, 0]

    if portfolio2.shape[1] > 1:
        cum_return_portfolio2 = portfolio2.mean(axis=1)
    else:
        cum_return_portfolio2 = portfolio2.iloc[:, 0]

    return pd.DataFrame({
        'Date': dates,
        'Portfolio_1_Cumulative': cum_return_portfolio1.values,
        'Portfolio_2_Cumulative': cum_return_portfolio2.values
    })

def create_chart(df):
    """Creates a fancy Plotly chart."""
    fig = go.Figure()

    # Add Portfolio1
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Portfolio_1_Cumulative'],
        mode='lines',
        name='Traditional Portfolio (Equities, Bonds, Commodities)',
        line=dict(color='#1976D2', width=3),
    ))

    # Add Portfolio2
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Portfolio_2_Cumulative'],
        mode='lines',
        name='Traditional Portfolio with Cryptocurrencies',
        line=dict(color='#F9A825', width=2)
    ))

    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="Cumulative Returns (%)",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=450
    )
    
    # Remove gridlines for cleaner look
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    
    return fig



# -----------------------------------------------------------------------------
# PAGES
# -----------------------------------------------------------------------------

def home_page():
    # -- Hero Section --
    forest_path = os.path.join(IMG_DIR,"forest.png")
    forest_base64 = wu.image_to_base64(forest_path) 
    
    # 1. Use f""" for string interpolation
    # 2. Use url('data:image/png;base64, ...') syntax in CSS
    st.markdown(f"""
        <style>
        /* ... your other fonts and settings ... */
        
        .hero-section {{
            position: relative;
            height: 400px;
            /* THE FIX IS HERE: Use url() instead of <img> */
            background-image: url("data:image/png;base64,{forest_base64}");
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            border-radius: 15px; /* Optional: looks nice with cards */
        }}
        
        .hero-section h1, .hero-section p {{
            color: white;
            text-shadow:
                -1px -1px 0 black,
                 1px -1px 0 black,
                -1px  1px 0 black,
                 1px  1px 0 black;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # 3. IMPORTANT: You must actually create the HTML Div that uses the class
    st.markdown("""
        <div class="hero-section">
        
        </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .top {
            font-size: 42px; /* bigger first line */
            font-weight: 700;
            margin-bottom: 12px;
        }
        .lead {
            font-size: 18px;
            margin-bottom: 8px;
        }
        
        </style>
        
        <div class="container">
        <div class="top">Welcome to Amber Quant, Your Partner in Asset Management</div>
        <div class="lead">At Amber Quant, our clients are at the heart of everything we do.</div>
        <div class="lead">Leveraging our deep sector knowledge and the expertise of our international network, we work in close partnership with our clients. Our goal is to fully understand their long-term strategic objectives and their unique risk profiles, enabling us to design and propose customized investment solutions and portfolios specifically adapted to their needs.</div>
        <div class="lead">Whatever your financial ambitions, our teams are ready to listen and help you achieve them.</div>
        </div>
        """,
        unsafe_allow_html=True,
        )

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
    
    # -- Key Metrics --
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="AUM", value="CHF 342M", delta="+12% YTD")
    m2.metric(label="Avg. Client Return", value="18.4%", delta="+4.2% vs Market")
    m3.metric(label="Active Portfolios", value="1,204", delta="24 New")
    m4.metric(label="Management Fee", value="0.65%", delta_color="off")

    st.write("") # Spacer
    st.write("") 

    # -- Interactive Chart Section --
    st.markdown('<div class="section-header">Historic Performance</div>', unsafe_allow_html=True)
    st.write("Compare the historical performance of our best-selling portfolios.")
    
    df = get_portfolios_cumulative_returns()
    fig = create_chart(df)
    st.plotly_chart(fig, use_container_width=True)

    # -- Value Props --
    st.markdown('<div class="section-header">Why Amber?</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        st.markdown("<p class='feature-title'>Adaptive Portfolio Management</p>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'>We continuously monitor changes in correlations and volatility regimes to maintain a stable and efficient portfolio structure.</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<p class='feature-title'>Full Transparency</p>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'>Every allocation is clear and explainable. You can see exactly how each asset contributes to total risk and performance — no black box.</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<p class='feature-title'>Broad Multi-Asset Diversification</p>", unsafe_allow_html=True)
        st.markdown("<div class='feature-card'>Our portfolios allocate across five distinct asset classes, reducing concentration risks and enhancing long-term stability across different market environments.</div>", unsafe_allow_html=True)
    # -- CTA --
    st.write("")
    st.write("")
    cta_col1, cta_col2, cta_col3 = st.columns([1,2,1])
    # ...existing code...
    with cta_col2:
        st.markdown(
            """
            <style>
            .cta-box {
              background-color: #f8f9fa;
              border-radius: 15px;
              padding: 30px;
              text-align: center;
              border: 1px solid #ddd;
            }
            .cta-btn {
              display: inline-block;
              margin-top: 16px;
              padding: 10px 20px;
              background: transparent;               /* no background by default */
              color: #2E86C1;                        /* button text color */
              text-decoration: none;
              border-radius: 8px;
              font-weight: 600;
              border: 2px solid transparent;         /* keep size stable */
              transition: background 0.18s ease, color 0.18s ease, border-color 0.18s ease;
            }
            .cta-btn:hover {
              background: #FFCC99;                   /* orange on hover */
              color: #000;
              border-color: #CC6600;
            }
            </style>
            <div class="cta-box">
                <h3>Ready to optimize your wealth?</h3>
                <p>Schedule a free consultation with our senior advisors today.</p>
                <a class="cta-btn" href="?page=contact">Contact Us</a>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.page == "contact":
        st.switch_page("Contact.py")


wu.render_navbar(IMG_DIR)


if st.session_state.page == 'Home':
    home_page()


# Footer filler
st.write("")
st.write("")
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.8rem;'>© 2025 Amber Wealth Management. All rights reserved. Investments involve risk.</div>", unsafe_allow_html=True)