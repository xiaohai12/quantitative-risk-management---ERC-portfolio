import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Lumina Wealth | Premium Investment Portfolios",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS (The "Fancy & Pure" Aesthetic)
# -----------------------------------------------------------------------------
st.markdown("""
    <style>
    /* Import nice font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit Header and Footer for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Top Navbar Style */
    div.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Button Styling to look like Nav Links */
    .stButton > button {
        width: 100%;
        border: none;
        background-color: transparent;
        color: #555;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        color: #000;
        background-color: #f0f2f6;
    }
    .stButton > button:focus {
        color: #2E86C1;
        border-bottom: 2px solid #2E86C1;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* Hero Text */
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #1a2a6c, #b21f1f, #fdbb2d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }

    /* Section headers */
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #1a2a6c;
        padding-left: 15px;
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
# NAVIGATION BAR
# -----------------------------------------------------------------------------
def render_navbar():
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### **LUMINA WEALTH**")
        
    with col2:
        if st.button("Home"):
            navigate_to("Home")
    with col3:
        if st.button("Portfolios"):
            navigate_to("Portfolios")
    with col4:
        if st.button("Philosophy"):
            navigate_to("Philosophy")
    with col5:
        if st.button("Contact"):
            navigate_to("Contact")
    
    st.markdown("---")

# -----------------------------------------------------------------------------
# PAGES
# -----------------------------------------------------------------------------

def home_page():
    # -- Hero Section --
    st.markdown('<div class="hero-title">Wealth. Elevated.</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Intelligent portfolio management for the modern investor. <br>Pure data, zero clutter.</div>', unsafe_allow_html=True)

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

def portfolios_page():
    st.markdown('<div class="hero-title">Our Strategies</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌊 The Blue Ocean Fund")
        st.write("Focused on emerging markets and high-growth tech sectors.")
        st.progress(85, text="Risk Level: High")
        st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=["Tech", "Bio", "Crypto"]))
        
    with col2:
        st.subheader("🏔️ The Iron Mountain")
        st.write("Focused on dividends, bonds, and real estate trusts.")
        st.progress(30, text="Risk Level: Low")
        st.line_chart(pd.DataFrame(np.random.randn(20, 3), columns=["Bonds", "REITs", "Gold"]))

def philosophy_page():
    st.markdown('<div class="hero-title">Our Philosophy</div>', unsafe_allow_html=True)
    st.write("### Data over Emotion.")
    st.write("At Lumina, we believe that human emotion is the enemy of wealth generation. We use strict quantitative models to make decisions.")

def contact_page():
    st.markdown('<div class="hero-title">Get in Touch</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.text_input("Name")
        st.text_input("Email")
        st.selectbox("Interest", ["Individual Investment", "Corporate Treasury", "Retirement Planning"])
        st.text_area("Message")
        st.button("Send Message")
    
    with col2:
        st.map(pd.DataFrame({'lat': [40.7128], 'lon': [-74.0060]})) # NYC coordinates
        st.write("**Lumina Wealth HQ**")
        st.write("100 Wall Street, New York, NY")

# -----------------------------------------------------------------------------
# MAIN APP LOGIC
# -----------------------------------------------------------------------------

render_navbar()

if st.session_state.page == 'Home':
    home_page()
elif st.session_state.page == 'Portfolios':
    portfolios_page()
elif st.session_state.page == 'Philosophy':
    philosophy_page()
elif st.session_state.page == 'Contact':
    contact_page()

# Footer filler
st.write("")
st.write("")
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.8rem;'>© 2025 Lumina Wealth Management. All rights reserved. Investments involve risk.</div>", unsafe_allow_html=True)