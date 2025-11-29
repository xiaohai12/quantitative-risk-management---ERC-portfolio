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
    background-color: #eef5ff;
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
            
function goToContact() {
    const url = new URL(window.location);
    url.searchParams.set("page", "contact");
    window.location.href = url.toString();
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
    
    # amber Portfolio Simulation (Slightly better alpha, lower beta)
    amber_returns = np.random.normal(loc=0.0004, scale=0.008, size=len(dates))
    amber_price = 100 * (1 + amber_returns).cumprod()

    return pd.DataFrame({'Date': dates, 'S&P 500': sp500_price, 'Amber Aggressive': amber_price})

def create_chart(df):
    """Creates a fancy Plotly chart."""
    fig = go.Figure()

    # Add amber Line (Filled Area)
    fig.add_trace(go.Scatter(
        x=df['Date'], y=df['Amber Aggressive'],
        mode='lines',
        name='Amber Aggressive',
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
    st.markdown('<div class="section-header">Performance Projection</div>', unsafe_allow_html=True)
    st.write("Track the historical performance of our flagship aggressive growth algorithm compared to the market benchmark.")
    
    df = get_dummy_data()
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
    with cta_col2:
        st.markdown(
            """
            <div onclick="goToContact()" 
                style="cursor: pointer; background-color: #f8f9fa; border-radius: 15px; padding: 30px; text-align: center; border: 1px solid #ddd;">
                <h3>Ready to optimize your wealth?</h3>
                <p>Schedule a free consultation with our senior advisors today.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


wu.render_navbar(IMG_DIR)


if st.session_state.page == 'Home':
    home_page()


# Footer filler
st.write("")
st.write("")
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.8rem;'>© 2025 Amber Wealth Management. All rights reserved. Investments involve risk.</div>", unsafe_allow_html=True)
