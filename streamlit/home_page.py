import streamlit as st
import pandas as pd
import numpy as np
import os
import utils.web_util as wu
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
def get_dummy_data():
    """Generates random walk data to simulate portfolio performance."""
    dates = pd.date_range(start=date.today() - timedelta(days=365*2), end=date.today())
    
    # Simulate returns
    np.random.seed(42)
    
    # S&P 500 Simulation
    sp500_returns = np.random.normal(loc=0.0003, scale=0.01, size=len(dates))
    sp500_price = 100 * (1 + sp500_returns).cumprod()
    
    # Lumina Portfolio Simulation (Slightly better alpha, lower beta)
    lumina_returns = np.random.normal(loc=0.0004, scale=0.008, size=len(dates))
    lumina_price = 100 * (1 + lumina_returns).cumprod()

    return pd.DataFrame({'Date': dates, 'S&P 500': sp500_price, 'Lumina Aggressive': lumina_price})

def create_chart(df):
    """Creates a fancy Plotly chart."""
    fig = go.Figure()

    # Add Lumina Line (Filled Area)
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Lumina Aggressive'],
        mode='lines',
        name='Lumina Aggressive',
        line=dict(color='#2E86C1', width=3),
        fill='tozeroy',
        fillcolor='rgba(46, 134, 193, 0.1)'
    ))

    # Add S&P 500 Line (Dashed)
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['S&P 500'],
        mode='lines',
        name='S&P 500 Benchmark',
        line=dict(color='#95A5A6', width=2, dash='dot')
    ))

    fig.update_layout(
        title="",
        xaxis_title="",
        yaxis_title="Normalized Return (%)",
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
    forest_path = '/mount/src/quantitative-risk-management---erc-portfolio/streamlit/pictures/forest.png'
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
        
        <style>
        .hero-section h1, .hero-section p {
            color: white;
            text-shadow:
                -2px -2px 0 black,
                 2px -2px 0 black,
                -2px  2px 0 black,
                 2px  2px 0 black;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 3. IMPORTANT: You must actually create the HTML Div that uses the class
    st.markdown("""
        <div class="hero-section">
            <h1>Welcome to the Portfolio</h1>
            <p>Quantitative Risk Management</p>
        </div>
    """, unsafe_allow_html=True)
    
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # -- Key Metrics --
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Total Assets Managed", value="$142M", delta="+12% YTD")
    m2.metric(label="Avg. Client Return", value="18.4%", delta="+4.2% vs Market")
    m3.metric(label="Active Portfolios", value="1,204", delta="24 New")
    m4.metric(label="Management Fee", value="0.65%", delta_color="off")

    st.write("") # Spacer
    st.write("") 

    # -- Interactive Chart Section --
    st.markdown('<div class="section-header">Performance Projection</div>', unsafe_allow_html=True)
    st.write("Track the historical performance of our flagship aggressive growth algorithm compared to the market benchmark.")
    
    df = get_dummy_data()
    fig = create_chart(df)
    st.plotly_chart(fig, use_container_width=True)

    # -- Value Props --
    st.markdown('<div class="section-header">Why Lumina?</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("### 🛡️ Risk-First Approach")
        st.info("We prioritize capital preservation. Our algorithms actively hedge against downside volatility before chasing upside.")
    
    with c2:
        st.markdown("### 🧠 AI-Driven Rebalancing")
        st.info("Your portfolio is monitored 24/7. We automatically rebalance based on macro-economic shifts, not just calendar dates.")

    with c3:
        st.markdown("### 💎 Transparent Fee Structure")
        st.info("No hidden trading fees. No front-loading. Just a simple, flat advisory fee based on assets under management.")

    # -- CTA --
    st.write("")
    st.write("")
    cta_col1, cta_col2, cta_col3 = st.columns([1,2,1])
    with cta_col2:
        st.markdown(
            """
            <div style="background-color: #f8f9fa; border-radius: 15px; padding: 30px; text-align: center; border: 1px solid #ddd;">
                <h3>Ready to optimize your wealth?</h3>
                <p>Schedule a free consultation with our senior advisors today.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )


wu.render_navbar()


if st.session_state.page == 'Home':
    home_page()


# Footer filler
st.write("")
st.write("")
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.8rem;'>© 2025 Lumina Wealth Management. All rights reserved. Investments involve risk.</div>", unsafe_allow_html=True)
